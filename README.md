# Lead Scraper Maps – Grupo 3 (Alto Ticket)

Este projeto é um **scraper técnico e educativo** para coleta estruturada de dados **publicamente disponíveis** no Google Maps (via Google Places API), com foco em **análise de mercado local** e **estudos de concorrência**.

Ele foi projetado para execução **local**, com controle de custo, cache em SQLite e geração de dados estruturados para **análise estratégica**, não para envio automático de comunicações.

---

## 🎯 Objetivo do Projeto

O objetivo deste projeto é demonstrar uma arquitetura prática para coleta, enriquecimento e classificação de dados públicos de negócios locais, atendendo aos seguintes critérios técnicos:

- Empresa com **site próprio**
- Presença ativa no **Google Maps**
- Atuação em **nichos de alto ticket** (problema → solução)
- Localização em regiões com **concorrência relevante** (proxy de Ads caros)
- Preferência por **email corporativo** (separando casos sem email)

---

## 🧱 Arquitetura Geral

Pipeline resumido:

1. **Google Maps (Places API – Text Search)**
   - Busca por *nicho + bairro + cidade*
   - Curitiba/PR + Região Metropolitana

2. **Enriquecimento (Place Details)**
   - Site
   - Telefone
   - Endereço
   - Componentes de endereço (bairro)

3. **Crawling leve do site**
   - Home + páginas de contato
   - Extração de emails
   - Classificação: corporativo vs genérico

4. **Scoring automático (0–100)**
   - Nicho
   - Concorrência
   - Região
   - Presença de email corporativo

5. **Persistência e saída**
   - Cache SQLite
   - CSVs incrementais por status

---

## 📁 Estrutura do Projeto

```
lead_scraper_maps/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── config.py
├── services/
│   ├── places_client.py
│   ├── site_crawler.py
│   ├── scoring.py
│   └── storage.py
├── data/
│   └── sqlite_cache.db
└── outputs/
    ├── leads_qualificados.csv
    ├── leads_sem_email.csv
    └── leads_descartados.csv
```

---

## ⚙️ Requisitos

- Python **3.9+**
- Conta Google Cloud com **Places API habilitada**
- Ambiente virtual (`venv`)

---

## 🔐 Configuração

### 1. Criar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar `.env`

```env
GOOGLE_MAPS_API_KEY=COLE_SUA_API_KEY
REQUEST_DELAY=1.2
USER_AGENT=Mozilla/5.0
SQLITE_DB_PATH=data/sqlite_cache.db
```

⚠️ **Nunca versionar o `.env`**.

---

## ▶️ Execução

Rodar o pipeline completo:

```bash
python main.py
```

Na primeira execução:
- Mais lenta (cache vazio)
- Maior volume de chamadas à API

Execuções seguintes:
- Muito mais rápidas
- Uso intensivo de cache

---

## 📤 Outputs Gerados

Todos os arquivos são gerados incrementalmente em `outputs/`:

- **leads_qualificados.csv**
  - Score ≥ 70
  - Prontos para CRM / Kit / abordagem direta

- **leads_sem_email.csv**
  - Empresas com site, mas sem email corporativo
  - Ideais para contato via telefone ou WhatsApp

- **leads_descartados.csv**
  - Fora do perfil estratégico

---

## 🧠 Estratégia de Uso

Este projeto tem caráter **técnico e demonstrativo**. Ele pode ser utilizado para:

- Estudos de mercado local
- Análise de concorrência por região e nicho
- Avaliação de maturidade digital (site, presença local, canais)
- Prototipagem de pipelines de dados

Qualquer uso para comunicação, prospecção ou marketing deve respeitar integralmente:
- LGPD
- Termos de Uso do Google
- Políticas de consentimento das plataformas de email/CRM

---

## 🔒 Compliance e Boas Práticas

- Utiliza exclusivamente **dados públicos**
- Consome APIs oficiais (Google Places API)
- Crawling limitado e não intrusivo
- Rate limit e cache aplicados
- Não realiza envio de emails, mensagens ou automações de contato

---

## 💰 Limites de Custo e Boas Práticas de API

Este projeto utiliza a **Google Places API**, que possui modelo de cobrança por volume de requisições. Para evitar custos inesperados, siga rigorosamente as boas práticas abaixo.

### 📌 Recomendações de Controle de Custo

- **Utilize sempre cache local (SQLite)**
  - O projeto já evita chamadas duplicadas para o mesmo `place_id` e domínio
  - Não apague o arquivo `data/sqlite_cache.db` entre execuções

- **Execute por nichos específicos**
  - Evite rodar todos os nichos simultaneamente
  - Valide os resultados de um nicho antes de avançar para o próximo

- **Monitore o consumo no Google Cloud Console**
  - Acesse: *Billing → Reports*
  - Filtre por *Places API*

- **Aplique limites de execução**
  - Reduza temporariamente a lista de bairros em `config.py` para testes
  - Ajuste `MAX_PAGES_PER_QUERY` no `.env` durante validação inicial

### 🔐 Boas Práticas de Segurança da API Key

- Restrinja a API Key para:
  - **Places API apenas**
  - (Opcional) IP local durante desenvolvimento

- Nunca versionar ou expor a chave em repositórios públicos

### 📊 Cotas gratuitas e modelo de cobrança da Google Maps API

Este projeto utiliza exclusivamente endpoints da **Google Places API** (Text Search e Place Details), que possuem **cota gratuita mensal** oferecida pela Google Maps Platform.

Atualmente, a Google disponibiliza:

- **Places API – Text Search**: até **5.000 requisições/mês sem custo**
- **Places Details (campos básicos)**: até **5.000 requisições/mês sem custo**

As cotas são **renovadas mensalmente** e são **independentes por tipo de requisição (SKU)**.

No cenário de uso deste projeto — execução manual, escopo regional (Curitiba e Região Metropolitana), cache persistente em SQLite e execução por nicho — é possível operar **integralmente dentro do free tier**, sem geração de cobrança.

Mesmo assim, recomenda-se fortemente a criação de um **budget mensal** no Google Cloud Console para monitoramento e alertas preventivos.

### ⚠️ Observação Importante

O projeto foi desenhado para **execução consciente e incremental**. Ele não deve ser utilizado como crawler massivo ou contínuo.

A responsabilidade pelo uso da API, custos gerados e conformidade com os termos do Google é sempre do operador do script.

---

## 🚀 Evoluções Planejadas

- Integração com Google Ads Keyword Planner (CPC real)
- Detecção de anúncios ativos no SERP
- Clusterização avançada por renda
- Exportação direta para CRMs
- Execução automatizada (cron / servidor)

---

## 👤 Autor

Projeto open-source desenvolvido pela **Ad Rock Digital Mkt** como referência técnica para arquiteturas de coleta e análise de dados locais.

Este repositório é disponibilizado para fins **educacionais e técnicos**.