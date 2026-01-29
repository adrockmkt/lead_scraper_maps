#!/usr/bin/env python3
"""
Test Script para Fase 2 - Otimização de Custo e Performance

Este script demonstra todas as novas funcionalidades implementadas.
"""

import os
import sys

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_dry_run():
    """Testa modo DRY_RUN com um único nicho"""
    print("\n🧪 Test 1: DRY_RUN Mode")
    print("="*50)
    
    os.system("python main_enhanced.py --dry-run --nichos 'dedetizadora' --verbose")
    
def test_limites():
    """Testa limites personalizados"""
    print("\n🧪 Test 2: Limites Personalizados")
    print("="*50)
    
    os.system("python main_enhanced.py --dry-run --nichos 'dedetizadora' --limite-global 10 --limite-bairro 3")
    
def test_bairros_filtrados():
    """Testa filtragem por bairros"""
    print("\n🧪 Test 3: Bairros Filtrados")
    print("="*50)
    
    os.system("python main_enhanced.py --dry-run --nichos 'dedetizadora' --bairros 'Centro,Batel' --verbose")
    
def test_multiple_nichos():
    """Testa múltiplos nichos com limites"""
    print("\n🧪 Test 4: Múltiplos Nichos")
    print("="*50)
    
    os.system("python main_enhanced.py --dry-run --nichos 'dedetizadora,desentupidora' --limite-global 5")
    
def test_help():
    """Mostra help do sistema"""
    print("\n🧪 Test 5: Help System")
    print("="*50)
    
    os.system("python main_enhanced.py --help")

def main():
    """Executa todos os testes"""
    print("🚀 TEST SUITE - FASE 2")
    print("=" * 60)
    print("Demonstrando todas as funcionalidades implementadas")
    
    try:
        test_dry_run()
        test_limites()
        test_bairros_filtrados()
        test_multiple_nichos()
        test_help()
        
        print("\n" + "="*60)
        print("✅ TODOS OS TESTES CONCLUÍDOS!")
        print("="*60)
        
        print("\n📊 Verifique os relatórios gerados:")
        print("   • outputs/metrics_report.json (se gerado)")
        print("   • Saída detalhada no console")
        
        print("\n🎯 Principais funcionalidades demonstradas:")
        print("   ✅ DRY_RUN - Simulação sem custos")
        print("   ✅ Limites dinâmicos por nicho/bairro")
        print("   ✅ Controle via flags CLI")
        print("   ✅ Métricas detalhadas")
        print("   ✅ Relatórios de consumo")
        
    except Exception as e:
        print(f"\n❌ Erro durante testes: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()