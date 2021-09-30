import pandas as pd
import os


def cria_df_estoque(diretorio_excel):
    global codigo, descricao, grupo, subgrupo, estoque, estoque_min
    excel_estoque = pd.read_excel(diretorio_excel)

    df = pd.DataFrame(excel_estoque)
    df_novo = pd.DataFrame()

    for colunas in df.columns:
        if df.iloc[5][colunas] == "Código":
            codigo = colunas
        if df.iloc[5][colunas] == "Descrição":
            descricao = colunas
        if df.iloc[5][colunas] == "Grupo":
            grupo = colunas
        if df.iloc[5][colunas] == "SubGrupo":
            subgrupo = colunas
        if df.iloc[5][colunas] == "Estoque":
            estoque = colunas
        if df.iloc[5][colunas] == "Estoque Mínimo":
            estoque_min = colunas
    try:
        df_novo['Código'] = df[codigo]
        df_novo['Descrição'] = df[descricao]
        df_novo['Grupo'] = df[grupo]
        df_novo['SubGrupo'] = df[subgrupo]
        df_novo['Estoque'] = df[estoque]
        df_novo['Estoque Mínimo'] = df[estoque_min]

    except ValueError:
        assert Exception("Uma ou mais colunas não foram encontradas")
    except:
        assert Exception("Uma ou mais colunas não foram encontradas")

    df_novo.dropna(inplace=True)
    return df_novo.drop(5)


def cria_df_vendas(diretorio_excel):
    global codigo, quantidade
    excel_vendas = pd.read_excel(diretorio_excel)

    df = pd.DataFrame(excel_vendas)
    df_novo = pd.DataFrame()

    for colunas in df.columns:
        if df.iloc[5][colunas] == "Código":
            codigo = colunas
        if df.iloc[5][colunas] == "Qtd":
            quantidade = colunas

    df_novo['Código'] = df[codigo]
    df_novo['Vendas'] = df[quantidade]

    df_novo.dropna(inplace=True)
    return df_novo.drop(5)


def cria_estimativa_de_compra(dias=14):
    print('Gerando Tabelas...')
    try:
        df_estoque = cria_df_estoque('estoque.xls')
        df_vendas = cria_df_vendas('vendas.xls')
        print('Gerando Tabelas...OK')
    except FileNotFoundError:
        raise Exception('Um ou mais diretorios invalidos')
    except:
        raise Exception('Erro ao gerar Tabelas')

    print('Unificando Tabelas...')
    try:
        df_analise = pd.merge(df_estoque, df_vendas, how="left", on="Código")
        df_analise.dropna(inplace=True)
        print('Unificando Tabelas...OK')
    except ValueError:
        raise Exception('Tabelas não encontradas')
    except:
        raise Exception('Erro ao unificar Tabelas')

    df_final = cria_colunas(df_analise, dias)

    print('Criando excel')
    criarExcel(df_final)


def criarExcel(df_final):
    if not os.path.exists('db'):
        os.makedirs('db')

    df_final.to_excel('db/analise_db.xlsx')


def cria_colunas(df_analise, dias):
    print('Criando colunas de analise...')
    try:
        df_analise['Estimativa de Compra'] = (df_analise['Estoque Mínimo'] + df_analise['Vendas']) - df_analise[
            'Estoque']
        nao_compra = df_analise['Estimativa de Compra'] > 0
        df_analise['Estimativa de Compra'] = df_analise['Estimativa de Compra'].where(nao_compra, 0)
        df_analise['Média de Vendas'] = df_analise['Vendas'] / dias
        df_analise['Dias de Estoque'] = df_analise['Estoque'] / df_analise['Média de Vendas']
        print('Criando colunas de analise...OK')
        return df_analise
    except ZeroDivisionError:
        raise Exception('Valores de colunas = 0')
    except TypeError:
        raise Exception('Valores das colunas não são numericos')
    except:
        raise Exception('Erro ao criar colunas de analise')


if __name__ == '__main__':
    cria_estimativa_de_compra()
