import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
import pandas as pd
import plotly.express as px

# =====================
# LEITURA E TRATAMENTO
# =====================
df = pd.read_csv("Netflix.csv")
df = df[df['type'] == 'Movie']

# Quantidade de filmes
qtd_filmes = df.shape[0]

# Top 10 gêneros mais comuns
generos_series = df['genres'].dropna().str.split(', ').explode()
top_generos = generos_series.value_counts().nlargest(10).reset_index()
top_generos.columns = ['Gênero', 'Contagem']

# Top 10 filmes com maior receita
top_receita = df[['title', 'revenue']].dropna().sort_values(by='revenue', ascending=False).head(10)

# Top 10 filmes mais populares
top_populares = df[['title', 'popularity']].dropna().sort_values(by='popularity', ascending=False).head(10)

# ==============
# DASHBOARD APP
# ==============
app = dash.Dash(_name_, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Netflix Dashboard"

# Temas
tema_claro = dbc.themes.PULSE
tema_escuro = dbc.themes.CYBORG
claro = "pulse"
escuro = "cyborg"

# ==========
# LAYOUT APP
# ==========
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Netflix Dashboard", className="text-center mb-4 mt-2"), width=10),
        dbc.Col(ThemeSwitchAIO(aio_id="tema", themes=[tema_claro, tema_escuro]), width=2)
        
    ]),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Quantidade Total de Filmes"),
            dbc.CardBody(html.H3(f"{qtd_filmes}", className="card-title text-center"))
        ], className="mb-4"), width=12)
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id = 'grafico1'))
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id = 'grafico2'))
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id = 'grafico3'))
    ])
], fluid=True)



@app.callback(Output('grafico1','figure'),
              Input(ThemeSwitchAIO.ids.switch ('tema'), 'value'),
              )
def grafico1(tema):
    template = claro if tema else escuro
    fig = px.bar(top_generos, x='Contagem', y='Gênero', orientation='h',
                                        title='Top 10 Gêneros Mais Comuns', color = 'Gênero',template = template)
    return fig
    



@app.callback(Output('grafico2','figure'),
              Input(ThemeSwitchAIO.ids.switch ('tema'), 'value'),
              )
def grafico2(tema):
    template = claro if tema else escuro
    fig = px.bar(top_receita, x='revenue', y='title', orientation='h',
                                        title='Top 10 Filmes com Maior Receita', color = 'title',template = template)
    return fig


@app.callback(Output('grafico3','figure'),
              Input(ThemeSwitchAIO.ids.switch ('tema'), 'value'),
              )
def grafico3(tema):
    template = claro if tema else escuro
    fig = px.bar(top_populares, x='title', y='popularity',
                                        title='Top 10 Filmes Mais Populares', color = 'title',template = template)
    return fig



if _name_ == '_main_':
    app.run(debug=True, port=8051)