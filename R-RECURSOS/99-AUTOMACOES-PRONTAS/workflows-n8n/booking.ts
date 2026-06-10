export type Shift = 'Manhã' | 'Tarde' | 'Noite';
export type BookingStatus = 'Pendente' | 'Confirmada' | 'Cancelada';
export type UserRole = 'ADMIN' | 'ATENDENTE' | 'FINANCEIRO' | 'OPERACIONAL';
export type PaymentStatus = 'Aguardando' | 'Pago' | 'Parcial';
export type PaymentMethod = 'PIX' | 'Cartão' | 'Boleto' | 'Dinheiro' | 'Transferência';
export type ChecklistStatus = 'Pendente' | 'Em andamento' | 'Concluído';

export interface Venue {
  id: string;
  name: string;
  address: string;
  capacity: number;
  base_price: number;
  rules: string;
  photos: string[];
}

export interface AppUser {
  id: string;
  name: string;
  email: string;
  role: UserRole;
}

export interface Customer {
  id: string;
  name: string;
  whatsapp: string;
  email: string;
  notes_internal: string;
}

export interface Booking {
  id: string;
  venue_id: string;
  customer_id: string;
  customer_name: string;
  whatsapp: string;
  email: string;
  event_type: string;
  guests: number;
  date: string;
  shift: Shift;
  total_price: number;
  status: BookingStatus;
  created_at: string;
  observations: string;
  responsible_user_id: string | null;
  google_event_id: string | null;
  notes_internal: string;
}

export interface BlockedShift {
  id: string;
  venue_id: string;
  date: string;
  shift: Shift;
  reason: string;
  created_by_user_id: string | null;
}

export interface Payment {
  id: string;
  booking_id: string;
  amount: number;
  method: PaymentMethod;
  status: PaymentStatus;
  receipt_url: string | null;
  created_at: string;
  created_by_user_id: string;
}

export interface OpsChecklist {
  id: string;
  booking_id: string;
  item_key: string;
  item_label: string;
  status: ChecklistStatus;
  assigned_user_id: string | null;
  updated_at: string;
}

export interface MessageTemplate {
  id: string;
  key: string;
  title: string;
  template_text: string;
}

export interface AuditLog {
  id: string;
  entity_type: string;
  entity_id: string;
  action: string;
  old_value_json: string | null;
  new_value_json: string | null;
  user_id: string;
  created_at: string;
}

export interface PricingRule {
  id: string;
  venue_id: string;
  weekend_extra: number;
  shift_extras: Record<Shift, number>;
}

export const SHIFTS: Shift[] = ['Manhã', 'Tarde', 'Noite'];

export const SHIFT_TIMES: Record<Shift, { start: string; end: string }> = {
  'Manhã': { start: '08:00', end: '12:00' },
  'Tarde': { start: '14:00', end: '18:00' },
  'Noite': { start: '19:00', end: '23:59' },
};

export const EVENT_TYPES = [
  'Aniversário',
  'Casamento',
  'Formatura',
  'Confraternização',
  'Chá de bebê',
  'Evento corporativo',
  'Outro',
];

export const PAYMENT_METHODS: PaymentMethod[] = ['PIX', 'Cartão', 'Boleto', 'Dinheiro', 'Transferência'];

export const DEFAULT_CHECKLIST_ITEMS = [
  { key: 'limpeza_pre', label: 'Limpeza pré-evento' },
  { key: 'mesas_cadeiras', label: 'Organização de mesas e cadeiras' },
  { key: 'som', label: 'Configuração de som' },
  { key: 'iluminacao', label: 'Verificação de iluminação' },
  { key: 'chaves', label: 'Entrega de chaves' },
  { key: 'vistoria_entrada', label: 'Vistoria de entrada' },
  { key: 'vistoria_saida', label: 'Vistoria de saída' },
  { key: 'limpeza_pos', label: 'Limpeza pós-evento' },
];
