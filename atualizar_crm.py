import os
import glob
import re

vault_dir = "/Users/alejandrosulichin/Documents/VAULT-ALE"

def parse_client_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    
    # 1. Name
    name = ""
    for line in lines:
        if line.startswith('# '):
            name = line[2:].strip().replace('[[', '').replace(']]', '')
            break
    if not name:
        name = os.path.splitext(os.path.basename(filepath))[0]

    # 2. Link
    link_name = os.path.splitext(os.path.basename(filepath))[0]
    obsidian_link = f"[[{link_name}]]"

    # 3. Tags
    tags = re.findall(r'#[\w\-]+', content)
    
    valid_tags = {'#cliente-ativo', '#lead', '#prospecção', '#prospeccao', '#cliente-inativo', '#arquivado'}
    if not any(t in valid_tags for t in tags):
        if not re.search(r'(Tipo:|Localização:|Fase atual:)', content, re.IGNORECASE):
            return None

    # Determine status
    status = "Ativo"
    if any(t in {'#lead', '#prospecção', '#prospeccao'} for t in tags):
        status = "Lead"
    elif any(t in {'#cliente-inativo', '#arquivado', '#finalizado'} for t in tags):
        status = "Arquivado"

    # 4. Extract key-value fields
    tipo = ""
    localizacao = ""
    contato = ""
    whatsapp = ""
    email = ""
    fase_atual = ""

    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith('- '):
            line_strip = line_strip[2:]
        
        if re.match(r'^Tipo:', line_strip, re.IGNORECASE):
            tipo = re.sub(r'^Tipo:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^Segmento:', line_strip, re.IGNORECASE):
            tipo = re.sub(r'^Segmento:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^Localização:', line_strip, re.IGNORECASE):
            localizacao = re.sub(r'^Localização:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^Cidade:', line_strip, re.IGNORECASE):
            localizacao = re.sub(r'^Cidade:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^Contato:', line_strip, re.IGNORECASE):
            contato = re.sub(r'^Contato:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^Responsável:', line_strip, re.IGNORECASE):
            contato = re.sub(r'^Responsável:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^WhatsApp:', line_strip, re.IGNORECASE):
            whatsapp = re.sub(r'^WhatsApp:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^Telefone:', line_strip, re.IGNORECASE):
            whatsapp = re.sub(r'^Telefone:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^phone:', line_strip, re.IGNORECASE):
            whatsapp = re.sub(r'^phone:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^E-mail:', line_strip, re.IGNORECASE):
            email = re.sub(r'^E-mail:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^Email:', line_strip, re.IGNORECASE):
            email = re.sub(r'^Email:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^Fase atual:', line_strip, re.IGNORECASE):
            fase_atual = re.sub(r'^Fase atual:\s*', '', line_strip, flags=re.IGNORECASE).strip()
        elif re.match(r'^Status:', line_strip, re.IGNORECASE):
            fase_atual = re.sub(r'^Status:\s*', '', line_strip, flags=re.IGNORECASE).strip()

    # Extract first pending task
    proximo_passo = ""
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith('- [ ]'):
            task_text = line_strip[5:].strip()
            if task_text:
                proximo_passo = task_text
                break

    # Deduce Localizacao from tags if empty
    if not localizacao:
        if '#teresina' in tags:
            localizacao = "Teresina - PI"
        elif '#eua' in tags:
            localizacao = "EUA"
        elif '#argentina' in tags:
            localizacao = "Argentina"
        elif '#brasilia' in tags:
            localizacao = "Brasília - DF"
        else:
            localizacao = "-"

    # Deduce Tipo from tags if empty
    if not tipo:
        for t in tags:
            if t not in {'#cliente-ativo', '#lead', '#prospecção', '#prospeccao', '#teresina', '#eua', '#argentina', '#brasilia'}:
                tipo = t.replace('#', '').capitalize()
                break
        if not tipo:
            tipo = "-"

    # Fallbacks
    if not contato: contato = "-"
    if not whatsapp: whatsapp = "-"
    if not email: email = "-"
    if not fase_atual:
        fase_atual = "Em Prospecção" if status == "Lead" else ("Ativo" if status == "Ativo" else "Arquivado")

    return {
        'name': name,
        'link': obsidian_link,
        'status': status,
        'tipo': tipo,
        'localizacao': localizacao,
        'contato': contato,
        'whatsapp': whatsapp,
        'email': email,
        'fase_atual': fase_atual,
        'proximo_passo': proximo_passo,
        'tags': " ".join(tags)
    }

def generate_card_html(item):
    tag_pills = ""
    if item['tags']:
        tag_list = item['tags'].split()
        for tag in tag_list:
            if tag in {'#cliente-ativo', '#lead', '#prospecção', '#prospeccao'}:
                continue
            tag_clean = tag.replace('#', '')
            tag_pills += f'<span style="background-color: var(--background-secondary-alt); color: var(--text-muted); font-size: 0.72em; padding: 2px 6px; border-radius: 4px; margin-right: 4px; display: inline-block;">#{tag_clean}</span>'

    # WhatsApp link formatting
    whatsapp_clean = re.sub(r'\D', '', item['whatsapp'])
    if whatsapp_clean:
        if len(whatsapp_clean) in (10, 11) and not whatsapp_clean.startswith('55'):
            whatsapp_clean = "55" + whatsapp_clean
        wa_link = f'<a href="https://wa.me/{whatsapp_clean}" style="text-decoration: none; color: var(--text-accent); font-weight: bold;">💬 {item["whatsapp"]}</a>'
    else:
        wa_link = '<span style="color: var(--text-muted);">Sem telefone</span>'

    # Next step block
    step_html = ""
    if item['proximo_passo']:
        step_html = f"""
      <div style="font-size: 0.82em; background-color: var(--background-secondary-alt); border-left: 3px solid var(--text-accent); padding: 6px 10px; margin-top: 8px; border-radius: 0 4px 4px 0; color: var(--text-normal);">
        <b>Próximo Passo:</b> {item['proximo_passo']}
      </div>"""

    card = f"""  <div style="background-color: var(--background-secondary); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); display: flex; flex-direction: column; justify-content: space-between; gap: 8px;">
    <div>
      <div style="display: flex; justify-content: space-between; align-items: start; gap: 8px;">
        <span style="font-size: 1.15em; font-weight: bold; color: var(--text-normal);">{item['link']}</span>
        <span style="background-color: var(--background-secondary-alt); color: var(--text-accent); padding: 2px 6px; border-radius: 4px; font-size: 0.75em; font-weight: bold; border: 1px solid var(--border-color);">{item['fase_atual']}</span>
      </div>
      <div style="margin-top: 4px; margin-bottom: 8px; min-height: 18px;">{tag_pills}</div>
      <div style="font-size: 0.88em; line-height: 1.4; color: var(--text-normal);">
        <b>Segmento:</b> {item['tipo']}<br>
        <b>Localização:</b> {item['localizacao']}<br>
        <b>Contato:</b> {item['contato']}
      </div>
      {step_html}
    </div>
    <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--border-color); font-size: 0.85em; display: flex; justify-content: space-between; align-items: center;">
      <span>{wa_link}</span>
      <span style="font-size: 0.8em; color: var(--text-muted);">{item['email'] if item['email'] != '-' else ''}</span>
    </div>
  </div>"""
    return card

def main():
    search_path = os.path.join(vault_dir, "P-PROJETOS/*/*.md")
    files = glob.glob(search_path)
    
    leads = []
    ativos = []
    arquivados = []

    for f in files:
        client_data = parse_client_file(f)
        if client_data:
            if client_data['status'] == 'Lead':
                leads.append(client_data)
            elif client_data['status'] == 'Ativo':
                ativos.append(client_data)
            else:
                arquivados.append(client_data)

    leads.sort(key=lambda x: x['name'])
    ativos.sort(key=lambda x: x['name'])
    arquivados.sort(key=lambda x: x['name'])

    crm_path = os.path.join(vault_dir, "CRM.md")
    with open(crm_path, 'w', encoding='utf-8') as f:
        f.write("# 🗂️ CRM — Quadro Geral de Leads e Clientes\n\n")
        
        # 1. Statistics Cards
        f.write("## 📊 Painel de Desempenho\n")
        f.write('<div style="display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap;">\n')
        
        f.write(f"""  <div style="flex: 1; min-width: 140px; background-color: var(--background-secondary); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.01);">
    <div style="font-size: 2.2em; font-weight: bold; color: var(--text-accent); line-height: 1.1;">{len(leads)}</div>
    <div style="font-size: 0.85em; color: var(--text-muted); font-weight: bold; margin-top: 4px;">🎯 Leads / Prospecções</div>
  </div>\n""")
        
        f.write(f"""  <div style="flex: 1; min-width: 140px; background-color: var(--background-secondary); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.01);">
    <div style="font-size: 2.2em; font-weight: bold; color: #2ecc71; line-height: 1.1;">{len(ativos)}</div>
    <div style="font-size: 0.85em; color: var(--text-muted); font-weight: bold; margin-top: 4px;">🟢 Clientes Ativos</div>
  </div>\n""")
        
        f.write(f"""  <div style="flex: 1; min-width: 140px; background-color: var(--background-secondary); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.01);">
    <div style="font-size: 2.2em; font-weight: bold; color: var(--text-muted); line-height: 1.1;">{len(arquivados)}</div>
    <div style="font-size: 0.85em; color: var(--text-muted); font-weight: bold; margin-top: 4px;">📦 Arquivados / Histórico</div>
  </div>\n""")
        
        f.write('</div>\n\n')
        f.write("---\n\n")

        # Grid layouts helper
        grid_start = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 16px; margin-top: 12px; margin-bottom: 24px;">\n'
        grid_end = '</div>\n\n'

        # 2. Leads Section
        f.write("## 🎯 1. Leads e Prospecções\n")
        if leads:
            f.write(grid_start)
            for item in leads:
                f.write(generate_card_html(item) + "\n")
            f.write(grid_end)
        else:
            f.write("*Nenhum lead em prospecção no momento.*\n\n")

        # 3. Active Clients Section
        f.write("## 🟢 2. Clientes Ativos\n")
        if ativos:
            f.write(grid_start)
            for item in ativos:
                f.write(generate_card_html(item) + "\n")
            f.write(grid_end)
        else:
            f.write("*Nenhum cliente ativo no momento.*\n\n")

        # 4. Archived Section
        f.write("## 📦 3. Clientes Arquivados / Histórico\n")
        if arquivados:
            f.write(grid_start)
            for item in arquivados:
                f.write(generate_card_html(item) + "\n")
            f.write(grid_end)
        else:
            f.write("*Nenhum cliente arquivado no momento.*\n\n")

        f.write("---\n")
        f.write("*Este painel é atualizado dinamicamente a partir das notas em `P-PROJETOS` rodando o script `./atualizar_crm.sh`.*\n")

if __name__ == "__main__":
    main()
