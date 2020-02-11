import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import bs4 as bs
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import urllib.request









pokemon = pd.read_csv('./pokemon_alopez247.csv')
pokemon.head()
colors = {
    "Bug": "#A6B91A",
    "Dark": "#705746",
    "Dragon": "#6F35FC",
    "Electric": "#F7D02C",
    "Fairy": "#D685AD",
    "Fighting": "#C22E28",
    "Fire": "#EE8130",
    "Flying": "#A98FF3",
    "Ghost": "#735797",
    "Grass": "#7AC74C",
    "Ground": "#E2BF65",
    "Ice": "#96D9D6",
    "Normal": "#A8A77A",
    "Poison": "#A33EA1",
    "Psychic": "#F95587",
    "Rock": "#B6A136",
    "Steel": "#B7B7CE",
    "Water": "#6390F0",
}


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',"/assets/hover.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[

    html.H1(children="Pokemon Assignment"),



    html.Div(
                dcc.Dropdown(
                    id = "poke1",
                    options=[{"label": i,"value": i} for i in pokemon["Name"].unique()],
                    value="Bulbasaur"
                ),style={'width': '48%', 'display': 'inline-block'}
            ),
    html.Div(
                dcc.Dropdown(
                    id = "poke2",
                    options=[{"label": i,"value": i} for i in pokemon["Name"].unique()],
                    value="Pikachu"
                ),style={'width': '48%', 'display': 'inline-block'}
            ),
    html.Div(children=[
        html.Img(id="image1",className="simage",style={'float':'left','width':'300px','height':'300px'}),
        dcc.Graph(
            id="stats",style={'float':'left'}),
        html.Img(id="image2",className="bimage",style={'float':'left','width':'300px','height':'300px'})
    ])
])
@app.callback(
    Output('image1','src'),
    [Input("poke1",'value')]

)
def get_image_url(name):
    sauce = urllib.request.urlopen("https://www.pokemon.com/us/pokedex/"+name).read()

    soup = bs.BeautifulSoup(sauce, "lxml")

    for image in soup.find_all("img", {"class": "active"}):
        url = image['src']
        break

    return url
@app.callback(
    Output('image2','src'),
    [Input("poke2",'value')]

)
def get_image_url(name):
    sauce = urllib.request.urlopen("https://www.pokemon.com/us/pokedex/"+name).read()

    soup = bs.BeautifulSoup(sauce, "lxml")

    for image in soup.find_all("img", {"class": "active"}):
        url = image['src']
        break

    return url
def polar_pokemon_stats(pkmn_name):

    pkmn = pokemon[pokemon.Name == pkmn_name]
    obj = go.Scatterpolar(
        r=[
            pkmn['HP'].values[0],
            pkmn['Attack'].values[0],
            pkmn['Defense'].values[0],
            pkmn['Sp_Atk'].values[0],
            pkmn['Sp_Def'].values[0],
            pkmn['Speed'].values[0],
            pkmn['HP'].values[0]
        ],
        theta=[
            'HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed', 'HP'
        ],
        fill='toself',
        marker=dict(
            color=colors[pkmn['Type_1'].values[0]]
        ),
        name=pkmn['Name'].values[0]
    )

    return obj

@app.callback(
    Output("stats","figure"),
    [Input("poke1",'value'),
     Input("poke2",'value')]
)
def plot_pokemon_comparison(name1, name2):
    names = [name1, name2]
    name_str = ",".join(names)
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 250]
            )
        ),
        showlegend=False,
        title="Stats of {}".format(name_str)
    )
    plot_pokelist = []
    for name in names:
        plot_pokelist.append(polar_pokemon_stats(name))

    pokemon_figure = go.Figure(data=plot_pokelist, layout=layout)
    return pokemon_figure
# name = 'Charmander'
# plot_single_pokemon(name)


if __name__ == '__main__':
    app.run_server(debug=True)



