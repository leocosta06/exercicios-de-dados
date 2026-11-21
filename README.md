# exercícios de dados
# Análise de Vendas com Python e Pandas

Solução de um desafio de análise de dados em Python: a partir de uma base fictícia de vendas de uma loja de varejo, o script limpa os dados e responde 10 perguntas de negócio (faturamento, ticket médio, ranking de vendedores, participação por categoria etc.).

## Tecnologias

- Python 3
- [pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/) (leitura de arquivos `.xlsx`)

## Como rodar

1. Instale as dependências:

   ```bash
   pip install pandas openpyxl
   ```

2. Coloque a planilha de vendas na mesma pasta do script, com o nome `base_dados_intermediario.xlsx`.

   > A base não está neste repositório. Ela foi fornecida junto com o desafio.

3. Execute:

   ```bash
   python analise_vendas.py
   ```

O resultado de cada pergunta é impresso no terminal, numerado de 1 a 10.

## Estrutura da base

| Coluna | Descrição |
|---|---|
| Centro | Código do centro de vendas |
| Unidade | Unidade (loja) onde ocorreu a venda |
| Categoria | Categoria do produto |
| Produto | Nome do produto |
| Valor Unitário | Preço de cada unidade |
| Cod_vendedor | Código e nome do vendedor (ex.: `12345 - Nome`) |
| Qtd | Quantidade vendida |
| Data_compra | Data da venda |
| Valor Total | Valor total da venda |

## Limpeza dos dados

Antes de responder às perguntas, inspecionei a base e encontrei dois problemas:

- **Valor Unitário como texto:** algumas linhas vinham com vírgula decimal (ex.: `"1934,76"`), o que fazia a coluna inteira ser lida como texto. Troquei a vírgula por ponto e converti para número.
- **Erros de digitação nos produtos:** 11 nomes estavam escritos errado (ex.: `geledeire` em vez de `geladeira`). Usei `value_counts()` para identificá-los, já que apareciam poucas vezes e eram quase iguais a nomes corretos, e corrigi com um dicionário de substituição.

Também verifiquei valores vazios, duplicados e valores zerados ou negativos, e confirmei que `Valor Total` é consistente com `Valor Unitário × Qtd`. As demais colunas de texto não tinham inconsistências.

Por fim, criei a coluna `Vendedor` (só o nome) a partir de `Cod_vendedor`.

## Perguntas respondidas

1. Soma do valor total de vendas por unidade
2. Unidade com maior faturamento, produto mais vendido nela (em quantidade) e valor total
3. Vendedor com maior total de vendas
4. Faturamento por categoria em cada centro
5. Centro com maior ticket médio
6. Unidade com mais vendas, categoria mais vendida nela e produto mais vendido na categoria
7. Maior diferença percentual entre o 1º e o 2º produto mais vendidos (em valor) de cada centro
8. Percentual de cada categoria no total de vendas
9. Os 5 vendedores com menor desempenho
10. Média de itens por venda em cada unidade

## Decisões de interpretação

- **Pergunta 6:** considerei "número de vendas" como a contagem de registros (cada linha é uma compra) e "mais vendido" como a soma da coluna `Qtd`.
- **Ticket médio (pergunta 5):** valor médio de `Valor Total` por registro, já que cada linha representa uma compra.
- **Pergunta 9:** a base possui apenas 5 vendedores, então a lista contém todos, do menor para o maior total.

## Aprendizados

- Uso de `groupby`, `idxmax`, `nsmallest` e filtros encadeados no pandas.
- Importância de inspecionar os dados (`info`, `value_counts`, `unique`) antes de analisar.
- Formatação de números no padrão brasileiro (`1.234,50`) em Python.
