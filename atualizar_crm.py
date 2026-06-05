import os
import glob
import re
import urllib.parse

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

    # 2. Link for Obsidian
    link_name = os.path.splitext(os.path.basename(filepath))[0]
    obsidian_link = f"[[{link_name}]]"

    # 3. Obsidian Deep Link URI
    # Relative path from vault root (e.g. P-PROJETOS/Natusa/Natusa.md)
    rel_path = os.path.relpath(filepath, vault_dir)
    rel_path_no_ext = os.path.splitext(rel_path)[0]
    obsidian_uri = f"obsidian://open?vault=VAULT-ALE&file={urllib.parse.quote(rel_path_no_ext)}"

    # 4. Tags
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

    # 5. Extract key-value fields
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
        'uri': obsidian_uri,
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

def generate_markdown_card(item):
    tag_pills = ""
    if item['tags']:
        tag_list = item['tags'].split()
        for tag in tag_list:
            if tag in {'#cliente-ativo', '#lead', '#prospecção', '#prospeccao'}:
                continue
            tag_clean = tag.replace('#', '')
            tag_pills += f'<span style="background-color: var(--background-secondary-alt); color: var(--text-muted); font-size: 0.72em; padding: 2px 6px; border-radius: 4px; margin-right: 4px; display: inline-block;">#{tag_clean}</span>'

    whatsapp_clean = re.sub(r'\D', '', item['whatsapp'])
    if whatsapp_clean:
        if len(whatsapp_clean) in (10, 11) and not whatsapp_clean.startswith('55'):
            whatsapp_clean = "55" + whatsapp_clean
        wa_link = f'<a href="https://wa.me/{whatsapp_clean}" style="text-decoration: none; color: var(--text-accent); font-weight: bold;">💬 {item["whatsapp"]}</a>'
    else:
        wa_link = '<span style="color: var(--text-muted);">Sem telefone</span>'

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

def generate_html_card(item):
    tag_pills = ""
    if item['tags']:
        tag_list = item['tags'].split()
        for tag in tag_list:
            if tag in {'#cliente-ativo', '#lead', '#prospecção', '#prospeccao'}:
                continue
            tag_clean = tag.replace('#', '')
            tag_pills += f'<span class="tag">#{tag_clean}</span>'

    whatsapp_clean = re.sub(r'\D', '', item['whatsapp'])
    if whatsapp_clean:
        if len(whatsapp_clean) in (10, 11) and not whatsapp_clean.startswith('55'):
            whatsapp_clean = "55" + whatsapp_clean
        wa_button = f'<a href="https://wa.me/{whatsapp_clean}" target="_blank" class="wa-btn">💬 WhatsApp</a>'
    else:
        wa_button = '<span style="color: var(--text-muted); font-size: 0.85rem;">Sem telefone</span>'

    step_html = ""
    if item['proximo_passo']:
        step_html = f"""
        <div class="step-box">
            <b>Próximo Passo:</b> {item['proximo_passo']}
        </div>"""

    badge_class = "badge-active"
    if item['status'] == 'Lead':
        badge_class = "badge-lead"
    elif item['status'] == 'Arquivado':
        badge_class = "badge-archive"

    card = f"""        <div class="card" data-status="{item['status'].lower()}">
            <div>
                <div class="card-header">
                    <h3 class="card-title">
                        <a href="{item['uri']}" style="color: inherit; text-decoration: none;" title="Abrir no Obsidian">
                            🔗 {item['name']}
                        </a>
                    </h3>
                    <span class="badge {badge_class}">{item['fase_atual']}</span>
                </div>
                <div class="tags">{tag_pills}</div>
                <div class="details">
                    <b>Segmento:</b> {item['tipo']}<br>
                    <b>Localização:</b> {item['localizacao']}<br>
                    <b>Contato:</b> {item['contato']}
                </div>
                {step_html}
            </div>
            <div class="card-footer">
                {wa_button}
                <span class="email-text" title="{item['email']}">{item['email'] if item['email'] != '-' else ''}</span>
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

    # ------------------
    # 1. WRITE CRM.md (for Obsidian)
    # ------------------
    crm_path = os.path.join(vault_dir, "CRM.md")
    with open(crm_path, 'w', encoding='utf-8') as f:
        f.write("# 🗂️ CRM — Quadro Geral de Leads e Clientes\n\n")
        
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

        grid_start = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 16px; margin-top: 12px; margin-bottom: 24px;">\n'
        grid_end = '</div>\n\n'

        f.write("## 🎯 1. Leads e Prospecções\n")
        if leads:
            f.write(grid_start)
            for item in leads:
                f.write(generate_markdown_card(item) + "\n")
            f.write(grid_end)
        else:
            f.write("*Nenhum lead em prospecção no momento.*\n\n")

        f.write("## 🟢 2. Clientes Ativos\n")
        if ativos:
            f.write(grid_start)
            for item in ativos:
                f.write(generate_markdown_card(item) + "\n")
            f.write(grid_end)
        else:
            f.write("*Nenhum cliente ativo no momento.*\n\n")

        f.write("## 📦 3. Clientes Arquivados / Histórico\n")
        if arquivados:
            f.write(grid_start)
            for item in arquivados:
                f.write(generate_markdown_card(item) + "\n")
            f.write(grid_end)
        else:
            f.write("*Nenhum cliente arquivado no momento.*\n\n")

        f.write("---\n")
        f.write("*Este painel é atualizado dinamicamente a partir das notas em `P-PROJETOS` rodando o script `./atualizar_crm.sh`.*\n")

    # ------------------
    # 2. WRITE crm.html (for Web browser and hosting)
    # ------------------
    html_path = os.path.join(vault_dir, "crm.html")
    
    all_clients = leads + ativos + arquivados
    all_cards_html = "\n".join(generate_html_card(item) for item in all_clients)

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CRM — Painel Geral de Clientes</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --border-color: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-color: #8b5cf6;
            --accent-hover: #7c3aed;
            --lead-color: #f59e0b;
            --active-color: #10b981;
            --archive-color: #64748b;
        }}
        
        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}

        .container {{
            max-width: 1200px;
            width: 100%;
        }}

        header {{
            margin-bottom: 32px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 24px;
        }}

        .header-title-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}

        h1 {{
            font-size: 2.2rem;
            margin: 0;
            background: linear-gradient(to right, #a78bfa, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }}

        .last-update {{
            color: var(--text-muted);
            font-size: 0.85rem;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }}

        .stat-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}

        .stat-val {{
            font-size: 2.8rem;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 8px;
        }}

        .stat-val.leads {{ color: var(--lead-color); }}
        .stat-val.active {{ color: var(--active-color); }}
        .stat-val.archived {{ color: var(--text-muted); }}

        .stat-label {{
            color: var(--text-muted);
            font-size: 0.95rem;
            font-weight: 600;
        }}

        .controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .search-wrapper {{
            position: relative;
            flex-grow: 1;
            max-width: 400px;
        }}

        .search-input {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px 16px;
            color: var(--text-main);
            width: 100%;
            font-size: 0.95rem;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}

        .search-input:focus {{
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.25);
        }}

        .filter-btn-group {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 20px;
            color: var(--text-muted);
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.2s;
        }}

        .filter-btn.active, .filter-btn:hover {{
            background-color: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
            box-shadow: 0 4px 6px -1px rgba(139, 92, 246, 0.2);
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 24px;
        }}

        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.3);
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 12px;
            gap: 12px;
        }}

        .card-title {{
            font-size: 1.3rem;
            font-weight: 700;
            margin: 0;
            color: var(--text-main);
        }}
        
        .card-title a:hover {{
            text-decoration: underline;
        }}

        .badge {{
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 8px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }}

        .badge-lead {{ background-color: rgba(245, 158, 11, 0.15); color: var(--lead-color); border: 1px solid rgba(245, 158, 11, 0.3); }}
        .badge-active {{ background-color: rgba(16, 185, 129, 0.15); color: var(--active-color); border: 1px solid rgba(16, 185, 129, 0.3); }}
        .badge-archive {{ background-color: rgba(148, 163, 184, 0.15); color: var(--text-muted); border: 1px solid rgba(148, 163, 184, 0.3); }}

        .tags {{
            margin-bottom: 16px;
            min-height: 24px;
        }}

        .tag {{
            background-color: rgba(148, 163, 184, 0.1);
            color: var(--text-muted);
            font-size: 0.75rem;
            padding: 4px 8px;
            border-radius: 4px;
            margin-right: 6px;
            margin-bottom: 6px;
            display: inline-block;
            font-weight: 500;
        }}

        .details {{
            font-size: 0.92rem;
            line-height: 1.6;
            color: var(--text-muted);
            margin-bottom: 16px;
        }}

        .details b {{
            color: var(--text-main);
        }}

        .step-box {{
            background-color: rgba(139, 92, 246, 0.05);
            border-left: 3px solid var(--accent-color);
            padding: 10px 14px;
            border-radius: 0 8px 8px 0;
            margin-top: 14px;
            font-size: 0.88rem;
            color: var(--text-main);
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.2);
        }}

        .card-footer {{
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.88rem;
        }}

        .wa-btn {{
            background-color: #25d366;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: background-color 0.2s, transform 0.1s;
        }}

        .wa-btn:hover {{
            background-color: #20ba5a;
            transform: scale(1.02);
        }}

        .email-text {{
            color: var(--text-muted);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 180px;
            font-size: 0.85rem;
        }}

        .hidden {{
            display: none !important;
        }}

        footer {{
            margin-top: 64px;
            border-top: 1px solid var(--border-color);
            padding-top: 24px;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-title-row">
                <h1>🗂️ CRM — Quadro de Clientes</h1>
                <div class="last-update" id="time-stamp">Atualizado via Script</div>
            </div>
        </header>

        <section class="stats-grid">
            <div class="stat-card">
                <div class="stat-val leads">{len(leads)}</div>
                <div class="stat-label">🎯 Leads / Prospecção</div>
            </div>
            <div class="stat-card">
                <div class="stat-val active">{len(ativos)}</div>
                <div class="stat-label">🟢 Clientes Ativos</div>
            </div>
            <div class="stat-card">
                <div class="stat-val archived">{len(arquivados)}</div>
                <div class="stat-label">📦 Arquivados</div>
            </div>
        </section>

        <div class="controls">
            <div class="search-wrapper">
                <input type="text" id="search-box" class="search-input" placeholder="Buscar por nome, segmento, local..." oninput="searchClients()">
            </div>
            <div class="filter-btn-group">
                <button class="filter-btn active" data-filter="all" onclick="filterClients('all')">Todos</button>
                <button class="filter-btn" data-filter="lead" onclick="filterClients('lead')">Leads</button>
                <button class="filter-btn" data-filter="ativo" onclick="filterClients('ativo')">Ativos</button>
                <button class="filter-btn" data-filter="arquivado" onclick="filterClients('arquivado')">Arquivados</button>
            </div>
        </div>

        <main class="grid">
{all_cards_html}
        </main>

        <footer>
            <p>Gerado automaticamente a partir das notas locais de <b>P-PROJETOS</b> no Obsidian.</p>
        </footer>
    </div>

    <script>
        // Set update timestamp
        const now = new Date();
        document.getElementById('time-stamp').textContent = "Última atualização: " + now.toLocaleString('pt-BR');

        function filterClients(status) {{
            // Update active button state
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.currentTarget.classList.add('active');
            
            applyFilter();
        }}

        function searchClients() {{
            applyFilter();
        }}

        function applyFilter() {{
            const activeBtn = document.querySelector('.filter-btn.active');
            const filterValue = activeBtn.getAttribute('data-filter');
            const searchVal = document.getElementById('search-box').value.toLowerCase();
            
            const cards = document.querySelectorAll('.card');
            cards.forEach(card => {{
                const cardStatus = card.getAttribute('data-status');
                const cardText = card.textContent.toLowerCase();
                
                const matchesStatus = (filterValue === 'all') || (cardStatus === filterValue);
                const matchesSearch = cardText.includes(searchVal);
                
                if (matchesStatus && matchesSearch) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
        }}
    </script>
</body>
</html>
"""
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"CRM atualizado com sucesso! {len(leads)} leads, {len(ativos)} ativos, {len(arquivados)} arquivados. Arquivo html gerado.")

if __name__ == "__main__":
    main()
