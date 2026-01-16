import os
import time
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
from tenacity import retry, wait_fixed, stop_after_attempt

from config import (
    PLACES_TEXT_SEARCH_URL,
    PLACES_DETAILS_URL,
    PLACES_DETAILS_FIELDS,
    BAIRROS_CURITIBA,
    CIDADE_PRINCIPAL,
    ESTADO,
    CIDADES_ADICIONAIS
)

# ======================================================
# ENV / CONFIG
# ======================================================

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", 1.2))
MAX_PAGES = int(os.getenv("MAX_PAGES_PER_QUERY", 2))

HEADERS = {
    "Accept": "application/json"
}

# ======================================================
# CORE CLIENT
# ======================================================

class GooglePlacesClient:
    def __init__(self):
        if not API_KEY:
            raise RuntimeError("GOOGLE_MAPS_API_KEY não encontrada no .env")

        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    # --------------------------------------------------
    # TEXT SEARCH (bairro + nicho)
    # --------------------------------------------------
    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
    def text_search(
        self,
        query: str,
        page_token: Optional[str] = None
    ) -> Dict:
        params = {
            "query": query,
            "language": "pt-BR",
            "region": "br",
            "key": API_KEY
        }

        if page_token:
            params["pagetoken"] = page_token
            # token precisa de tempo para ativar
            time.sleep(2)

        response = self.session.get(
            PLACES_TEXT_SEARCH_URL,
            params=params,
            timeout=15
        )
        response.raise_for_status()
        return response.json()

    # --------------------------------------------------
    # PLACE DETAILS (campos mínimos)
    # --------------------------------------------------
    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
    def place_details(self, place_id: str) -> Dict:
        params = {
            "place_id": place_id,
            "fields": ",".join(PLACES_DETAILS_FIELDS),
            "language": "pt-BR",
            "key": API_KEY
        }

        response = self.session.get(
            PLACES_DETAILS_URL,
            params=params,
            timeout=15
        )
        response.raise_for_status()
        return response.json()

    # --------------------------------------------------
    # BUSCA COMPLETA POR NICHO + LOCAL
    # --------------------------------------------------
    def search_by_nicho_and_local(
        self,
        nicho: str,
        cidade: str,
        bairro: Optional[str] = None
    ) -> List[Dict]:
        resultados = []
        page_token = None
        page_count = 0

        if bairro:
            query = f"{nicho} {bairro}, {cidade} {ESTADO}"
        else:
            query = f"{nicho} {cidade} {ESTADO}"

        while page_count < MAX_PAGES:
            data = self.text_search(query=query, page_token=page_token)

            for item in data.get("results", []):
                resultados.append({
                    "place_id": item.get("place_id"),
                    "nome": item.get("name"),
                    "categorias": item.get("types", []),
                    "endereco": item.get("formatted_address"),
                    "rating": item.get("rating"),
                    "user_ratings_total": item.get("user_ratings_total", 0),
                    "query_origem": query
                })

            page_token = data.get("next_page_token")
            page_count += 1

            if not page_token:
                break

            time.sleep(REQUEST_DELAY)

        return resultados

    # --------------------------------------------------
    # PIPELINE PRINCIPAL DE COLETA
    # --------------------------------------------------
    def coletar_por_nicho(self, nicho: str) -> List[Dict]:
        leads = []

        # Curitiba por bairros
        for bairro in BAIRROS_CURITIBA:
            print(f"[Maps] Buscando '{nicho}' em {bairro} / {CIDADE_PRINCIPAL}")
            leads.extend(
                self.search_by_nicho_and_local(
                    nicho=nicho,
                    cidade=CIDADE_PRINCIPAL,
                    bairro=bairro
                )
            )

        # Região metropolitana (sem bairro)
        for cidade in CIDADES_ADICIONAIS:
            print(f"[Maps] Buscando '{nicho}' em {cidade}")
            leads.extend(
                self.search_by_nicho_and_local(
                    nicho=nicho,
                    cidade=cidade
                )
            )

        # Deduplicação por place_id
        unique = {}
        for lead in leads:
            pid = lead.get("place_id")
            if pid and pid not in unique:
                unique[pid] = lead

        return list(unique.values())

    # --------------------------------------------------
    # ENRIQUECIMENTO COM DETAILS
    # --------------------------------------------------
    def enriquecer_lead(self, lead: Dict) -> Dict:
        place_id = lead.get("place_id")
        if not place_id:
            return lead

        details = self.place_details(place_id).get("result", {})

        lead.update({
            "telefone": details.get("formatted_phone_number"),
            "site": details.get("website"),
            "geometry": details.get("geometry"),
            "address_components": details.get("address_components", [])
        })

        time.sleep(REQUEST_DELAY)
        return lead