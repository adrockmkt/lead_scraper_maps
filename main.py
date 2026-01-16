import os
from dotenv import load_dotenv

from config import (
    NICHOS_ALTO_TICKET,
    CIDADE_PRINCIPAL,
    CIDADES_ADICIONAIS
)

from services.places_client import GooglePlacesClient
from services.site_crawler import SiteCrawler
from services.scoring import LeadScorer
from services.storage import Storage

# ======================================================
# BOOTSTRAP
# ======================================================

load_dotenv()

USER_AGENT = os.getenv("USER_AGENT")
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH")

if not USER_AGENT:
    raise RuntimeError("USER_AGENT não definido no .env")

if not SQLITE_DB_PATH:
    raise RuntimeError("SQLITE_DB_PATH não definido no .env")

# ======================================================
# MAIN PIPELINE
# ======================================================

def main():
    print("▶ Iniciando Lead Scraper Maps (Grupo 3)")

    places_client = GooglePlacesClient()
    crawler = SiteCrawler(user_agent=USER_AGENT)
    scorer = LeadScorer()
    storage = Storage(db_path=SQLITE_DB_PATH)

    total_processados = 0
    total_qualificados = 0
    total_sem_email = 0
    total_descartados = 0

    for nicho in NICHOS_ALTO_TICKET:
        print(f"\n=== Nicho: {nicho.upper()} ===")

        leads_maps = places_client.coletar_por_nicho(nicho)
        print(f"Encontrados {len(leads_maps)} registros únicos no Maps")

        # proxy simples de concorrência
        concorrencia_nicho = len(leads_maps)

        for lead in leads_maps:
            place_id = lead.get("place_id")

            if storage.lead_exists(place_id):
                continue

            # enriquecer com details
            lead = places_client.enriquecer_lead(lead)

            lead.update({
                "nicho": nicho,
                "cidade": CIDADE_PRINCIPAL,
                "concorrencia": concorrencia_nicho
            })

            site = lead.get("site")

            # crawling do site (se existir e ainda não foi crawleado)
            email_corporativo = None

            if site and not storage.site_crawled(site):
                crawl_result = crawler.crawl_site(site)

                emails_corp = crawl_result.get("emails_corporativos", [])
                if emails_corp:
                    email_corporativo = emails_corp[0]

                storage.mark_site_crawled(site)

            lead["email_corporativo"] = email_corporativo

            # scoring
            lead = scorer.calcular_score(lead)

            # persistência
            storage.save_lead(lead)
            storage.export_csv(lead)

            # métricas
            total_processados += 1

            if lead["status"] == "qualificado":
                total_qualificados += 1
            elif lead["status"] == "sem_email":
                total_sem_email += 1
            else:
                total_descartados += 1

    # ==================================================
    # RESUMO FINAL
    # ==================================================
    print("\n====== RESUMO DA EXECUÇÃO ======")
    print(f"Leads processados: {total_processados}")
    print(f"Qualificados: {total_qualificados}")
    print(f"Sem email corporativo: {total_sem_email}")
    print(f"Descartados: {total_descartados}")
    print("Arquivos CSV gerados em /outputs")
    print("Execução finalizada.")

# ======================================================
# ENTRYPOINT
# ======================================================

if __name__ == "__main__":
    main()