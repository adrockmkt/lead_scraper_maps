#!/usr/bin/env python3
"""
Lead Scraper Maps - Fase 2: Otimização de Custo e Performance

Uso:
    python main.py [opções]

Opções:
    --dry-run               Simulação sem chamadas à API
    --nichos "nicho1,nicho2"  Nichos específicos (ex: "dedetizadora,desentupidora")
    --bairros "bairro1,bairro2" Bairros específicos
    --limite-global N       Limite global de leads por nicho
    --limite-bairro N       Limite de leads por bairro
    --verbose               Saída detalhada
    --no-metrics            Desativar coleta de métricas
    --help                  Ajuda
"""

import os
import sys
import argparse
from dotenv import load_dotenv

from config import (
    NICHOS_ALTO_TICKET,
    CIDADE_PRINCIPAL,
    BAIRROS_CURITIBA,
    LIMITE_POR_NICHO,
    LIMITE_PADRAO_POR_NICHO,
    LIMITE_POR_BAIRRO
)

from services.places_client_enhanced import GooglePlacesClientEnhanced
from services.site_crawler import SiteCrawler
from services.scoring import LeadScorer
from services.storage import Storage
from services.metrics import MetricsCollector

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
# CLI ARGUMENT PARSING
# ======================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Lead Scraper Maps - Fase 2: Otimização de Custo e Performance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --dry-run --verbose
  python main.py --nichos "dedetizadora,desentupidora" --limite-global 25
  python main.py --bairros "Centro,Batel,Água Verde" --no-metrics
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulação sem chamadas à API (usado para testes e planejamento)"
    )
    
    parser.add_argument(
        "--nichos",
        type=str,
        help="Nichos específicos separados por vírgula (ex: 'dedetizadora,desentupidora')"
    )
    
    parser.add_argument(
        "--bairros",
        type=str,
        help="Bairros específicos separados por vírgula (ex: 'Centro,Batel,Água Verde')"
    )
    
    parser.add_argument(
        "--limite-global",
        type=int,
        help="Limite global de leads por nicho (sobrescreve config)"
    )
    
    parser.add_argument(
        "--limite-bairro",
        type=int,
        help="Limite de leads por bairro (sobrescreve config)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Saída detalhada do processo"
    )
    
    parser.add_argument(
        "--no-metrics",
        action="store_true",
        help="Desativar coleta de métricas de performance"
    )
    
    return parser.parse_args()

# ======================================================
# ENHANCED MAIN PIPELINE
# ======================================================

def main():
    args = parse_arguments()
    
    # Configuração inicial
    print("🚀 Lead Scraper Maps - Fase 2: Otimização de Custo e Performance")
    print("=" * 60)
    
    if args.dry_run:
        print("🔍 MODO DRY-RUN ATIVADO (simulação sem chamadas à API)")
    
    # Filtros de nichos
    nichos_processar = NICHOS_ALTO_TICKET
    if args.nichos:
        nichos_processar = [n.strip() for n in args.nichos.split(",")]
        print(f"🎯 Nichos filtrados: {', '.join(nichos_processar)}")
    
    # Filtros de bairros
    bairros_processar = BAIRROS_CURITIBA
    if args.bairros:
        bairros_processar = [b.strip() for b in args.bairros.split(",")]
        print(f"🏘️  Bairros filtrados: {', '.join(bairros_processar)}")
    
    # Inicialização dos componentes
    metrics_collector = None if args.no_metrics else MetricsCollector(dry_run=args.dry_run)
    
    places_client = GooglePlacesClientEnhanced(
        dry_run=args.dry_run,
        metrics_collector=metrics_collector
    )
    
    # Sobrescrever limites se especificado
    if args.limite_global:
        places_client.limite_padrao_por_nicho = args.limite_global
        print(f"📊 Limite global por nicho: {args.limite_global}")
    
    if args.limite_bairro:
        places_client.limite_por_bairro = args.limite_bairro
        print(f"📊 Limite por bairro: {args.limite_bairro}")
    
    crawler = SiteCrawler(user_agent=USER_AGENT)
    scorer = LeadScorer()
    storage = Storage(db_path=SQLITE_DB_PATH)
    
    # Sobrescrever bairros no config se filtrado
    if args.bairros:
        # Import dinâmico para sobrescrever configuração
        import config
        config.BAIRROS_CURITIBA = bairros_processar
    
    # Métricas gerais
    total_processados = 0
    total_qualificados = 0
    total_sem_email = 0
    total_descartados = 0
    total_pulados_existente = 0
    
    # ==================================================
    # PIPELINE PRINCIPAL
    # ==================================================
    
    for nicho in nichos_processar:
        print(f"\n🎯 === NICHo: {nicho.upper()} ===")
        
        # Verificar se nicho está na lista de limites
        if nicho not in LIMITE_POR_NICHO:
            print(f"⚠️  Nicho '{nicho}' não possui limite específico, usando padrão ({LIMITE_PADRAO_POR_NICHO})")
        
        # Coletar leads
        leads_maps = places_client.coletar_por_nicho(nicho)
        
        if not leads_maps:
            print(f"❌ Nenhum lead encontrado para '{nicho}'")
            continue
        
        print(f"📋 {len(leads_maps)} leads únicos encontrados")
        
        # Proxy simples de concorrência
        concorrencia_nicho = len(leads_maps)
        
        # Processar leads
        for i, lead in enumerate(leads_maps, 1):
            if args.verbose:
                print(f"  [{i}/{len(leads_maps)}] Processando: {lead.get('nome', 'N/A')}")
            
            place_id = lead.get("place_id")
            
            # Verificar se já existe
            if storage.lead_exists(place_id):
                if args.verbose:
                    print(f"    ⏭️  Lead já existe no banco, pulando")
                total_pulados_existente += 1
                continue
            
            # Enriquecer com details
            lead = places_client.enriquecer_lead(lead, nicho)
            
            lead.update({
                "nicho": nicho,
                "cidade": CIDADE_PRINCIPAL,
                "concorrencia": concorrencia_nicho
            })
            
            # Extrair bairro do endereço para métricas
            bairro_lead = "Não identificado"
            endereco = lead.get("endereco", "")
            for bairro in bairros_processar:
                if bairro.lower() in endereco.lower():
                    bairro_lead = bairro
                    break
            
            # Crawling do site
            email_corporativo = None
            site = lead.get("site")
            
            if site and not storage.site_crawled(site):
                if not args.dry_run:
                    crawl_result = crawler.crawl_site(site)
                    emails_corp = crawl_result.get("emails_corporativos", [])
                    if emails_corp:
                        email_corporativo = emails_corp[0]
                    storage.mark_site_crawled(site)
                else:
                    # Mock para dry-run
                    email_corporativo = f"contato@{site.replace('https://www.', '').replace('https://', '')}"
            
            lead["email_corporativo"] = email_corporativo
            
            # Scoring
            lead = scorer.calcular_score(lead)
            
            # Persistência (se não for dry-run)
            if not args.dry_run:
                storage.save_lead(lead)
                storage.export_csv(lead)
            
            # Registrar métricas
            if metrics_collector:
                metrics_collector.registrar_lead_processado(
                    nicho=nicho,
                    bairro=bairro_lead,
                    status=lead.get("status", "desconhecido")
                )
            
            # Contadores
            total_processados += 1
            status = lead.get("status", "desconhecido")
            
            if status == "qualificado":
                total_qualificados += 1
                if args.verbose:
                    print(f"    ✅ Qualificado! (score: {lead.get('score', 0)})")
            elif status == "sem_email":
                total_sem_email += 1
                if args.verbose:
                    print(f"    ⚠️  Sem email corporativo")
            else:
                total_descartados += 1
                if args.verbose:
                    print(f"    ❌ Descartado (score: {lead.get('score', 0)})")
    
    # ==================================================
    # RESUMO FINAL
    # ==================================================
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DA EXECUÇÃO")
    print("=" * 60)
    
    print(f"📈 Leads processados: {total_processados}")
    print(f"✅ Qualificados: {total_qualificados}")
    print(f"⚠️  Sem email corporativo: {total_sem_email}")
    print(f"❌ Descartados: {total_descartados}")
    print(f"⏭️  Pulados (já existentes): {total_pulados_existente}")
    
    if total_processados > 0:
        taxa_qualificacao = (total_qualificados / total_processados) * 100
        print(f"🎯 Taxa de qualificação: {taxa_qualificacao:.1f}%")
    
    if args.dry_run:
        print("\n🔍 EXECUÇÃO EM MODO DRY-RUN")
        print("   Nenhuma chamada real à API foi realizada")
        print("   Nenhum dado foi persistido no banco")
        print("   Nenhum arquivo CSV foi gerado")
    else:
        print("\n💾 Arquivos CSV gerados em /outputs")
    
    # Imprimir métricas detalhadas
    if metrics_collector:
        metrics_collector.finalizar_e_imprimir()
    
    print("\n✅ Execução finalizada!")
    print("=" * 60)


# ======================================================
# ENTRYPOINT
# ======================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execução interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        sys.exit(1)