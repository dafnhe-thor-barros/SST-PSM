import urllib.request
import os

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "artigos_pdf")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

papers_to_download = [
    {
        "doi": "10.5935/0034-7140.20180003",
        "file": "Carneiro_2018_Terceirizacao_Impacto_Acidentes_Doencas_RBE.pdf",
        "desc": "Carneiro (2018) - Terceirização e Impacto sobre Gravidade dos Acidentes (RBE/FGV)"
    },
    {
        "doi": "10.1590/2317-6369000044718",
        "file": "RBSO_2019_Acidentes_Fatais_Terceirizados_Petroleo.pdf",
        "desc": "RBSO (2019) - Mortalidade e Acidentes Fatais com Terceirizados no Petróleo"
    },
    {
        "doi": "10.1590/1413-81232020255.34942019",
        "file": "CSC_2020_Acidentes_Fatais_Politica_Seguranca_Petroleo.pdf",
        "desc": "Ciência & Saúde Coletiva (2020) - Análise de Política de SST e Terceirizados"
    },
    {
        "doi": "10.1590/2179-8966/2021/57853",
        "file": "Galvao_2023_Terceirizacao_Desastres_Mineracao.pdf",
        "desc": "Galvão (2023) - Terceirização e Acidentalidade nos Desastres da Mineração"
    }
]

for p in papers_to_download:
    filepath = os.path.join(DOWNLOAD_DIR, p["file"])
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"[JÁ EXISTE] {p['desc']} ({os.path.getsize(filepath)} bytes)")
        continue
    
    print(f"\n[RESOLVENDO DOI] {p['doi']} -> {p['desc']}...")
    try:
        doi_url = f"https://doi.org/{p['doi']}"
        req = urllib.request.Request(doi_url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            final_url = resp.geturl()
            print(f"  Página do artigo: {final_url}")
            
            # Formatar link do PDF para SciELO
            if "/a/" in final_url:
                base_art = final_url.split('?')[0].rstrip('/')
                pdf_url = base_art + "/?format=pdf"
            else:
                pdf_url = final_url + "?format=pdf"
            
            print(f"  Baixando PDF de: {pdf_url}")
            req_pdf = urllib.request.Request(pdf_url, headers=headers)
            with urllib.request.urlopen(req_pdf, timeout=30) as resp_pdf:
                data = resp_pdf.read()
                with open(filepath, "wb") as f:
                    f.write(data)
                print(f"  [SUCESSO] Salvo com {len(data)} bytes.")
    except Exception as e:
        print(f"  [ERRO] {e}")

print("\nProcesso concluído.")
