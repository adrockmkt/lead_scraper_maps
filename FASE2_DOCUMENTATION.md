# Fase 2 - Otimização de Custo e Performance

## 📋 Visão Geral

A Fase 2 implementa otimizações críticas para reduzir custos de API, melhorar performance e fornecer maior controle sobre a execução do pipeline.

## 🚀 Novas Funcionalidades

### 1. Modo DRY_RUN
Simulação completa sem chamadas reais à API Google Maps.

**Uso:**
```bash
python main_enhanced.py --dry-run
```

**Benefícios:**
- Testar configurações sem custos
- Validar lógica de negócio
- Planejar volume de coleta
- Debug de fluxo

### 2. Limites Dinâmicos por Nicho/Bairro
Controle granular sobre volume de coleta.

**Configuração (config.py):**
```python
LIMITE_POR_NICHO = {
    "dedetizadora": 50,
    "desentupidora": 50,
    "guincho": 40,
    # ... outros nichos
}
LIMITE_PADRAO_POR_NICHO = 30
LIMITE_POR_BAIRRO = 15
```

**Sobrescrita via CLI:**
```bash
python main_enhanced.py --limite-global 25 --limite-bairro 10
```

### 3. Controle de Execução por Flags (CLI)
Filtragem e controle granular da execução.

**Opções Disponíveis:**
```bash
# Nichos específicos
python main_enhanced.py --nichos "dedetizadora,desentupidora"

# Bairros específicos
python main_enhanced.py --bairros "Centro,Batel,Água Verde"

# Saída detalhada
python main_enhanced.py --verbose

# Desativar métricas
python main_enhanced.py --no-metrics
```

### 4. Métricas de Execução
Coleta automática de métricas detalhadas.

**Métricas Coletadas:**
- Tempo por nicho
- Volume por bairro
- Consumo estimado da API
- Taxa de qualificação
- Custos por tipo de chamada

**Relatório Gerado:**
```json
{
  "resumo_execucao": {
    "duracao_segundos": 180.5,
    "duracao_formatada": "3.0min"
  },
  "api_calls": {
    "text_search": 45,
    "place_details": 120,
    "total": 165
  },
  "custos_estimados_usd": {
    "text_search": 0.2250,
    "place_details": 2.0400,
    "total": 2.2650
  },
  "metricas_por_nicho": {...},
  "metricas_por_bairro": {...}
}
```

### 5. Relatório de Consumo Estimado da API
Previsão de custos baseada no volume de chamadas.

**Custos Configurados:**
```python
CUSTO_TEXT_SEARCH = 0.005    # ~$5 por 1000 chamadas
CUSTO_PLACE_DETAILS = 0.017  # ~$17 por 1000 chamadas
```

**Exemplo de Cálculo:**
- 45 chamadas Text Search: $0.225
- 120 chamadas Place Details: $2.040
- **Total estimado: $2.265**

## 📊 Exemplos de Uso

### Cenário 1: Teste Completo
```bash
python main_enhanced.py --dry-run --verbose
```
- Simulação completa
- Saída detalhada
- Sem custos

### Cenário 2: Coleta Focada
```bash
python main_enhanced.py --nichos "dedetizadora,desentupidora" --limite-global 25
```
- Apenas 2 nichos
- Limite reduzido
- Métricas ativas

### Cenário 3: Região Específica
```bash
python main_enhanced.py --bairros "Centro,Batel,Água Verde" --verbose
```
- Apenas bairros centrais
- Saída detalhada
- Todos nichos

### Cenário 4: Otimização de Custos
```bash
python main_enhanced.py --limite-global 15 --limite-bairro 5 --no-metrics
```
- Limites reduzidos
- Sem coleta de métricas
- Custo mínimo

## 📈 Relatórios Gerados

### 1. Console Output
```
📊 MÉTRICAS DE EXECUÇÃO - FASE 2
==================================================
⏱️  Duração: 3.0min
🔌 API Calls: 45 (search) + 120 (details) = 165 total
💰 Custo estimado: $2.2650 USD
📈 Leads: 120 processados → 45 qualificados
   • Taxa de qualificação: 37.5%

🏆 TOP 3 NICHOS POR VOLUME:
   1. dedetizadora: 50 leads, 20 qualificados
   2. desentupidora: 45 leads, 18 qualificados
   3. guincho: 25 leads, 7 qualificados
```

### 2. JSON Report (outputs/metrics_report.json)
Relatório detalhado com todas as métricas para análise posterior.

## 🔧 Configuração Avançada

### Variáveis de Ambiente (.env)
```bash
# Controle de requisições
REQUEST_DELAY=1.2
MAX_PAGES_PER_QUERY=2

# Paths
SQLITE_DB_PATH=data/leads.db
USER_AGENT=LeadScraperMaps/1.0
```

### Configuração de Limites (config.py)
```python
# Personalizar por nicho
LIMITE_POR_NICHO = {
    "dedetizadora": 100,  # Alta demanda
    "guincho": 20,        # Baixa demanda
    # ...
}

# Limites globais
LIMITE_PADRAO_POR_NICHO = 30
LIMITE_POR_BAIRRO = 15
```

## 🎯 Benefícios Alcançados

### 1. Redução de Custos
- **DRY_RUN**: Testes sem custos
- **Limites**: Controle fino de volume
- **Métricas**: Visibilidade do consumo

### 2. Melhoria de Performance
- **Filtragem**: Processamento apenas do necessário
- **Limites**: Evita sobrecarga
- **Métricas**: Identificação de gargalos

### 3. Controle Operacional
- **CLI**: Execução parametrizada
- **Métricas**: Monitoramento em tempo real
- **Relatórios**: Análise pós-execução

### 4. Governança
- **Limites**: Respeito a cotas de API
- **DRY_RUN**: Validação segura
- **Métricas**: Auditoria de uso

## 📝 Próximos Passos

1. **Integração com Fase 3**: Enriquecimento com dados de mercado
2. **Automação Agendada**: Execução via cron
3. **Dashboard Visual**: Interface web para métricas
4. **Alertas**: Notificações de custos/limites

## 🐛 Troubleshooting

### Problemas Comuns

**1. Erro de API em DRY_RUN**
- DRY_RUN não deve requerer API_KEY
- Verificar se a flag está sendo usada corretamente

**2. Limites não aplicados**
- Verificar configuração em config.py
- Sobrescrita via CLI tem prioridade

**3. Métricas não geradas**
- Verificar flag --no-metrics
- Confirmar permissões de escrita em /outputs

**4. Performance lenta**
- Aumentar REQUEST_DELAY no .env
- Reduzir MAX_PAGES_PER_QUERY
- Usar filtros para reduzir volume

### Debug Mode
```bash
python main_enhanced.py --dry-run --verbose --nichos "dedetizadora"
```

## 📚 Referências

- [Google Places API Pricing](https://developers.google.com/maps/billing-and-pricing)
- [Python Argparse Documentation](https://docs.python.org/3/library/argparse.html)
- [Roadmap do Projeto](roadmap.md)