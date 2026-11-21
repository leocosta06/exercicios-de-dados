import pandas as pd

#       planilha com os dados da Bemol 
df  = pd.read_excel("base_dados_intermediario.xlsx") 

#       Funções pra formatar os valores

# transforma 1234.5 em "1.234,50"
def reais(valor):
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return texto

 # transforma 25.0543 em "25,05%".
def porcento(valor):
    return f"{valor:.2f}".replace(".", ",") + "%"

#       Limpeza dos dados

# Primeiro dei uma olhada geral na base pra ver os tipos das colunas e
# se tinha valor vazio:
# print(df.info())
# print(df.isna().sum())
# Resultado: nenhuma coluna com valor vazio, mas "Valor Unitário" aparece
# como texto (object) e não como número, então tem algo estranho nela.
 
# Olhando os valores dessa coluna, percebi que algumas linhas vieram com
# vírgula no lugar do ponto, por isso o Python não reconhece como número. Troco a vírgula por ponto e converto:

colunas_numericas = ["Valor Unitário", "Qtd", "Valor Total"]
for col in colunas_numericas:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.strip().str.replace(",", ".", regex=False),
        errors="coerce"
    )
# recalcula para garantir
df["Valor Total"] = df["Valor Unitário"] * df["Qtd"] 

# depois conferi se o Valor Total bate com Valor Unitário x Qtd:
# print((df["Valor Unitário"] * df["Qtd"] - df["Valor Total"]).abs().max())
# a diferença deu praticamente zero, então os valores estão consistentes.
 
# agora os nomes dos produtos. Usei o value_counts pra ver quantas vezes cada um aparece:
# print(df["Produto"].value_counts())
# tinha 30 nomes diferentes, mas alguns apareciam poucas vezes e eram
# quase iguais a outros (ex: "geledeire" com 39 e "geladeira" com 568).
# são erros de digitação, então corrigi pelos nomes certos

produtos_errados = {
    "geledeire": "geladeira",
    "micro-ondes": "micro-ondas",
    "mese de jenter": "mesa de jantar",
    "ermário de cozinhe": "armário de cozinha",
    "liquidificedor": "liquidificador",
    "senduicheire": "sanduicheira",
    "cefeteire": "cafeteira",
    "ferro de pesser": "ferro de passar",
    "impressore": "impressora",
    "tecledo": "teclado",
    "eir fryer": "air fryer",
}
df["Produto"] = df["Produto"].replace(produtos_errados)

# conferindo se deu certo:
# print(df["Produto"].nunique())
 
# fiz o mesmo com as outras colunas de texto e não achei erros:
# print(df["Unidade"].unique())      
# print(df["Categoria"].unique())    
# print(df["Cod_vendedor"].unique())  
 
# tirando duplicados e registros inválidos
# print(df.duplicated().sum()) 
# deu 0 duplicados, mas deixo o filtro por segurança

# remove linhas totalmente repetidas
df = df.drop_duplicates()

df = df.dropna(subset = ["Valor Unitário","Qtd","Valor Total"])

# filtro: mantém só as linhas onde Qtd, Valor Total e Valor Unitário são maiores que zero
df = df[(df["Qtd"] > 0) & (df["Valor Unitário"] > 0) & (df["Valor Total"] > 0)]


# pegando só o nome do vendedor (ex: "29854 - Fernando" vira "Fernando" não tem necessidade de usar o código do vendedor pra nada, então só deixo o nome):
df["Vendedor"] = df["Cod_vendedor"].str.split(" - ").str[1]

# salva a base tratada em um novo arquivo Excel 
df.to_excel("base_dados_tratada.xlsx", index=False)

#   QUESTÃO 1: Soma das vendas por unidade

print("1)")

total_unidade = df.groupby("Unidade")["Valor Total"].sum().sort_values(ascending=False)

for unidade,valor in total_unidade.items():
    print(f" Unidade: {unidade} | Total: R$ {reais(valor)}")

#   QUESTÃO 2: Unidade que mais vendeu e o produto mais vendido nela 

print("2)")

melhor_unidade = total_unidade.idxmax()

vendas_unidade = df[df["Unidade"] == melhor_unidade]

qtd_produtos = vendas_unidade.groupby("Produto")["Qtd"].sum().sort_values(ascending=False)

print(f"   Unidade: '{melhor_unidade}'")
print(f"   Produto: '{qtd_produtos.idxmax()}'") 
print(f"   Quantidade: {qtd_produtos.max()}")     
print(f"   Valor total da unidade: R$ {reais(total_unidade.max())}")

#   QUESTÃO 3: Vendedor que mais vendeu

print("3)")

total_vendedor = df.groupby("Vendedor")["Valor Total"].sum().sort_values(ascending=False)
print(f"   Vendedor: {total_vendedor.idxmax()}")
print(f"   Total: R$ {reais(total_vendedor.max())}")

#   QUESTÃO 4: Faturamento por categoria em cada centro

print("4)")

fat = df.groupby(["Centro", "Categoria"])["Valor Total"].sum().sort_values(ascending=False)

for (centro, categoria), valor in fat.items():
       print(f"   Centro: {centro} | Categoria: {categoria} | Valor Total: R$ {reais(valor)}")

#   QUESTÃO 5: Centro com maior ticket médio
print("5)")

ticket_medio = df.groupby("Centro")["Valor Total"].mean().sort_values(ascending=False)
print(f"   Centro: {ticket_medio.idxmax()}")
print(f"   Valor do ticket médio: R$ {reais(ticket_medio.max())}")

#   QUEASTÃO 6: Unidade com mais vendas > categoria > produto

print("6)")

num_vendas = df["Unidade"].value_counts().sort_values(ascending=False)
unidade = num_vendas.idxmax()
dados_unidade = df[df["Unidade"] == unidade]
categoria = dados_unidade.groupby("Categoria")["Qtd"].sum().sort_values(ascending=False).idxmax()

dados_categoria = dados_unidade[dados_unidade["Categoria"] == categoria]

qtd_produto = dados_categoria.groupby("Produto")["Qtd"].sum().sort_values(ascending=False)

print(f"   Unidade: {unidade}")
print(f"   Total de vendas: {num_vendas.max()}")
print(f"   Categoria: {categoria}")
print(f"   Produto: {qtd_produto.idxmax()}")
print(f"   Quantidade: {qtd_produto.max()}")

#   QUESTÃO 7: Maior diferença percentual entre 1º e 2º produto de cada centro

print("7)")

maior_dif = 0

for centro in df["Centro"].unique():
     produtos = df[df["Centro"] == centro].groupby("Produto")["Valor Total"].sum().sort_values(ascending=False)
     produtos = produtos.sort_values(ascending=False)

     primeiro = produtos.iloc[0]
     segundo = produtos.iloc[1]

     dif = (primeiro - segundo) / segundo * 100

     if dif > maior_dif:
          maior_dif = dif
          resposta = (centro, produtos.index[0], primeiro, produtos.index[1], segundo)

print(f"   Centro: {resposta[0]}")
print(f"   Produto: {resposta[1]}")
print(f"   Valor: R$ {reais(resposta[2])}")
print(f"   Segundo: {resposta[3]}")
print(f"   Valor total segundo colocado: R$ {reais(resposta[4])}")
print(f"   Diferença percentual: {porcento(maior_dif)}")

#   QUESTÃO 8:Percentual de cada categoria

print("8)")

total_geral = df["Valor Total"].sum()

total_categoria = df.groupby("Categoria")["Valor Total"].sum().sort_values(ascending=False)

for categoria, valor in total_categoria.items():
      print(f"   {categoria}: {porcento(valor / total_geral * 100)}")

#   QUESTÃO 9: Os 5 vendedores com menor desempenho

print("9)")

for vendedor, valor in total_vendedor.nsmallest(5).items():
    print(f"   Vendedor: {vendedor} | Total: R$ {reais(valor)}")

#   QUESTÃO 10:  Média de Qtd por venda em cada unidade

print("10)")
media = df.groupby("Unidade")["Qtd"].mean().sort_values(ascending=False)
for unidade, valor in media.items():
     print(f"    Unidade: {unidade} | Média: {valor:.2f}".replace(".", ","))