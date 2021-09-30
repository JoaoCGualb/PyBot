import pandas as pd


excel = pd.read_excel('1.xls')

excel_estoque = pd.DataFrame(excel)

excel_estoque.to_excel('fmoiemiemi.xls')