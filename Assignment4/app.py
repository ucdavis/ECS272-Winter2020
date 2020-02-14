import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
import random
import csv
import json
import os



#Style Sheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__ , external_stylesheets = external_stylesheets)
cssURL = "https://rawgit.com/richard-muir/uk-car-accidents/master/road-safety.css"
app.css.append_css({
    "external_url": cssURL
})
#Read CSV
df = pd.read_csv('pokemon/pokemon_alopez247.csv')

names = df['Name']
num = ['1','2','3','4','5','6','7','8','9','10']
#nearest = []
#Drop down for second graph
option_list = ["Attack", "Defense", "Speed", "Catch_Rate"]
#pokemon_names = []
FONT_FAMILY =  "Arial" 
#App Layout
app.layout = html.Div(children=[
    html.H1(children = "PokeDex",style={
            'paddingLeft' : '14em',
            'fontFamily' : FONT_FAMILY
            }),
    html.H3(children= "Assignment 4",style={
            'paddingLeft' : '21em',
            'fontFamily' : FONT_FAMILY
            }),
    html.H3(children= "Ishan Jain, Sanjat Mishra, Kavish Doshi",style={
            'paddingLeft' : '17em',
            'fontFamily' : FONT_FAMILY,
            'paddingBottom':'1em'
            }),
    html.Div([
        html.Label('Select number of clusters'),
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': i, 'value': i} for i in num
            ],
            value='2'
        ),
        html.Label('Select a pokemon'),
        dcc.Dropdown(
            id='dropdown2',
            options=[
                {'label': i, 'value': i} for i in names
            ],
            value='Venusaur',
        ),
    ],
        style={
            "width": '90%',
            'paddingLeft': '4em',
            'paddingBottom':'1em' ,
            'display':'inline-block',
        }
    ),
    html.Div(
        className="Pokemon Viz",
        children=[
            dcc.Graph(id="output-graph", style={"height": "26em","paddingBottom":'2em','float':'left','width':'30%','paddingRight':'2em'})
        ]
    ),
    html.Div([
        dcc.Dropdown(
            id='option_dropdown',
            options=[
                {'label': i, 'value': i} for i in option_list
            ],
            value=["Attack"]
        )
    ],
        style={
            "width": '23%',
            'display': 'inline-block',
            'paddingLeft': '0em',
            'boxSizing': 'border-box',
        }
    ),
    html.Div(
        children=[
            html.Div(
                id='list',
                children=[
                    dcc.Checklist(id="pokemonCheck", value = [],
                    labelStyle = {
                        'display':'inline-block',
                        'paddingRight':'1em'
                    }
                    )
                ])
            ]
    ),

    html.Div(
        id = 'output-graph1',
        style = {
        
        'width' : '33%',
        'display' : 'inline-block',
        'boxSizing' : 'border-box',
        'fontFamily' : "Arial",
        'float':'left',
        "height": "20em"

        }
    ),

    html.Div(
        id='intermediate-value',
        style = {
            'display' : 'none'
        }
    ),


    html.Div([
        dcc.Graph(
            id='radar-graph'
        )
    ],
    style={
        'width' : '30%',
        'display' : 'inline-block',
        'paddingRight': '0em',
        'boxSizing' : 'border-box',
        'fontFamily' : "Arial",
        'float':'right',
        "height": "20em"
    },

    )

])

@app.callback(
    Output(component_id='output-graph', component_property='figure'),
    [Input(component_id='dropdown', component_property='value'),
    Input(component_id='dropdown2', component_property='value')]
)
def update_graph(no_of_clusters, pokemon):
    
    x = df.iloc[:, [6,7,10]].values
    names = df.iloc[:, 1].values
    kmeans5 = KMeans(n_clusters=int(no_of_clusters))
    y_kmeans5 = kmeans5.fit_predict(x)
    #a = kmeans5.cluster_centers_
    index = np.nonzero(names == pokemon)
    cluster_nu = y_kmeans5[index]
    itemindex = np.where(y_kmeans5==cluster_nu)
    a = [item for item in itemindex]
    nearest = random.sample(list(a[0]), 5)
    #print(nearest)
    pokemon_names = []
    for i in nearest:
        pokemon_names.append(names[i])
    #print(pokemon_names)
    with open('names.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(pokemon_names)

    data = []
    xaxes = dict(title="x: Attack", showgrid=True, zeroline=True, showticklabels=True)
    yaxes = dict(title="y: Defence", showgrid=True, zeroline=True, showticklabels=True)
    zaxes = dict(title="z: Speed", showgrid=True, zeroline=True, showticklabels=True)
    layout = go.Layout(
                margin=dict(l=0, r=0, b=0, t=0),
                scene=dict(xaxis=xaxes, yaxis=yaxes, zaxis=zaxes),
            )
        
    scatter = go.Scatter3d(
        name="Pokemon Clustering",
        x=[x[i][0] for i in range(len(y_kmeans5))],
        y=[x[i][1] for i in range(len(y_kmeans5))],
        z=[x[i][2] for i in range(len(y_kmeans5))],
        text=[("Pokemon: "+names[i]) for i in range(len(names))],
        textposition="top center",
        mode="markers",
        marker=dict(size=3, symbol="circle", color = y_kmeans5, colorscale='Blackbody',),
    )
    data.append(scatter)
    figure = go.Figure(data=data, layout=layout)

    return figure

@app.callback(Output('intermediate-value', 'children'),
    [Input(component_id='dropdown', component_property='value'),
    Input(component_id='dropdown2', component_property='value')])

def intermediate(no_of_clusters, pokemon):
    x = df.iloc[:, [6, 7, 10]].values
    names = df.iloc[:, 1].values
    kmeans5 = KMeans(n_clusters=int(no_of_clusters))
    y_kmeans5 = kmeans5.fit_predict(x)
    # a = kmeans5.cluster_centers_
    index = np.nonzero(names == pokemon)
    cluster_nu = y_kmeans5[index]
    itemindex = np.where(y_kmeans5 == cluster_nu)
    a = [item for item in itemindex]
    nearest = random.sample(list(a[0]), 5)
    # print(nearest)
    pokemon_names = []
    for i in nearest:
        pokemon_names.append(names[i])

    return json.dumps(pokemon_names)

@app.callback(Output('pokemonCheck', component_property='options'),
    [Input('intermediate-value', 'children')])

def pokemonCheckList(jsonified_pokemon):
    dff = pd.read_json(jsonified_pokemon)
    intermediate_pokemon = dff.values.tolist()
    pokemon_names = []
    for i in range(len(intermediate_pokemon)):
        pokemon_names.append(intermediate_pokemon[i][0])
    print(pokemon_names)
    #print(type(pokemon_names[0]))
    return [{'label' : i, 'value' : i} for i in pokemon_names]


@app.callback(
    Output(component_id='output-graph1', component_property='children'),
    [Input(component_id='option_dropdown', component_property='value'),
     Input(component_id='pokemonCheck', component_property='value'),
     Input(component_id='dropdown2', component_property='value')]
)

def update_graph(option, pokemon_names, pokemon):
    #Get Pokemon Names and their values corresponding to options (ex . Attack, Defense, Speed, Catch_Rate)
    print('Hit it')


    print(pokemon_names)
    option_value = []
    '''
    with open('names.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            pokemon_names = row
    '''
    #Get the values for each pokemon according to selected option
    filtered_df = df[["Name","Attack", "Defense", "Speed", "Catch_Rate"]]
    #print(pokemon_names)

    for name in pokemon_names:
        option_df = df[(df.Name == name)]
        option_value.append(int(option_df.iloc[0][option]))

    #print(option_value)


    return dcc.Graph(
        id='similarPokemonGraph',
        figure={
            'data': [
                {'x': pokemon_names, 'y': option_value,
                 'type': 'bar',
                 'marker': {
                     'color': '#0277bd'
                 }
                 }
            ],
            'layout': {
                'title': 'Similar Pokemons',
                'hovermode': 'closest',
                'paper_bgcolor': '#e1f5fe',
                'plot_bgcolor': '#e1f5fe',
                'height': 500,

            },

        }
    )

@app.callback(
    Output(component_id='radar-graph', component_property='figure'),
    [Input(component_id='pokemonCheck', component_property='value')]
)

def updateRadarGraph(names):
    categories = ['Attack', 'Defense', 'Sp_Atk',
                  'Sp_Def', 'Speed']

    fig = go.Figure()
    '''
    with open('names.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            names = row
    '''
    num = len(names)

    for i in range(num):
        option_df = df[(df.Name == names[i])]
        option_value = []
        for j in range(5):
            option_value.append(int(option_df.iloc[0][categories[j]]))

        fig.add_trace(go.Scatterpolar(
            r = option_value,
            theta= categories,
            fill='toself',
            name= names[i]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 200]
            )),
        showlegend=True,
        paper_bgcolor = '#ffffff',
        plot_bgcolor='#ffffff'

    )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
