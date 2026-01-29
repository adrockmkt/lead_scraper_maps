import time
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from config import (
    CUSTO_TEXT_SEARCH,
    CUSTO_PLACE_DETAILS,
    METRICS_OUTPUT_PATH
)

@dataclass
class ExecutionMetrics:
    """Métricas de execução para análise de performance e custo"""
    
    # Timing
    inicio_execucao: float
    fim_execucao: Optional[float] = None
    duracao_total: Optional[float] = None
    
    # Contadores de API
    total_text_search_calls: int = 0
    total_place_details_calls: int = 0
    
    # Contadores de leads
    leads_coletados: int = 0
    leads_processados: int = 0
    leads_qualificados: int = 0
    leads_sem_email: int = 0
    leads_descartados: int = 0
    leads_duplicados: int = 0
    
    # Métricas por nicho
    metricas_por_nicho: Optional[Dict[str, Dict]] = None
    
    # Métricas por bairro
    metricas_por_bairro: Optional[Dict[str, Dict]] = None
    
    # Custos
    custo_estimado_text_search: float = 0.0
    custo_estimado_place_details: float = 0.0
    custo_total_estimado: float = 0.0
    
    def __post_init__(self):
        if self.metricas_por_nicho is None:
            self.metricas_por_nicho = {}
        if self.metricas_por_bairro is None:
            self.metricas_por_bairro = {}
    
    def registrar_text_search(self, nicho: str, bairro: str, resultados_encontrados: int):
        """Registra uma chamada de Text Search API"""
        self.total_text_search_calls += 1
        self.custo_estimado_text_search += CUSTO_TEXT_SEARCH
        
        # Métricas por nicho
        if nicho not in self.metricas_por_nicho:
            self.metricas_por_nicho[nicho] = {
                "text_search_calls": 0,
                "place_details_calls": 0,
                "leads_coletados": 0,
                "leads_processados": 0,
                "leads_qualificados": 0,
                "tempo_inicio": time.time()
            }
        
        self.metricas_por_nicho[nicho]["text_search_calls"] += 1
        self.metricas_por_nicho[nicho]["leads_coletados"] += resultados_encontrados
        
        # Métricas por bairro
        if bairro not in self.metricas_por_bairro:
            self.metricas_por_bairro[bairro] = {
                "text_search_calls": 0,
                "leads_coletados": 0,
                "nichos_processados": set()
            }
        
        self.metricas_por_bairro[bairro]["text_search_calls"] += 1
        self.metricas_por_bairro[bairro]["leads_coletados"] += resultados_encontrados
        self.metricas_por_bairro[bairro]["nichos_processados"].add(nicho)
    
    def registrar_place_details(self, nicho: str):
        """Registra uma chamada de Place Details API"""
        self.total_place_details_calls += 1
        self.custo_estimado_place_details += CUSTO_PLACE_DETAILS
        
        if nicho in self.metricas_por_nicho:
            self.metricas_por_nicho[nicho]["place_details_calls"] += 1
    
    def registrar_lead_processado(self, nicho: str, bairro: str, status: str):
        """Registra processamento de um lead"""
        self.leads_processados += 1
        
        if nicho in self.metricas_por_nicho:
            self.metricas_por_nicho[nicho]["leads_processados"] += 1
            if status == "qualificado":
                self.metricas_por_nicho[nicho]["leads_qualificados"] += 1
        
        if bairro in self.metricas_por_bairro:
            self.metricas_por_bairro[bairro]["leads_processados"] = (
                self.metricas_por_bairro[bairro].get("leads_processados", 0) + 1
            )
    
    def finalizar_execucao(self):
        """Finaliza métricas e calcula totais"""
        self.fim_execucao = time.time()
        self.duracao_total = self.fim_execucao - self.inicio_execucao
        self.custo_total_estimado = (
            self.custo_estimado_text_search + self.custo_estimado_place_details
        )
        
        # Calcular tempo por nicho
        for nicho_data in self.metricas_por_nicho.values():
            if "tempo_inicio" in nicho_data:
                nicho_data["tempo_duracao"] = time.time() - nicho_data["tempo_inicio"]
                del nicho_data["tempo_inicio"]
        
        # Converter sets para listas para serialização JSON
        for bairro_data in self.metricas_por_bairro.values():
            if "nichos_processados" in bairro_data:
                bairro_data["nichos_processados"] = list(bairro_data["nichos_processados"])
    
    def gerar_relatorio(self) -> Dict:
        """Gera relatório completo das métricas"""
        relatorio = {
            "resumo_execucao": {
                "inicio": datetime.fromtimestamp(self.inicio_execucao).isoformat(),
                "fim": datetime.fromtimestamp(self.fim_execucao).isoformat() if self.fim_execucao else None,
                "duracao_segundos": self.duracao_total,
                "duracao_formatada": self._formatar_duracao(self.duracao_total) if self.duracao_total else None
            },
            "api_calls": {
                "text_search": self.total_text_search_calls,
                "place_details": self.total_place_details_calls,
                "total": self.total_text_search_calls + self.total_place_details_calls
            },
            "leads": {
                "coletados": self.leads_coletados,
                "processados": self.leads_processados,
                "qualificados": self.leads_qualificados,
                "sem_email": self.leads_sem_email,
                "descartados": self.leads_descartados,
                "duplicados": self.leads_duplicados
            },
            "custos_estimados_usd": {
                "text_search": round(self.custo_estimado_text_search, 4),
                "place_details": round(self.custo_estimado_place_details, 4),
                "total": round(self.custo_total_estimado, 4)
            },
            "metricas_por_nicho": self.metricas_por_nicho,
            "metricas_por_bairro": self.metricas_por_bairro
        }
        
        return relatorio
    
    def salvar_relatorio(self):
        """Salva relatório em arquivo JSON"""
        relatorio = self.gerar_relatorio()
        
        import os
        os.makedirs(os.path.dirname(METRICS_OUTPUT_PATH), exist_ok=True)
        
        with open(METRICS_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    def _formatar_duracao(self, segundos: float) -> str:
        """Formata duração em texto legível"""
        if segundos < 60:
            return f"{segundos:.1f}s"
        elif segundos < 3600:
            minutos = segundos / 60
            return f"{minutos:.1f}min"
        else:
            horas = segundos / 3600
            return f"{horas:.1f}h"
    
    def imprimir_resumo(self):
        """Imprime resumo das métricas no console"""
        print("\n" + "="*50)
        print("📊 MÉTRICAS DE EXECUÇÃO - FASE 2")
        print("="*50)
        
        # Tempo e API calls
        print(f"⏱️  Duração: {self._formatar_duracao(self.duracao_total) if self.duracao_total else 'N/A'}")
        print(f"🔌 API Calls: {self.total_text_search_calls} (search) + {self.total_place_details_calls} (details) = {self.total_text_search_calls + self.total_place_details_calls} total")
        
        # Custos
        print(f"💰 Custo estimado: ${self.custo_total_estimado:.4f} USD")
        print(f"   • Text Search: ${self.custo_estimado_text_search:.4f}")
        print(f"   • Place Details: ${self.custo_estimado_place_details:.4f}")
        
        # Leads
        print(f"📈 Leads: {self.leads_processados} processados → {self.leads_qualificados} qualificados")
        if self.leads_processados > 0:
            taxa_qualificacao = (self.leads_qualificados / self.leads_processados) * 100
            print(f"   • Taxa de qualificação: {taxa_qualificacao:.1f}%")
        
        # Top nichos
        print(f"\n🏆 TOP 3 NICHOS POR VOLUME:")
        sorted_nichos = sorted(
            self.metricas_por_nicho.items(),
            key=lambda x: x[1].get("leads_coletados", 0),
            reverse=True
        )[:3]
        
        for i, (nicho, data) in enumerate(sorted_nichos, 1):
            leads = data.get("leads_coletados", 0)
            qualificados = data.get("leads_qualificados", 0)
            print(f"   {i}. {nicho}: {leads} leads, {qualificados} qualificados")
        
        # Top bairros
        print(f"\n🏘️  TOP 5 BAIRROS POR VOLUME:")
        sorted_bairros = sorted(
            self.metricas_por_bairro.items(),
            key=lambda x: x[1].get("leads_coletados", 0),
            reverse=True
        )[:5]
        
        for i, (bairro, data) in enumerate(sorted_bairros, 1):
            leads = data.get("leads_coletados", 0)
            nichos_count = len(data.get("nichos_processados", []))
            print(f"   {i}. {bairro}: {leads} leads, {nichos_count} nichos")
        
        print("="*50)
        print(f"📄 Relatório detalhado salvo em: {METRICS_OUTPUT_PATH}")
        print("="*50 + "\n")


class MetricsCollector:
    """Wrapper para facilitar coleta de métricas durante execução"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.metrics = ExecutionMetrics(inicio_execucao=time.time())
    
    def registrar_text_search(self, nicho: str, bairro: str, resultados: List):
        """Registra chamada de text search (se não for dry run)"""
        if not self.dry_run:
            self.metrics.registrar_text_search(nicho, bairro, len(resultados))
    
    def registrar_place_details(self, nicho: str):
        """Registra chamada de place details (se não for dry run)"""
        if not self.dry_run:
            self.metrics.registrar_place_details(nicho)
    
    def registrar_lead_processado(self, nicho: str, bairro: str, status: str):
        """Registra processamento de lead"""
        self.metrics.registrar_lead_processado(nicho, bairro, status)
    
    def finalizar_e_imprimir(self):
        """Finaliza coleta e imprime relatório"""
        self.metrics.finalizar_execucao()
        self.metrics.imprimir_resumo()
        self.metrics.salvar_relatorio()
        return self.metrics.gerar_relatorio()