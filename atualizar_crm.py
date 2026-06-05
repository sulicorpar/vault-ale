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
    # Obsidian link format: [[Name]]
    obsidian_link = f"[[{link_name}]]"

    # 3. Tags
    # Find all tags in the format #tag-name
    tags = re.findall(r'#[\w\-]+', content)
    
    # Check if this is a valid client file
    valid_tags = {'#cliente-ativo', '#lead', '#prospecção', '#prospeccao', '#cliente-inativo', '#arquivado'}
    if not any(t in valid_tags for t in tags):
        # Double check if it has Tipo: or Localização: or Fase atual:
        if not re.search(r'(Tipo:|Localização:|Fase atual:)', content, re.IGNORECASE):
            return None

    # Determine status/phase
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
        # Remove markdown list bullet if present
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
        'tags': " ".join(tags)
    }

def main():
    search_path = os.path.join(vault_dir, "P-PROJETOS/*/*.md")
    files = glob.glob(search_path)
    
    leads = []
    ativos = []
    arquivados = []

    for f in files:
        # Skip sub-folders by verifying depth or location
        client_data = parse_client_file(f)
        if client_data:
            if client_data['status'] == 'Lead':
                leads.append(client_data)
            elif client_data['status'] == 'Ativo':
                ativos.append(client_data)
            else:
                arquivados.append(client_data)

    # Sort lists by name
    leads.sort(key=lambda x: x['name'])
    ativos.sort(key=lambda x: x['name'])
    arquivados.sort(key=lambda x: x['name'])

    # Write CRM.md
    crm_path = os.path.join(vault_dir, "CRM.md")
    with open(crm_path, 'w', encoding='utf-8') as f:
        f.write("# 🗂️ CRM — Quadro Geral de Leads e Clientes\n\n")
        
        f.write("## 📊 Estatísticas Rápidas\n")
        f.write(f"- 🎯 **Leads em Prospecção:** {len(leads)}\n")
        f.write(f"- 🟢 **Clientes Ativos:** {len(ativos)}\n")
        f.write(f"- 📦 **Clientes Arquivados:** {len(arquivados)}\n\n")
        
        f.write("---\n\n")
        
        f.write("## 🎯 1. Leads e Prospecções\n")
        if leads:
            f.write("| Cliente | Segmento | Localização | Contato | WhatsApp | Fase Atual |\n")
            f.write("| --- | --- | --- | --- | --- | --- |\n")
            for item in leads:
                f.write(f"| {item['link']} | {item['tipo']} | {item['localizacao']} | {item['contato']} | {item['whatsapp']} | {item['fase_atual']} |\n")
        else:
            f.write("*Nenhum lead em prospecção no momento.*\n")
        f.write("\n")

        f.write("## 🟢 2. Clientes Ativos\n")
        if ativos:
            f.write("| Cliente | Segmento | Localização | Contato | WhatsApp | Tags |\n")
            f.write("| --- | --- | --- | --- | --- | --- |\n")
            for item in ativos:
                f.write(f"| {item['link']} | {item['tipo']} | {item['localizacao']} | {item['contato']} | {item['whatsapp']} | `{item['tags']}` |\n")
        else:
            f.write("*Nenhum cliente ativo no momento.*\n")
        f.write("\n")

        f.write("## 📦 3. Clientes Arquivados / Histórico\n")
        if arquivados:
            f.write("| Cliente | Segmento | Localização | Contato | Tags |\n")
            f.write("| --- | --- | --- | --- | --- |\n")
            for item in arquivados:
                f.write(f"| {item['link']} | {item['tipo']} | {item['localizacao']} | {item['contato']} | `{item['tags']}` |\n")
        else:
            f.write("*Nenhum cliente arquivado no momento.*\n")
        f.write("\n\n---\n")
        f.write("*Este quadro é gerado automaticamente a partir das notas em `P-PROJETOS` rodando o script `./atualizar_crm.sh`.*\n")

    print(f"CRM atualizado com sucesso! {len(leads)} leads, {len(ativos)} ativos, {len(arquivados)} arquivados.")

if __name__ == "__main__":
    main()
