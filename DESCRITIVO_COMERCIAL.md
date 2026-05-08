# Descritivo Comercial - Lead Scraper Maps

## Visao geral

O **Lead Scraper Maps** e uma ferramenta de inteligencia comercial para identificar, enriquecer e classificar empresas locais a partir de dados publicos disponiveis no Google Maps e nos sites institucionais dessas empresas.

O projeto foi desenvolvido para apoiar a criacao de bases qualificadas de oportunidades comerciais, estudos de mercado local e analises de concorrencia por nicho e regiao. Ele nao faz envio automatico de emails, mensagens ou qualquer tipo de abordagem ativa. Sua funcao e organizar informacoes publicas e transformar esses dados em uma lista estruturada de empresas com maior potencial comercial.

Na configuracao atual, o sistema esta focado em nichos de alto valor comercial em Curitiba/PR e Regiao Metropolitana, especialmente segmentos em que o cliente costuma buscar uma solucao com urgencia ou alta intencao de compra.

## O problema que o projeto resolve

Empresas que vendem servicos B2B ou atuam com prospeccao local normalmente enfrentam alguns desafios:

- Encontrar empresas reais e ativas em uma regiao especifica.
- Separar negocios com presenca digital minima daqueles com dados incompletos.
- Identificar site, telefone e possiveis canais corporativos de contato.
- Priorizar oportunidades com maior potencial antes de importar tudo para um CRM.
- Reduzir trabalho manual de pesquisa no Google Maps, Google Search e sites individuais.

O Lead Scraper Maps automatiza essa etapa inicial de pesquisa e organizacao, permitindo que a equipe comercial trabalhe com uma base mais limpa, segmentada e priorizada.

## Como o sistema funciona

O funcionamento do projeto segue um pipeline em etapas:

1. **Busca no Google Maps**

   O sistema consulta a Google Places API usando combinacoes de nicho, bairro e cidade. Exemplo: "dedetizadora Batel, Curitiba PR" ou "desentupidora Sao Jose dos Pinhais PR".

2. **Coleta de empresas encontradas**

   Para cada resultado, o sistema captura dados basicos como nome da empresa, endereco, avaliacao, quantidade de avaliacoes e identificador unico do local no Google Maps.

3. **Enriquecimento com dados detalhados**

   Em seguida, o projeto consulta os detalhes do estabelecimento para obter telefone, site, endereco completo, categorias e informacoes complementares disponibilizadas pela API.

4. **Leitura leve do site da empresa**

   Quando a empresa possui site, o sistema acessa a pagina inicial e paginas relacionadas a contato, como "contato", "fale conosco" ou "contact". O objetivo e localizar emails publicados no proprio site.

5. **Classificacao dos emails**

   Os emails encontrados sao separados entre emails genericos, como Gmail, Hotmail e Outlook, e emails corporativos, associados ao dominio da propria empresa. O sistema da preferencia a contatos funcionais, como contato@, comercial@, vendas@ e atendimento@.

6. **Pontuacao automatica**

   Cada empresa recebe um score de 0 a 100 com base em criterios como presenca de site, nicho de alto ticket, concorrencia local, email corporativo e regiao de atuacao.

7. **Exportacao dos resultados**

   Ao final, os dados sao salvos em arquivos CSV separados por status, facilitando analise, revisao e importacao posterior em ferramentas comerciais.

## Nichos mapeados atualmente

O projeto esta configurado para buscar empresas em nichos de alta intencao comercial, como:

- Dedetizadoras
- Desentupidoras
- Guinchos
- Assistencia tecnica de ar condicionado
- Instalacao de ar condicionado
- Manutencao de ar condicionado
- Impermeabilizacao
- Reformas especializadas
- Reparos de telhado
- Hidraulica predial
- Eletrica predial

Esses nichos foram escolhidos por terem caracteristicas comerciais relevantes: ticket potencial maior, necessidade clara do cliente, busca ativa no Google e concorrencia regional.

## Regiao de atuacao configurada

Na versao atual, o projeto busca empresas em:

- Curitiba/PR, com divisao por bairros
- Campo Largo
- Pinhais
- Fazenda Rio Grande
- Sao Jose dos Pinhais

Em Curitiba, o sistema utiliza uma lista de bairros para gerar buscas mais segmentadas, incluindo Centro, Batel, Agua Verde, Bigorrilho, Cabral, Juveve, Reboucas, Portao, Santa Felicidade, Boa Vista, Hauer, Xaxim, Cajuru, Boqueirao, Uberaba, Pinheirinho, Tatuquara e Cidade Industrial.

Essa estrutura pode ser adaptada para outras cidades, regioes ou nichos conforme a necessidade do cliente.

## Criterios de qualificacao

O sistema usa uma regra de pontuacao objetiva. Cada lead pode receber pontos por:

- Possuir site proprio.
- Pertencer a um nicho definido como alto ticket.
- Estar em um nicho/regiao com volume relevante de concorrentes.
- Ter email corporativo identificado no site.
- Estar em regiao considerada estrategica dentro da configuracao do projeto.

A classificacao final e organizada em tres grupos:

- **Leads qualificados**: empresas com score igual ou superior a 70, indicadas como melhores oportunidades para revisao comercial.
- **Leads sem email**: empresas com site, mas sem email corporativo encontrado, recomendadas para contato por telefone, WhatsApp ou pesquisa manual complementar.
- **Leads descartados**: empresas que nao atingem os criterios minimos definidos pela regra de pontuacao.

## Entregaveis gerados

O sistema gera arquivos CSV incrementais dentro da pasta `outputs/`:

- `leads_qualificados.csv`
- `leads_sem_email.csv`
- `leads_descartados.csv`

Os arquivos incluem campos como:

- Nome da empresa
- Site
- Email corporativo, quando encontrado
- Telefone
- Cidade
- Bairro, quando disponivel
- Nicho
- Score
- Status de classificacao

Esses arquivos podem ser usados para analise em planilhas, tratamento comercial, importacao em CRM ou criacao de relatorios.

## Controle de custo e eficiencia

O projeto utiliza a Google Places API, que pode ter custos conforme o volume de consultas. Para reduzir chamadas desnecessarias, o sistema usa cache local em SQLite.

Esse cache evita repetir buscas e enriquecimentos ja processados, tornando execucoes futuras mais rapidas e economicas. A ferramenta tambem possui configuracoes de intervalo entre requisicoes e limite de paginas por consulta, ajudando a manter uma operacao controlada.

## Requisitos tecnicos

Para executar o projeto, sao necessarios:

- Python 3.9 ou superior
- Chave de API da Google Maps Platform com Places API habilitada
- Arquivo `.env` com as credenciais e configuracoes locais
- Instalacao das dependencias do projeto via `requirements.txt`

O projeto roda localmente e nao depende de servidor externo na versao atual.

## Cuidados legais e boas praticas

O Lead Scraper Maps foi projetado para trabalhar com dados publicos e APIs oficiais. Ainda assim, qualquer uso comercial dos dados deve respeitar:

- LGPD
- Termos de uso da Google Maps Platform
- Politicas das ferramentas de CRM e email
- Boas praticas de prospeccao e consentimento

O sistema nao realiza disparos, nao envia mensagens, nao automatiza contato com leads e nao burla mecanismos de autenticacao ou areas privadas.

## Beneficios para o cliente

Para um cliente que precisa mapear oportunidades comerciais, o projeto oferece:

- Reducao de trabalho manual de pesquisa.
- Base mais organizada para prospeccao.
- Priorizacao automatica de oportunidades.
- Visao por nicho, cidade e bairro.
- Identificacao de empresas com presenca digital.
- Separacao entre leads prontos e leads que precisam de complemento manual.
- Possibilidade de evoluir para dashboards, integracoes com CRM e analises mais avancadas.

## Possiveis evolucoes

O projeto ja possui uma base funcional e pode evoluir em fases, conforme o escopo comercial desejado:

- Parametrizacao por cidade, estado, nicho e volume de busca.
- Execucao por linha de comando com filtros especificos.
- Relatorios de performance por nicho e regiao.
- Estimativa de consumo da API.
- Integracao com Google Ads Keyword Planner para leitura de CPC e demanda.
- Dashboard analitico em Looker Studio, Power BI ou ferramenta similar.
- Exportacao padronizada para CRM.
- Agendamento automatico de execucoes.
- Historico de evolucao por data, nicho e regiao.

## Resumo para proposta comercial

O Lead Scraper Maps e uma solucao de inteligencia comercial local que automatiza a identificacao e qualificacao inicial de empresas a partir do Google Maps e de sites publicos. Ele organiza dados dispersos em uma base estruturada, pontuada e pronta para analise comercial, ajudando o cliente a encontrar oportunidades com mais velocidade, criterio e controle operacional.

Na pratica, a ferramenta substitui horas de pesquisa manual por um processo padronizado, auditavel e reutilizavel, criando uma base solida para prospeccao consultiva, estudos de mercado e planejamento de campanhas locais.
