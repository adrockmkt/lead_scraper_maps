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
    CIDADES_ADICIONAIS,
    LIMITE_POR_NICHO,
    LIMITE_PADRAO_POR_NICHO,
    LIMITE_POR_BAIRRO
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
# ENHANCED CLIENT WITH DRY-RUN AND LIMITS
# ======================================================

class GooglePlacesClientEnhanced:
    def __init__(self, dry_run: bool = False, metrics_collector=None):
        if not API_KEY and not dry_run:
            raise RuntimeError("GOOGLE_MAPS_API_KEY não encontrada no .env")

        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.dry_run = dry_run
        self.metrics = metrics_collector
        
        # Controle de limites
        self.limite_por_nicho = LIMITE_POR_NICHO
        self.limite_padrao_por_nicho = LIMITE_PADRAO_POR_NICHO
        self.limite_por_bairro = LIMITE_POR_BAIRRO

    # --------------------------------------------------
    # TEXT SEARCH (com dry-run)
    # --------------------------------------------------
    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
    def text_search(
        self,
        query: str,
        page_token: Optional[str] = None
    ) -> Dict:
        if self.dry_run:
            # Simulação de resposta para dry-run
            print(f"[DRY-RUN] Simulando busca: '{query}'")
            return {
                "results": [
                    {
                        "place_id": f"mock_id_{hash(query) % 10000}",
                        "name": f"Empresa Mock {query[:20]}",
                        "types": ["point_of_interest"],
                        "formatted_address": f"Endereço Mock, {query.split(',')[-1].strip() if ',' in query else 'Curitiba PR'}",
                        "rating": 4.0,
                        "user_ratings_total": 25
                    }
                ] * 5,  # 5 resultados mock
                "next_page_token": None
            }

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
    # PLACE DETAILS (com dry-run)
    # --------------------------------------------------
    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
    def place_details(self, place_id: str) -> Dict:
        if self.dry_run:
            print(f"[DRY-RUN] Simulando detalhes para place_id: {place_id}")
            return {
                "result": {
                    "name": "Empresa Mock Detalhes",
                    "types": ["point_of_interest"],
                    "formatted_address": "Endereço Mock Completo, Curitiba - PR",
                    "address_components": [
                        {"long_name": "Curitiba", "short_name": "Curitiba", "types": ["city"]},
                        {"long_name": "PR", "short_name": "PR", "types": ["administrative_area_level_1"]}
                    ],
                    "formatted_phone_number": "(41) 9999-9999",
                    "website": "https://www.site-mock.com.br",
                    "geometry": {
                        "location": {"lat": -25.4284, "lng": -49.2733}
                    }
                }
            }

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
    # BUSCA COM CONTROLE DE LIMITES
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
        
        # Obter limites
        limite_nicho = self.limite_por_nicho.get(nicho, self.limite_padrao_por_nicho)
        limite_bairro = self.limite_por_bairro

        if bairro:
            query = f"{nicho} {bairro}, {cidade} {ESTADO}"
        else:
            query = f"{nicho} {cidade} {ESTADO}"

        print(f"🔍 Buscando '{nicho}' em {bairro or cidade} (limite: {limite_bairro if bairro else limite_nicho})")

        while page_count < MAX_PAGES and len(resultados) < (limite_bairro if bairro else limite_nicho):
            data = self.text_search(query=query, page_token=page_token)
            
            # Registrar métricas
            if self.metrics:
                self.metrics.registrar_text_search(nicho, bairro or cidade, data.get("results", []))

            novos_resultados = []
            for item in data.get("results", []):
                # Verificar limites
                if len(resultados) >= (limite_bairro if bairro else limite_nicho):
                    break
                    
                novos_resultados.append({
                    "place_id": item.get("place_id"),
                    "nome": item.get("name"),
                    "categorias": item.get("types", []),
                    "endereco": item.get("formatted_address"),
                    "rating": item.get("rating"),
                    "user_ratings_total": item.get("user_ratings_total", 0),
                    "query_origem": query
                })

            resultados.extend(novos_resultados)
            
            print(f"    +{len(novos_resultados)} resultados (total: {len(resultados)})")

            page_token = data.get("next_page_token")
            page_count += 1

            if not page_token or len(resultados) >= (limite_bairro if bairro else limite_nicho):
                break

            if not self.dry_run:
                time.sleep(REQUEST_DELAY)

        return resultados

    # --------------------------------------------------
    # PIPELINE PRINCIPAL COM CONTROLE DE LIMITES
    # --------------------------------------------------
    def coletar_por_nicho(self, nicho: str) -> List[Dict]:
        leads = []
        limite_nicho = self.limite_por_nicho.get(nicho, self.limite_padrao_por_nicho)
        
        print(f"\n🎯 Coletando leads para nicho: {nicho.upper()}")
        print(f"📊 Limite global para este nicho: {limite_nicho} leads")

        # Curitiba por bairros
        leads_curitiba = []
        for bairro in BAIRROS_CURITIBA:
            if len(leads_curitiba) >= limite_nicho:
                print(f"⚠️  Limite global do nicho atingido ({limite_nicho}), pulando bairros restantes")
                break
                
            leads_bairro = self.search_by_nicho_and_local(
                nicho=nicho,
                cidade=CIDADE_PRINCIPAL,
                bairro=bairro
            )
            
            # Controlar limite global
            espaco_restante = limite_nicho - len(leads_curitiba)
            if len(leads_bairro) > espaco_restante:
                leads_bairro = leads_bairro[:espaco_restante]
                print(f"⚠️  Ajustado para limite restante: {espaco_restante} leads")
            
            leads_curitiba.extend(leads_bairro)

        # Região metropolitana (se ainda houver espaço)
        leads_rmc = []
        if len(leads_curitiba) < limite_nicho:
            espaco_restante = limite_nicho - len(leads_curitiba)
            print(f"🏘️  Coletando da RMC (espaço restante: {espaco_restante})")
            
            for cidade in CIDADES_ADICIONAIS:
                if len(leads_rmc) >= espaco_restante:
                    break
                    
                leads_cidade = self.search_by_nicho_and_local(
                    nicho=nicho,
                    cidade=cidade
                )
                
                if len(leads_rmc) + len(leads_cidade) > espaco_restante:
                    leads_cidade = leads_cidade[:espaco_restante - len(leads_rmc)]
                
                leads_rmc.extend(leads_cidade)

        # Combinar e deduplicar
        todas_leads = leads_curitiba + leads_rmc
        
        # Deduplicação por place_id
        unique = {}
        for lead in todas_leads:
            pid = lead.get("place_id")
            if pid and pid not in unique:
                unique[pid] = lead

        leads_finais = list(unique.values())
        
        print(f"✅ Nicho '{nicho}': {len(leads_finais)} leads únicos coletados")
        return leads_finais

    # --------------------------------------------------
    # ENRIQUECIMENTO COM DETAILS
    # --------------------------------------------------
    def enriquecer_lead(self, lead: Dict, nicho: str) -> Dict:
        place_id = lead.get("place_id")
        if not place_id:
            return lead

        if not self.dry_run:
            details = self.place_details(place_id).get("result", {})
            
            lead.update({
                "telefone": details.get("formatted_phone_number"),
                "site": details.get("website"),
                "geometry": details.get("geometry"),
                "address_components": details.get("address_components", [])
            })
            
            # Registrar métricas
            if self.metrics:
                self.metrics.registrar_place_details(nicho)
                
            time.sleep(REQUEST_DELAY)
        else:
            # Dados mock para dry-run
            lead.update({
                "telefone": "(41) 9999-9999",
                "site": "https://www.site-mock.com.br",
                "geometry": {"location": {"lat": -25.4284, "lng": -49.2733}},
                "address_components": [
                    {"long_name": "Curitiba", "short_name": "Curitiba", "types": ["city"]},
                    {"long_name": "PR", "short_name": "PR", "types": ["administrative_area_level_1"]}
                ]
            })

        return lead
    
    def get_nicho_limits_summary(self):
        """Retorna resumo dos limites configurados"""
        return {
            "limites_por_nicho": self.limite_por_nicho,
            "limite_padrao": self.limite_padrao_por_nicho,
            "limite_por_bairro": self.limite_por_bairro,
            "total_bairros_curitiba": len(BAIRROS_CURITIBA),
            "total_cidades_rmc": len(CIDADES_ADICIONAIS)
        }