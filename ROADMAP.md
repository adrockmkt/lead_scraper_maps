# ROADMAP – Lead Scraper Maps

Este documento descreve as **evoluções planejadas** para o projeto **Lead Scraper Maps**, considerando boas práticas de engenharia, controle de custo, escalabilidade e uso responsável de dados públicos.

O roadmap está organizado por **fases**, permitindo evolução incremental sem comprometer a estabilidade do pipeline atual.

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
- [x] .gitignore e governança de segredos

---

## 🟡 Fase 2 — Otimização de Custo e Performance

Objetivo: reduzir chamadas desnecessárias à API e acelerar execuções recorrentes.

Planejado:
- [ ] Modo `DRY_RUN` (simulação sem chamadas à API)
- [ ] Limite dinâmico por nicho / bairro
- [ ] Controle de execução por flags (CLI args)
- [ ] Métricas de execução (tempo por nicho, volume por bairro)
- [ ] Relatório resumido de consumo estimado da API

---

## 🟠 Fase 3 — Enriquecimento de Inteligência de Mercado

Objetivo: elevar a qualidade analítica dos leads e do contexto competitivo.

Planejado:
- [ ] Integração com Google Ads Keyword Planner (CPC médio)
- [ ] Detecção de anúncios ativos no SERP (proxy competitivo)
- [ ] Classificação automática de maturidade digital
- [ ] Ajuste dinâmico de score baseado em dados reais

---

## 🔵 Fase 4 — Escalabilidade e Automação Controlada

Objetivo: permitir execução recorrente sem perder controle operacional.

Planejado:
- [ ] Execução agendada (cron)
- [ ] Persistência de histórico por data
- [ ] Versionamento de outputs
- [ ] Suporte a múltiplas cidades/estados
- [ ] Configuração por arquivo YAML/JSON

---

## 🟣 Fase 5 — Integrações e Visualização

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

---

## 📌 Observação Final

Este roadmap é **vivo** e pode ser ajustado conforme:
- mudanças nos termos das APIs
- necessidades técnicas
- aprendizados obtidos com o uso real do pipeline
