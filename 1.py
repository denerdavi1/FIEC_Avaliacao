import pandas as pd
import numpy as np
from datetime import date
import requests


#ITEM a)

#Receber o ano atual
data_atual = date.today()
ano = data_atual.year

#transformar ano em Inteiro
ano = int(ano)

#últimos 3 anos
ano1 = ano -1
ano2 = ano -2
ano3 = ano -3

#transformar em String
ano1 = str(ano1)
ano2 = str(ano2)
ano3 = str(ano3)

#Dados de Importações
url1 = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/IMP_"+ano1+".csv"
imp1 = pd.read_csv(url1)

url2 = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/IMP_"+ano2+".csv"
imp2 = pd.read_csv(url2)

url3 = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/IMP_"+ano3+".csv"
imp3 = pd.read_csv(url3)

#Dados de Exportação
url4 = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_"+ano1+".csv"
exp1 = pd.read_csv(url4)

url5 = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_"+ano2+".csv"
exp2 = pd.read_csv(url5)

url6 = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/IMP_"+ano3+".csv"
exp3 = pd.read_csv(url6)

#ITEM b)

url1.columns = ['ANO', 'MES', 'COD_NCM', 'COD_UNIDADE', 'COD_PAIS', 'SG_UF',
'COD_VIA', 'COD_URF', 'VL_QUANTIDADE', 'VL_PESO_KG',
'VL_FOB']

url2.columns = ['ANO', 'MES', 'COD_NCM', 'COD_UNIDADE', 'COD_PAIS', 'SG_UF',
'COD_VIA', 'COD_URF', 'VL_QUANTIDADE', 'VL_PESO_KG',
'VL_FOB']

url3.columns = ['ANO', 'MES', 'COD_NCM', 'COD_UNIDADE', 'COD_PAIS', 'SG_UF',
'COD_VIA', 'COD_URF', 'VL_QUANTIDADE', 'VL_PESO_KG',
'VL_FOB']

url4.columns = ['ANO', 'MES', 'COD_NCM', 'COD_UNIDADE', 'COD_PAIS', 'SG_UF',
'COD_VIA', 'COD_URF', 'VL_QUANTIDADE', 'VL_PESO_KG',
'VL_FOB']

url5.columns = ['ANO', 'MES', 'COD_NCM', 'COD_UNIDADE', 'COD_PAIS', 'SG_UF',
'COD_VIA', 'COD_URF', 'VL_QUANTIDADE', 'VL_PESO_KG',
'VL_FOB']

url6.columns = ['ANO', 'MES', 'COD_NCM', 'COD_UNIDADE', 'COD_PAIS', 'SG_UF',
'COD_VIA', 'COD_URF', 'VL_QUANTIDADE', 'VL_PESO_KG',
'VL_FOB']
