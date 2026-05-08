# ROADMAP – Lead Scraper Maps

Este documento descreve as **evoluções planejadas** para o projeto **Lead Scraper Maps**, considerando boas práticas de engenharia, controle de custo, escalabilidade e uso responsável de dados públicos.

O roadmap está organizado por **fases**, permitindo evolução incremental sem comprometer a estabilidade do pipeline atual.

Documentos relacionados:
- [DESCRITIVO_COMERCIAL.md](DESCRITIVO_COMERCIAL.md): visão comercial do projeto para apoiar proposta.
- [ESCOPO_ENTREGA_EXCEL.md](ESCOPO_ENTREGA_EXCEL.md): escopo específico para transformar o projeto em uma entrega de planilha Excel por categorias e cidades.

---

## 🟢 Fase 1 — Consolidação do Pipeline Atual (Status: Concluída)

Objetivo: garantir um pipeline estável, reutilizável e com governança técnica.

Entregas:
- [x] Integração com Google Places API (Text Search)
- [x] Clusterização por bairro (Curitiba + RMC)
- [x] Enriquecimento via Place Details
- [x] Crawling leve de sites institucionais
- [x] Extração e classificação de emails
- [x] Sistema de score (0–100)
- [x] Cache local em SQLite
- [x] Exportação incremental em CSV
- [x] README público-safe
- [x] Descritivo comercial do projeto
- [x] Escopo futuro para entrega em Excel
- [x] .gitignore e governança de segredos

---

## 🟢 Fase 2 — Otimização de Custo e Performance (Status: Concluída)

Objetivo: reduzir chamadas desnecessárias à API e acelerar execuções recorrentes.

Entregas:
- [x] Modo `DRY_RUN` (simulação sem chamadas à API)
- [x] Limite dinâmico por nicho / bairro
- [x] Controle de execução por flags (CLI args)
- [x] Métricas de execução (tempo por nicho, volume por bairro)
- [x] Relatório resumido de consumo estimado da API

Arquivos implementados:
- `main_enhanced.py` - Pipeline com CLI e controle granular
- `services/places_client_enhanced.py` - Cliente com dry-run e limites
- `services/metrics.py` - Coleta e análise de métricas
- `test_fase2.py` - Suite de testes para validação
- `FASE2_DOCUMENTATION.md` - Documentação completa

Uso:
```bash
python main_enhanced.py --dry-run --nichos "dedetizadora,desentupidora" --limite-global 25 --verbose
```

---

## 🟡 Fase 3 — Produto Comercial em Excel

Objetivo: preparar o projeto para uma entrega comercial vendável, baseada em categorias e cidades definidas pelo cliente.

Planejado:
- [ ] Parametrização por cliente/projeto
- [ ] Configuração externa de categorias, cidades e bairros
- [ ] Suporte mais flexível a múltiplas cidades/estados
- [ ] Exportação real em `.xlsx`
- [ ] Abas por categoria ou cidade
- [ ] Aba de resumo executivo
- [ ] Organização de outputs por cliente e data
- [ ] Inclusão de campos adicionais na entrega final: endereço, rating, quantidade de avaliações, query de origem e data da coleta
- [ ] Relatório resumido da execução
- [ ] Normalização de telefone e validação básica de emails

Detalhamento desta fase: [ESCOPO_ENTREGA_EXCEL.md](ESCOPO_ENTREGA_EXCEL.md).

---

## 🟠 Fase 4 — Enriquecimento de Inteligência de Mercado

Objetivo: elevar a qualidade analítica dos leads e do contexto competitivo.

Planejado:
- [ ] Integração com Google Ads Keyword Planner (CPC médio)
- [ ] Detecção de anúncios ativos no SERP (proxy competitivo)
- [ ] Classificação automática de maturidade digital
- [ ] Ajuste dinâmico de score baseado em dados reais

---

## 🔵 Fase 5 — Escalabilidade e Automação Controlada

Objetivo: permitir execução recorrente sem perder controle operacional.

Planejado:
- [ ] Execução agendada (cron)
- [ ] Persistência de histórico por data
- [ ] Versionamento de outputs
- [ ] Suporte a múltiplas cidades/estados
- [ ] Configuração por arquivo YAML/JSON

---

## 🟣 Fase 6 — Integrações e Visualização

Objetivo: facilitar análise e uso estratégico dos dados gerados.

Planejado:
- [ ] Exportação direta para CRMs (ex: via CSV padronizado ou API)
- [ ] Dashboard analítico (Looker Studio / Data Studio)
- [ ] Visualização geográfica por bairro
- [ ] Comparativo histórico por nicho

---

## ⚠️ Princípios de Evolução

Este projeto seguirá sempre os princípios:
- Execução consciente e incremental
- Uso responsável de APIs e dados públicos
- Evitar scraping agressivo ou massivo
- Clareza entre uso técnico e uso comercial
- Não prometer email ou telefone para 100% das empresas
- Entregar dados encontrados em fontes públicas, com transparência sobre limitações

---

## 📌 Observação Final

Este roadmap é **vivo** e pode ser ajustado conforme:
- mudanças nos termos das APIs
- necessidades técnicas
- aprendizados obtidos com o uso real do pipeline
