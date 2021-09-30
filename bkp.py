import math

import numpy as np
import pandas as pd


class Colunas:
    nome = {
            'codigo': 'Código',
            'estoque': 'Estoque',
            'descricao': 'Descrição',
            'media_vendas': 'Média de Vendas',
            'estimativa': 'Estimativa de Compra',
            'dias_restantes': 'Dias Restantes de Estoque',
            'vendas': 'Vendas',
    }


# colunas
# 0 - codigo
# 1 - descricao
# 7 - valor unitario
# 8 - quantidade
# 10 - subtotal
# 12 - desconto
# 13 - acresimo
# 15 - total
# linhas
# 5 - cabecario
# 6 - conteudo inicio
# 6+n - conteudo vazio


# excel1 = pd.read_excel('estoque.xls')
# excel2 = pd.read_excel('vendas.xls')
excel1 = pd.read_excel('1.xls')
excel2 = pd.read_excel('2.xls')
dia = 14

df_estoque = pd.DataFrame(excel1)
df_vendas = pd.DataFrame(excel2)


def limpa_excell(dataframe: pd.DataFrame, nome):
    dataframe.dropna(subset=['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 8'], inplace=True)
    dataframe: pd.DataFrame = dataframe.drop(
        columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7',
                 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14',
                 'Unnamed: 15'], index=5)
    return dataframe.rename(columns={'Unnamed: 0': Colunas.nome['codigo'], 'Unnamed: 1': Colunas.nome['descricao'], 'Unnamed: 8': nome})


df_estoque_limpo = limpa_excell(df_estoque, Colunas.nome['estoque'])
df_vendas_limpo = limpa_excell(df_vendas, Colunas.nome['vendas'])

df_analise_compra = pd.merge(df_estoque_limpo, df_vendas_limpo, how="left", on=[Colunas.nome['codigo'],Colunas.nome['descricao']])
df_analise_compra.dropna(subset=[Colunas.nome['vendas']], inplace=True)

df_analise_compra[Colunas.nome['estimativa']] = (df_analise_compra[Colunas.nome['vendas']] - df_analise_compra[Colunas.nome['estoque']])

nao_compra = df_analise_compra[Colunas.nome['estimativa']] > 0

df_analise_compra[Colunas.nome['estimativa']] = df_analise_compra[Colunas.nome['estimativa']].where(nao_compra, 0)

df_analise_compra[Colunas.nome['media_vendas']] = df_analise_compra[Colunas.nome['vendas']] / dia
df_analise_compra[Colunas.nome['dias_restantes']] = df_analise_compra[Colunas.nome['estoque']] / df_analise_compra[Colunas.nome['media_vendas']]

df_analise_compra.to_excel('estimatica_de_compra.xlsx')
print(df_analise_compra.head(10))
