# Escopo Futuro - Entrega de Planilha Excel por Categorias e Cidades

## Objetivo comercial

Este documento registra o que ainda precisa ser evoluido no projeto **Lead Scraper Maps** para que ele seja usado como base de uma entrega comercial ao cliente: uma planilha Excel segmentada por categorias e cidades, contendo empresas encontradas em fontes publicas, com nome, telefone, site e email quando disponivel.

A ideia e permitir a venda de um servico de **mapeamento e qualificacao de leads locais**, com entrega final em formato simples para o cliente usar em planilha, CRM ou processo comercial.

## O que o projeto ja faz hoje

O projeto atual ja possui a base tecnica principal:

- Busca empresas no Google Maps usando Google Places API.
- Pesquisa por nichos/categorias definidos no arquivo `config.py`.
- Pesquisa em Curitiba/PR, bairros de Curitiba e algumas cidades da Regiao Metropolitana.
- Remove duplicidades usando o `place_id` do Google.
- Enriquece os registros com telefone, site, endereco e dados complementares do local.
- Acessa o site da empresa quando existe.
- Busca emails publicados na home e em paginas de contato.
- Separa emails corporativos de emails genericos.
- Calcula um score de qualificacao de 0 a 100.
- Classifica os registros como `qualificado`, `sem_email` ou `descartado`.
- Salva cache local em SQLite para evitar reprocessamento.
- Exporta resultados em CSV.

## Entrega comercial pretendida

Para uma proposta comercial, a entrega desejada pode ser descrita assim:

> Entrega de uma planilha Excel segmentada por categorias e cidades definidas pelo cliente, contendo empresas localizadas em fontes publicas, com nome da empresa, telefone, site, email quando disponivel, cidade, categoria e status de qualificacao.

## Campos recomendados na planilha final

A planilha Excel final deve conter, no minimo:

- Nome da empresa
- Categoria/nicho
- Cidade
- Bairro, quando disponivel
- Endereco
- Telefone
- Site
- Email encontrado
- Tipo de email, quando aplicavel
- Fonte do dado
- Score de qualificacao
- Status do lead
- Observacoes

Tambem pode ser interessante incluir:

- Avaliacao no Google
- Quantidade de avaliacoes
- Link do Google Maps, se implementado
- Data da coleta
- Rodada/campanha de coleta

## O que ainda precisa ser implementado

Para transformar o projeto em uma entrega comercial mais redonda, ainda faltam algumas evolucoes.

### 1. Parametrizacao por cliente

Hoje as categorias, cidades e bairros ficam definidos diretamente no `config.py`.

Para uso comercial, o ideal e permitir configurar cada projeto de cliente sem alterar o codigo.

Implementar:

- Arquivo de configuracao por cliente em JSON, YAML ou CSV.
- Lista customizada de categorias/nichos.
- Lista customizada de cidades.
- Lista opcional de bairros por cidade.
- Nome do cliente ou projeto para separar os outputs.

### 2. Exportacao real em Excel

Hoje o projeto exporta arquivos `.csv`, que podem ser abertos no Excel, mas ainda nao gera um arquivo `.xlsx` formatado.

Implementar:

- Exportacao para `.xlsx`.
- Uma aba geral com todos os leads.
- Abas separadas por categoria ou por cidade.
- Aba de resumo com totais por categoria, cidade e status.
- Cabecalhos formatados.
- Filtros ativados na planilha.
- Congelamento da primeira linha.
- Largura automatica das colunas.

### 3. Organizacao dos outputs por projeto

Hoje os arquivos sao gerados diretamente em `outputs/`.

Para entregas comerciais, o ideal e separar cada execucao por cliente, data ou campanha.

Implementar:

- Pasta por cliente/projeto.
- Pasta por data de execucao.
- Nome padronizado do arquivo final, por exemplo:
  - `outputs/cliente_x/2026-05-08/leads_cliente_x.xlsx`
  - `outputs/cliente_x/2026-05-08/resumo_execucao.md`

### 4. Melhor tratamento de cidades e bairros

Hoje o projeto esta desenhado principalmente para Curitiba e algumas cidades da RMC.

Para vender para clientes com outras regioes, precisa evoluir:

- Suporte a multiplas cidades e estados.
- Bairros opcionais por cidade.
- Busca sem bairro quando o cliente quiser apenas cidade/categoria.
- Registro correto da cidade e bairro de origem de cada busca.

### 5. Mais dados na exportacao

O projeto ja coleta alguns dados que ainda podem ser melhor aproveitados nos arquivos finais.

Implementar ou revisar:

- Exportar endereco completo.
- Exportar rating do Google.
- Exportar quantidade de avaliacoes.
- Exportar query de origem.
- Exportar site e telefone de forma consistente.
- Corrigir ou padronizar o campo de site salvo no SQLite.
- Incluir data da coleta.

### 6. Relatorio resumido da coleta

Para uma entrega profissional, alem da planilha, e util entregar um resumo executivo.

Implementar:

- Total de empresas encontradas.
- Total de empresas unicas.
- Total com telefone.
- Total com site.
- Total com email.
- Total sem email.
- Total por categoria.
- Total por cidade.
- Observacoes sobre disponibilidade dos dados.

### 7. Controle de volume e custo

Como a Google Places API pode gerar custo conforme o volume, o projeto precisa permitir limites por entrega.

Implementar:

- Limite maximo de resultados por categoria.
- Limite maximo de cidades por rodada.
- Estimativa de chamadas de API antes da execucao.
- Modo de simulacao sem chamar a API.
- Log de execucao com quantidade de buscas feitas.

### 8. Melhorias de confiabilidade

Para uso comercial recorrente, vale aumentar a robustez do pipeline.

Implementar:

- Logs em arquivo.
- Tratamento mais detalhado de erros por empresa/site.
- Retomada de execucao interrompida.
- Validacao de emails encontrados.
- Normalizacao de telefones.
- Remocao de duplicidades por telefone, dominio ou nome similar, alem do `place_id`.

## Pontos que nao devem ser prometidos como garantia

Na proposta comercial, evitar prometer:

- Email de todas as empresas.
- Telefone de todas as empresas.
- Base 100% completa.
- Dados privados ou dados nao publicados.
- Garantia de conversao comercial.
- Garantia de que todos os dados estejam atualizados em tempo real.

O correto e prometer:

- Coleta de dados publicos disponiveis.
- Organizacao e classificacao dos registros encontrados.
- Email quando estiver publicado em fonte acessivel.
- Telefone quando estiver disponivel via Google Maps ou site.
- Entrega estruturada em planilha.
- Segmentacao conforme categorias e cidades combinadas.

## Texto sugerido para proposta

Segue um texto seguro para uso em proposta comercial:

> O projeto contempla o mapeamento de empresas em categorias e cidades definidas pelo cliente, utilizando fontes publicas e APIs oficiais para identificacao e organizacao dos dados. A entrega sera realizada em planilha Excel, contendo nome da empresa, categoria, cidade, site, telefone, email quando disponivel publicamente e status de qualificacao. A disponibilidade de telefone e email depende das informacoes publicadas pelas empresas nas fontes consultadas.

## Fase recomendada apos aprovacao do cliente

Se o cliente aprovar a proposta, a evolucao tecnica recomendada e:

1. Definir categorias, cidades e volume esperado com o cliente.
2. Criar arquivo de configuracao customizado por cliente.
3. Ajustar o pipeline para aceitar configuracao externa.
4. Implementar exportacao `.xlsx` com abas e resumo.
5. Rodar um teste com volume reduzido.
6. Validar qualidade da base.
7. Executar coleta completa.
8. Entregar planilha final e resumo da execucao.

## Resumo

O projeto ja possui a estrutura principal para coleta e qualificacao de empresas locais, mas ainda precisa evoluir a parametrizacao, exportacao em Excel, organizacao por cliente e relatorio de entrega para se tornar um produto comercial completo.

Com essas melhorias, ele pode ser oferecido como um servico de geracao de base qualificada por categoria e cidade, com entrega clara, auditavel e adequada para uso comercial responsavel.
