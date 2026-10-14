import urllib.request
import re
import os
import json

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "artigos_pdf")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def download_file(url, filename, desc):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"[JÁ EXISTE] {desc} ({os.path.getsize(filepath)} bytes)")
        return True
    
    print(f"[BAIXANDO] {desc}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp, open(filepath, "wb") as f:
            f.write(resp.read())
        size = os.path.getsize(filepath)
        print(f"[SUCESSO] {filename} salvo com {size} bytes.")
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao baixar {desc}: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False

# 1. Artigos com URLs diretas conhecidas
direct_downloads = [
    {
        "url": "https://www.scielo.br/j/csp/a/n9YJ9gXknCxXCpBztHLB9LG/?format=pdf",
        "file": "Vilela_2004_Culpa_da_Vitima_Acidentes_SciELO.pdf",
        "desc": "Vilela et al. (2004) - Culpa da Vítima e Análise de Acidentes (CSP/SciELO)"
    },
    {
        "url": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/nr-01-atualizada-2025-i-1.pdf",
        "file": "NR_01_Atualizada_MTE_GRO_PGR.pdf",
        "desc": "Norma Regulamentadora nº 01 Oficial Atualizada (MTE/Gov.br)"
    },
    {
        "url": "https://www.cpwr.com/wp-content/uploads/publications/Safety-Climate-Leading-Indicators-Workbook.pdf",
        "file": "CPWR_Safety_Climate_Leading_Indicators_Workbook.pdf",
        "desc": "CPWR - Strengthening Jobsite Safety Climate: 8 Leading Indicators"
    },
    {
        "url": "https://www.cpwr.com/wp-content/uploads/2020/06/Safety_Climate_Indicator8_Owner-Client-Involvement.pdf",
        "file": "CPWR_Indicator8_Owner_Client_Involvement.pdf",
        "desc": "CPWR - Indicator 8: Owner/Client Involvement in Safety Climate"
    },
    {
        "url": "https://www.cpwr.com/wp-content/uploads/2020/06/Safety_Climate_Indicator2_Aligning-Integrating-Safety.pdf",
        "file": "CPWR_Indicator2_Aligning_Integrating_Safety_as_Value.pdf",
        "desc": "CPWR - Indicator 2: Aligning and Integrating Safety as a Value"
    }
]

for item in direct_downloads:
    download_file(item["url"], item["file"], item["desc"])

# 2. Buscar e baixar artigos do SciELO (ex: Lima & Oliveira na RBSO)
queries = [
    ("Precarizacao e acidentes de trabalho os riscos da terceirizacao no setor eletrico", "Lima_Oliveira_Terceirizacao_Setor_Eletrico_RBSO.pdf", "Lima & Oliveira - Terceirização e Acidentes no Setor Elétrico"),
    ("A Terceirizacao Precariza as Relacoes de Trabalho Acidentes", "Terceirizacao_Acidentes_Doencas_SciELO.pdf", "Estudo Empírico Terceirização e Acidentes"),
    ("Superexploracao acidentalidade e terceirizacao nos desastres da mineracao", "Terceirizacao_Desastres_Mineracao_SciELO.pdf", "Terceirização e Desastres na Mineração")
]

for q, fname, desc in queries:
    print(f"\n[BUSCANDO NO SCIELO] {desc}...")
    try:
        search_url = f"https://search.scielo.org/?q={urllib.parse.quote(q)}&lang=pt"
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        # Encontrar links para artigos
        article_matches = re.findall(r'href=[\"\'](https://www.scielo.br/j/[a-z0-9]+/a/[A-Za-z0-9]+/[^\"\']*)[\"\']', html)
        if article_matches:
            target_art = article_matches[0].split('?')[0].rstrip('/') + '/?format=pdf'
            print(f"  URL encontrada: {target_art}")
            download_file(target_art, fname, desc)
        else:
            print(f"  Nenhum link direto em PDF encontrado para a busca.")
    except Exception as e:
        print(f"  Erro na busca SciELO: {e}")
