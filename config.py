# =========================================
# CONFIGURAÇÕES GERAIS DO PROJETO
# =========================================

# Cidade principal
CIDADE_PRINCIPAL = "Curitiba"
ESTADO = "PR"
PAIS = "BR"

# Região Metropolitana de Curitiba
CIDADES_ADICIONAIS = [
    "Campo Largo",
    "Pinhais",
    "Fazenda Rio Grande",
    "São José dos Pinhais"
]

# =========================================
# NICHOS – GRUPO 3 (PROBLEMA → SOLUÇÃO)
# Alto ticket, alta dependência de Search
# =========================================

NICHOS_ALTO_TICKET = [
    "dedetizadora",
    "desentupidora",
    "guincho",
    "assistência técnica ar condicionado",
    "instalação ar condicionado",
    "manutenção ar condicionado",
    "impermeabilização",
    "reforma especializada",
    "reparo de telhado",
    "hidráulica predial",
    "elétrica predial"
]

# =========================================
# CLUSTERIZAÇÃO POR BAIRRO (CURITIBA)
# Não limitamos – lista pode crescer
# =========================================

BAIRROS_CURITIBA = [
    "Centro",
    "Batel",
    "Água Verde",
    "Bigorrilho",
    "Cabral",
    "Ahú",
    "Juvevê",
    "Alto da Glória",
    "Rebouças",
    "Portão",
    "Santa Felicidade",
    "Boa Vista",
    "Hauer",
    "Xaxim",
    "Cajuru",
    "Boqueirão",
    "Uberaba",
    "Pinheirinho",
    "Tatuquara",
    "Cidade Industrial"
]

# =========================================
# GOOGLE PLACES – TEXT SEARCH
# =========================================

PLACES_TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
PLACES_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

# Campos solicitados no Place Details (economia de custo)
PLACES_DETAILS_FIELDS = [
    "name",
    "types",
    "formatted_address",
    "address_components",
    "formatted_phone_number",
    "website",
    "geometry"
]

# =========================================
# FILTROS DE QUALIDADE
# =========================================

# Domínios de email genéricos (descartar como email válido)
EMAIL_DOMINIOS_GENERICOS = [
    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "yahoo.com",
    "icloud.com",
    "live.com",
    "aol.com"
]

# Keywords que indicam email funcional (preferência)
EMAIL_FUNCIONAL_KEYWORDS = [
    "contato",
    "comercial",
    "vendas",
    "atendimento",
    "suporte",
    "orcamento"
]

# =========================================
# SCORE DE QUALIDADE (0–100)
# =========================================

SCORE_REGRAS = {
    "tem_site": 25,
    "nicho_alto_ticket": 25,
    "concorrencia_alta": 20,   # >= 10 resultados
    "email_corporativo": 20,
    "regiao_valorizada": 10
}

SCORE_MINIMO_APROVACAO = 70

# =========================================
# OUTPUTS
# =========================================

OUTPUT_LEADS_QUALIFICADOS = "outputs/leads_qualificados.csv"
OUTPUT_LEADS_SEM_EMAIL = "outputs/leads_sem_email.csv"
OUTPUT_LEADS_DESCARTADOS = "outputs/leads_descartados.csv"

# =========================================
# FASE 2 - OTIMIZAÇÃO DE CUSTO E PERFORMANCE
# =========================================

# Limites dinâmicos por nicho (max resultados por nicho)
LIMITE_POR_NICHO = {
    "dedetizadora": 50,
    "desentupidora": 50,
    "guincho": 40,
    "assistência técnica ar condicionado": 30,
    "instalação ar condicionado": 30,
    "manutenção ar condicionado": 30,
    "impermeabilização": 25,
    "reforma especializada": 20,
    "reparo de telhado": 25,
    "hidráulica predial": 35,
    "elétrica predial": 35
}

# Limite padrão para nichos não especificados
LIMITE_PADRAO_POR_NICHO = 30

# Limites por bairro (max resultados por bairro por nicho)
LIMITE_POR_BAIRRO = 15

# Custo estimado por chamada da API (em USD)
CUSTO_TEXT_SEARCH = 0.005  # ~$5 por 1000 chamadas
CUSTO_PLACE_DETAILS = 0.017  # ~$17 por 1000 chamadas

# Métricas de performance
METRICS_OUTPUT_PATH = "outputs/metrics_report.json"