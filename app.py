##### Importando Modulos ####

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_table
import numpy as np
import pandas as pd
import openpyxl
import datetime
from datetime import datetime as dt
import pathlib

import plotly.graph_objects as go

##### Criando App e Server #####

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server
app.config.suppress_callback_exceptions = True

usar_base_bruta = False

##### Lendo as bases de dados #####

d_sh2 = pd.read_excel('data/d_sh2.xlsx', engine='openpyxl')
d_sh2.columns = ['COD_NCM', 'NM_NCM', 'COD_SH2', 'NM_SH2']

d_via = pd.read_excel('data/d_via.xlsx', engine='openpyxl')
d_via.columns = ['COD_VIA', 'NM_VIA']

if usar_base_bruta:

    f_comex = pd.read_csv('data/f_comex_.csv', sep = ';')
    f_comex = f_comex.merge(d_sh2[['COD_NCM', 'COD_SH2']], on = 'COD_NCM', how = 'inner')

    f_comex = f_comex.groupby(['ANO', 'MES', 'MOVIMENTACAO', 'SG_UF', 'COD_VIA', 'COD_SH2']).agg(VL_FOB = ('VL_FOB', 'sum')).reset_index()

    f_comex.to_csv('data/f_comex.csv', index = False, sep = ';')

else:

    f_comex = pd.read_csv('data/f_comex.csv', sep = ';')  

##### Criando controles para filtro #####

# SH2

aux_sh2 = d_sh2[['COD_SH2', 'NM_SH2']].drop_duplicates().copy()

sh2_options = [
    {"label": str(NM_SH2), "value": str(COD_SH2)} for COD_SH2, NM_SH2 in zip(aux_sh2['COD_SH2'], aux_sh2['NM_SH2'])
]

del aux_sh2

# VIA

via_options = [
    {"label": str(NM_VIA), "value": str(COD_VIA)} for COD_VIA, NM_VIA in zip(d_via['COD_VIA'], d_via['NM_VIA'])
]

# MOVIMENTAÇÃO

mov_options = [
    {"label": str(MOVIMENTACAO), "value": str(MOVIMENTACAO)} for MOVIMENTACAO in f_comex['MOVIMENTACAO'].drop_duplicates()
]

# ANO

year_options = [
    {"label": str(ANO), "value": str(ANO)} for ANO in f_comex['ANO'].drop_duplicates()
]

##### Criando Função de Descrição #####

def descricao():
    """
    :return: A Div contentando o titulo do DashBoard e uma breve descrição.
    """
    return html.Div(
        id="descricao",
        children=[
            html.H5("Comercio Exterior"),
            html.H3("Bem vindo ao relatório de comercio exterior do Observatorio da Indústria da FIEC."),
            html.Div(
                id = "intro",
                children = "Esse dash tem como principal objetivo ajudar na tomada de decisões relacionadas a importação e exportação de produtos.",
            ),
        ],
    )

##### Criando função de Filtros #####

def filtros():
    """
    :return: A Div contendo os filtros utilzados
    """
    return html.Div(
        id = "filtros",
        children = [

            # ANO

            html.P("Selecione o ANO"),
            dcc.Dropdown(
                id = "ano-filtro",
                options = year_options,
                value = dt.now().year - 1,
                clearable = False
            ),
            html.Br(),
            html.Br(),            
            
            # MOVIMENTO

            html.P("Selecione o MOVIMENTO"),
            dcc.Dropdown(
                id = "mov-filtro",
                options = mov_options,
                value = mov_options[0]['value'],
                clearable = False
            ),
            html.Br(),
            html.Br(),

            # SH2

            html.P("Seleciona o Grupo SH2"),
            dcc.Dropdown(
                id="sh2-filtro",
                options=sh2_options,
                value = np.nan,
                multi = True,
            ),
            html.Br(),
            html.Br(),

            # VIA

            html.P("Seleciona o Grupo VIA"),
            dcc.Dropdown(
                id="via-filtro",
                options=via_options,
                value = np.nan,
                multi = True,
            ),
            html.Br(),
            html.Br()
        ],
    )


##### Definindo Layout #####

app.layout = html.Div(
    id = "app",
    children = [

        # Cabeçalho

        html.Div(
            id = "cabecalho",
            className = "banner",
            children = [html.Img(src = app.get_asset_url('logo.png'))]
        ),

        # Coluna Esquerda

        html.Div(
            id = "coluna-esquerda",
            className = "four columns",
            children = [descricao(), filtros()]
        ),

        # Cards

        html.Div(
            [
                html.Div(
                    [html.H6(id = "total-importacao"), html.P("Valor Importado")],
                    id = "valor-importado",
                    className = "mini_container",
                ),
                html.Div(
                    [html.H6(id = "total-exportacao"), html.P("Valor Exportado")],
                    id = "valor-exportado",
                    className = "mini_container",
                )
            ]
        ),

        # Coluna Direita

        html.Div(
            id = "coluna-direita",
            className = "eight columns",
            children = [
                
                # Grafico de barra

                html.Div(
                    id = "grafico1",
                    children = [
                        html.B("Valor Financeira"),
                        html.Hr(),
                        dcc.Graph(id="grafico-valor-financeiro-mensal")
                    ]),

                # Grafico de pizza

                html.Div(
                    id = "grafico2",
                    children = [
                        html.B("Segmentação por VIA"),
                        html.Hr(),
                        dcc.Graph(id="grafico-via")
                    ]),

                # Tabela

                html.B("Comparação por Estado"),
                html.Hr(),
                dash_table.DataTable(
                    id='tabela-comparativa-por-estado',
                    columns=[{"name": i, "id": i} for i in ['Estado', 'Valor', 'Participação', 'Ano Anterior']]
                ),
            ],
        ),
    ],
)

@app.callback(
    Output("grafico-valor-financeiro-mensal", "figure"),
    Output("grafico-via", "figure"),
    [
        Input("ano-filtro", "value"),
        Input("mov-filtro", "value"),
        Input("sh2-filtro", "value"),
        Input("via-filtro", "value")
    ],
)
def atualizar_graficos(ano, mov, sh2, via):

    # Ano

    filtro_ano = (f_comex['ANO'].astype(str) == ano)

    # Movimentação

    filtro_mov = (f_comex['MOVIMENTACAO'].astype(str) == mov)

    # SH2

    filtro_sh2 = pd.Series([True for i in range(0, len(f_comex['COD_SH2']))])

    if sh2 != None:

        filtro_sh2 = (f_comex['COD_SH2'].isin(sh2))

    # Via

    filtro_via = pd.Series([True for i in range(0, len(f_comex['COD_VIA']))])

    if via != None:

        filtro_via = (f_comex['COD_VIA'].isin(via))

    # Aplicando Filtros

    aux = f_comex.loc[filtro_ano & filtro_mov & filtro_sh2 & filtro_via].copy()

    ##### Criando Gráfico de Barras ####

    aux1 = aux.groupby('MES').agg(Valor = ('VL_FOB', 'sum')).reset_index().rename(columns = {'MES': 'Mes'})

    fig1 = go.Figure(
        [
            go.Bar(
                x = aux1['Mes'], 
                y = aux1['Valor']
            )
        ]
    )

    ##### Criando Gráfico de Pizza #####

    aux2 = aux.groupby('COD_VIA').agg(Valor = ('VL_FOB', 'sum')).reset_index()
    aux2 = aux2.merge(d_via, on = 'COD_VIA', how = 'left')[['NM_VIA', 'Valor']].rename(columns = {'NM_VIA': 'Nome Via'})

    fig2 = go.Figure(
        data = [
            go.Pie(
                labels = aux2['Nome Via'], 
                values = aux2['Valor']
            )
        ]
    )

    return fig1, fig2


@app.callback(
    Output("tabela-comparativa-por-estado", "data"),
    Output("valor-importado", "children"),
    Output("valor-exportado", "children"),
    [
        Input("ano-filtro", "value"),
        Input("mov-filtro", "value"),
        Input("sh2-filtro", "value"),
        Input("via-filtro", "value")
    ],
)
def atualizar_tabela_e_cards(ano, mov, sh2, via):

    # Ano

    filtro_ano = (f_comex['ANO'].astype(str) == ano)

    # Movimentação

    filtro_mov = (f_comex['MOVIMENTACAO'].astype(str) == mov)

    # SH2

    filtro_sh2 = pd.Series([True for i in range(0, len(f_comex['COD_SH2']))])

    if sh2 != None:

        filtro_sh2 = (f_comex['COD_SH2'].isin(sh2))

    # Via

    filtro_via = pd.Series([True for i in range(0, len(f_comex['COD_VIA']))])

    if via != None:

        filtro_via = (f_comex['COD_VIA'].isin(via))

    # Aplicando Filtros

    aux_base0 = f_comex.loc[filtro_ano & filtro_sh2 & filtro_via].copy()
    aux_base = aux_base0.loc[filtro_mov].copy()

    aux = aux_base.groupby(['SG_UF']).agg(Valor = ('VL_FOB', 'sum')).reset_index().rename(columns = {'SG_UF': 'Estado'})

    aux['Participação'] = round(aux['Valor']*100/aux['Valor'].sum(),2)

    # Montando variáveis de participação no Ano Anterior

    base_ano_anterior_comex = f_comex.loc[(f_comex['ANO'] == int(ano)  - 1) & filtro_mov & filtro_sh2 & filtro_via].copy()

    base_ano_anterior_comex_group = base_ano_anterior_comex.groupby(['SG_UF']).agg(Valor = ('VL_FOB', 'sum')).reset_index().rename(columns = {'SG_UF': 'Estado'})

    base_ano_anterior_comex_group['Ano Anterior'] = round(base_ano_anterior_comex_group['Valor']*100/base_ano_anterior_comex_group['Valor'].sum(),2)

    # Montando tabela final

    aux = aux.merge(base_ano_anterior_comex_group[['Estado', 'Ano Anterior']], on = 'Estado', how = 'left')

    return aux.to_dict('records'), aux_base0.loc[aux_base0['MOVIMENTACAO'] == "Importação", 'VL_FOB'].sum(), aux_base0.loc[aux_base0['MOVIMENTACAO'] == "Exportação", 'VL_FOB'].sum()

if __name__ == '__main__':

    app.run_server(debug=True)

