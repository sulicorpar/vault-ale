import React, { createContext, useContext, useCallback, useMemo } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';
import { useAuth } from './AuthContext';
import {
  paymentMethodFromDb, paymentMethodToDb,
  paymentStatusFromDb, paymentStatusToDb,
  checklistStatusFromDb, checklistStatusToDb,
} from '@/lib/enum-maps';
import type { Customer, Payment, OpsChecklist, AuditLog, MessageTemplate, PaymentMethod, PaymentStatus, ChecklistStatus } from '@/types/booking';
import { DEFAULT_CHECKLIST_ITEMS } from '@/types/booking';

interface DataContextType {
  customers: Customer[];
  payments: Payment[];
  checklists: OpsChecklist[];
  auditLogs: AuditLog[];
  messageTemplates: MessageTemplate[];
  ensureCustomer: (name: string, whatsapp: string, email: string) => Promise<Customer>;
  updateCustomer: (id: string, data: Partial<Customer>) => Promise<void>;
  addPayment: (bookingId: string, amount: number, method: PaymentMethod, status: PaymentStatus, userId: string) => Promise<void>;
  getBookingPayments: (bookingId: string) => Payment[];
  getBookingPaymentTotal: (bookingId: string) => number;
  initBookingChecklist: (bookingId: string) => Promise<void>;
  getBookingChecklist: (bookingId: string) => OpsChecklist[];
  updateChecklistItem: (id: string, status: ChecklistStatus, userId?: string) => Promise<void>;
  addAuditLog: (entityType: string, entityId: string, action: string, userId: string, oldVal?: string, newVal?: string) => Promise<void>;
  updateTemplate: (id: string, text: string) => Promise<void>;
  renderTemplate: (key: string, vars: Record<string, string>) => string;
}

const DataContext = createContext<DataContextType | null>(null);

export const useData = () => {
  const ctx = useContext(DataContext);
  if (!ctx) throw new Error('useData must be used within DataProvider');
  return ctx;
};

export const DataProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { tenantId } = useAuth();
  const queryClient = useQueryClient();

  // Customers
  const { data: dbCustomers = [] } = useQuery({
    queryKey: ['customers', tenantId],
    queryFn: async () => {
      if (!tenantId) return [];
      const { data } = await supabase.from('customers').select('*').eq('tenant_id', tenantId);
      return data || [];
    },
    enabled: !!tenantId,
  });

  const customers: Customer[] = useMemo(() => dbCustomers.map(c => ({
    id: c.id,
    name: c.name,
    whatsapp: c.whatsapp,
    email: c.email || '',
    notes_internal: c.notes_internal || '',
  })), [dbCustomers]);

  // Payments
  const { data: dbPayments = [] } = useQuery({
    queryKey: ['payments', tenantId],
    queryFn: async () => {
      if (!tenantId) return [];
      const { data } = await supabase.from('payments').select('*').eq('tenant_id', tenantId);
      return data || [];
    },
    enabled: !!tenantId,
  });

  const payments: Payment[] = useMemo(() => dbPayments.map(p => ({
    id: p.id,
    booking_id: p.booking_id,
    amount: Number(p.amount),
    method: paymentMethodFromDb[p.method],
    status: paymentStatusFromDb[p.status],
    receipt_url: p.receipt_url,
    created_at: p.created_at,
    created_by_user_id: p.created_by_user_id || '',
  })), [dbPayments]);

  // Checklists
  const { data: dbChecklists = [] } = useQuery({
    queryKey: ['checklists', tenantId],
    queryFn: async () => {
      if (!tenantId) return [];
      const { data } = await supabase.from('ops_checklists').select('*').eq('tenant_id', tenantId);
      return data || [];
    },
    enabled: !!tenantId,
  });

  const checklists: OpsChecklist[] = useMemo(() => dbChecklists.map(c => ({
    id: c.id,
    booking_id: c.booking_id,
    item_key: c.item_key,
    item_label: c.item_label,
    status: checklistStatusFromDb[c.status],
    assigned_user_id: c.assigned_user_id,
    updated_at: c.updated_at,
  })), [dbChecklists]);

  // Audit logs
  const { data: dbAuditLogs = [] } = useQuery({
    queryKey: ['audit-logs', tenantId],
    queryFn: async () => {
      if (!tenantId) return [];
      const { data } = await supabase.from('audit_logs').select('*').eq('tenant_id', tenantId).order('created_at', { ascending: false }).limit(100);
      return data || [];
    },
    enabled: !!tenantId,
  });

  const auditLogs: AuditLog[] = useMemo(() => dbAuditLogs.map(l => ({
    id: l.id,
    entity_type: l.entity_type,
    entity_id: l.entity_id,
    action: l.action,
    old_value_json: l.old_value_json,
    new_value_json: l.new_value_json,
    user_id: l.user_id || '',
    created_at: l.created_at,
  })), [dbAuditLogs]);

  // Message templates
  const { data: dbTemplates = [] } = useQuery({
    queryKey: ['templates', tenantId],
    queryFn: async () => {
      if (!tenantId) return [];
      const { data } = await supabase.from('message_templates').select('*').eq('tenant_id', tenantId);
      return data || [];
    },
    enabled: !!tenantId,
  });

  const messageTemplates: MessageTemplate[] = useMemo(() => dbTemplates.map(t => ({
    id: t.id,
    key: t.key,
    title: t.title,
    template_text: t.template_text,
  })), [dbTemplates]);

  const invalidate = useCallback((key: string) => {
    queryClient.invalidateQueries({ queryKey: [key] });
  }, [queryClient]);

  const ensureCustomer = useCallback(async (name: string, whatsapp: string, email: string): Promise<Customer> => {
    if (!tenantId) throw new Error('Tenant não definido');
    const normalizedPhone = whatsapp.replace(/\D/g, '');
    const existing = customers.find(c => c.whatsapp.replace(/\D/g, '') === normalizedPhone);
    if (existing) return existing;

    const { data, error } = await supabase.from('customers').insert({
      tenant_id: tenantId,
      name,
      whatsapp,
      email,
    }).select().single();

    if (error) throw error;
    invalidate('customers');
    return { id: data.id, name: data.name, whatsapp: data.whatsapp, email: data.email || '', notes_internal: data.notes_internal || '' };
  }, [tenantId, customers, invalidate]);

  const updateCustomer = useCallback(async (id: string, data: Partial<Customer>) => {
    await supabase.from('customers').update(data).eq('id', id);
    invalidate('customers');
  }, [invalidate]);

  const addPayment = useCallback(async (bookingId: string, amount: number, method: PaymentMethod, status: PaymentStatus, userId: string) => {
    if (!tenantId) return;
    await supabase.from('payments').insert({
      tenant_id: tenantId,
      booking_id: bookingId,
      amount,
      method: paymentMethodToDb[method],
      status: paymentStatusToDb[status],
      created_by_user_id: userId,
    });
    invalidate('payments');
  }, [tenantId, invalidate]);

  const getBookingPayments = useCallback((bookingId: string) => {
    return payments.filter(p => p.booking_id === bookingId);
  }, [payments]);

  const getBookingPaymentTotal = useCallback((bookingId: string) => {
    return payments.filter(p => p.booking_id === bookingId && p.status === 'Pago').reduce((sum, p) => sum + p.amount, 0);
  }, [payments]);

  const initBookingChecklist = useCallback(async (bookingId: string) => {
    if (!tenantId) return;
    const existing = checklists.filter(c => c.booking_id === bookingId);
    if (existing.length > 0) return;

    const items = DEFAULT_CHECKLIST_ITEMS.map(item => ({
      tenant_id: tenantId,
      booking_id: bookingId,
      item_key: item.key,
      item_label: item.label,
    }));
    await supabase.from('ops_checklists').insert(items);
    invalidate('checklists');
  }, [tenantId, checklists, invalidate]);

  const getBookingChecklist = useCallback((bookingId: string) => {
    return checklists.filter(c => c.booking_id === bookingId);
  }, [checklists]);

  const updateChecklistItem = useCallback(async (id: string, status: ChecklistStatus, userId?: string) => {
    const updateData: Record<string, unknown> = { status: checklistStatusToDb[status] };
    if (userId) updateData.assigned_user_id = userId;
    await supabase.from('ops_checklists').update(updateData).eq('id', id);
    invalidate('checklists');
  }, [invalidate]);

  const addAuditLog = useCallback(async (entityType: string, entityId: string, action: string, userId: string, oldVal?: string, newVal?: string) => {
    if (!tenantId) return;
    await supabase.from('audit_logs').insert({
      tenant_id: tenantId,
      entity_type: entityType,
      entity_id: entityId,
      action,
      user_id: userId,
      old_value_json: oldVal || null,
      new_value_json: newVal || null,
    });
    invalidate('audit-logs');
  }, [tenantId, invalidate]);

  const updateTemplate = useCallback(async (id: string, text: string) => {
    await supabase.from('message_templates').update({ template_text: text }).eq('id', id);
    invalidate('templates');
  }, [invalidate]);

  const renderTemplate = useCallback((key: string, vars: Record<string, string>) => {
    const tmpl = messageTemplates.find(t => t.key === key);
    if (!tmpl) return '';
    let text = tmpl.template_text;
    Object.entries(vars).forEach(([k, v]) => {
      text = text.replace(new RegExp(`\\{${k}\\}`, 'g'), v);
    });
    return text;
  }, [messageTemplates]);

  return (
    <DataContext.Provider value={{
      customers, payments, checklists, auditLogs, messageTemplates,
      ensureCustomer, updateCustomer, addPayment, getBookingPayments, getBookingPaymentTotal,
      initBookingChecklist, getBookingChecklist, updateChecklistItem,
      addAuditLog, updateTemplate, renderTemplate,
    }}>
      {children}
    </DataContext.Provider>
  );
};
