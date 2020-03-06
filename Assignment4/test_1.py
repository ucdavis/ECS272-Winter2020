import dash
import random
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import cluster
import json
df = pd.read_csv('pokemon_alopez247.csv')
filtered_df = cluster.Cluster('pokemon_alopez247.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3("K-mean Clustering Overview")],
            style={'text-align': 'center', 'color': 'blue'}
        ),
        html.Div([
            dcc.Dropdown(
                id='k-mean-value',
                options=[
                    {'label': 'Two-mean-value', 'value': 2},
                    {'label': 'Three-mean-value', 'value': 3},
                    {'label': 'Four-mean-value', 'value': 4},
                    {'label': 'Five-mean-value', 'value': 5},
                ],
                value=2,
                placeholder="Two-mean-value selected as default",
            )
        ],
        style={'width': '31%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='attritube_1',
                options=[
                    {'label': 'Total', 'value': 'Total'},
                    {'label': 'HP', 'value': 'HP'},
                    {'label': 'Attack', 'value': 'Attack'},
                    {'label': 'Defense', 'value': 'Defense'},
                    {'label': 'Special Attack', 'value': 'Sp_Atk'},
                    {'label': 'Special Defense', 'value': 'Sp_Def'},
                    {'label': 'Speed', 'value': 'Speed'},
                    {'label': 'Height_m', 'value': 'Height_m'},
                    {'label': 'Weight_kg', 'value': 'Weight_kg'},
                    {'label': 'Catch_Rate', 'value': 'Catch_Rate'}
                ],
                value='Attack',
                placeholder="Type_1 selected as default",
            )
        ],
        style={'width': '31%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='attritube_2',
                options=[
                    {'label': 'HP', 'value': 'HP'},
                    {'label': 'Attack', 'value': 'Attack'},
                    {'label': 'Defense', 'value': 'Defense'},
                    {'label': 'Special Attack', 'value': 'Sp_Atk'},
                    {'label': 'Special Defense', 'value': 'Sp_Def'},
                    {'label': 'Speed', 'value': 'Speed'},
                    {'label': 'Height_m', 'value': 'Height_m'},
                    {'label': 'Weight_kg', 'value': 'Weight_kg'}
                ],
                value='Speed',
                placeholder="Catch_Rate selected as default",
            )
        ],
        style={'width': '31%', 'display': 'inline-block'}), 
    ]),
    html.Div([dcc.Graph(id='scatter-plot')]),
    html.Div([
        html.Div([
            html.H3("Sankey Diagram:Pokemon's Attribute by isLegendary and Color")],
            style={'text-align': 'center',
                   'color': 'blue', 'margin-top': '75px'}),
        html.Div(dcc.Dropdown(
            id='poke-attr',
            options=[
                {'label': 'Body_Style', 'value': 'Body_Style'},
                {'label': 'Egg_Group_1', 'value': 'Egg_Group_1'},
                {'label': 'Egg_Group_2', 'value': 'Egg_Group_2'},
                {'label': 'Type_1', 'value': 'Type_1'},
                {'label': 'Type_2', 'value': 'Type_2'}
            ],
            value='Body_Style',
            placeholder="Body_Style",
        )),
        html.Div(html.Div(dcc.Graph(id='Sankey-with-dropdown')))
    ]),
    html.Div([
        html.Div([
            html.H3("Type/Color/Body style parallel relationships")],
            style={'text-align': 'center',
                   'color': 'blue', 'margin-top': '20px'}),
        html.Div(html.Div(dcc.Graph(id='parallel'))),

    html.Div([
        html.Div([
            html.H3("Pokemon 's Histogram by Attritube")],
            style={'text-align': 'center',
                   'color': 'blue', 'margin-top': '75px'}),
        html.Div(dcc.Dropdown(
            id='poke-attr1',
            options=[
                {'label': 'Body_Style', 'value': 'Body_Style'},
                {'label': 'Egg_Group_1', 'value': 'Egg_Group_1'},
                {'label': 'Egg_Group_2', 'value': 'Egg_Group_2'},
                {'label': 'Type_1', 'value': 'Type_1'},
                {'label': 'Type_2', 'value': 'Type_2'},
                {'label': 'isLegendary', 'value': 'isLegendary'},
                {'label': 'Color', 'value': 'Color'},
                {'label': 'hasGender', 'value': 'hasGender'},
                {'label': 'hasMegaEvolution', 'value': 'hasMegaEvolution'}
            ],
            value='Type_1',
            placeholder="Type_1",
        )),
        html.Div(html.Div(dcc.Graph(id='histogram-with-dropdown')))
    ])

    ])
])

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('k-mean-value', 'value'),
    Input('attritube_1', 'value'),
    Input('attritube_2','value')]
)
def update_figure(selected_k_mean_value,selected_attr1,selected_attr2):
    if selected_attr1 == selected_attr2:
        raise PreventUpdate
    index1 = filtered_df.df.columns.get_loc(selected_attr1)
    index2 = filtered_df.df.columns.get_loc(selected_attr2)
    if index1 > index2:
        selected_attr1, selected_attr2 = selected_attr2, selected_attr1
        index1, index2 = index2, index1
    dff = filtered_df.getCluster(selected_k_mean_value, index1, index2)
    fig = px.scatter(dff, x=dff[selected_attr1], y=dff[selected_attr2],
                     color='K-Means', marginal_y="rug", marginal_x="histogram")
    fig.update_layout(
        title={
            'y': 0.99,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        margin={
            'b': 50, 'r': 20, 'l': 30, 't': 20
            },
        xaxis={
            'title': selected_attr1
        },
        yaxis_title_text=selected_attr2, 
        bargap=0.2,  
        bargroupgap=0.1  
    )
    return fig


@app.callback(
    Output('Sankey-with-dropdown', 'figure'),
    [Input('poke-attr', 'value'),
    Input('scatter-plot', 'selectedData')])
def update_Sankey(selected_poke_attr,selectedData):
    if selectedData:
        indices = [point['pointIndex'] for point in selectedData['points']]
        dff = df.iloc[indices, :]
    else:
        dff = df

    is_legendary = [i for i in dff.isLegendary.unique()]
    color = [i for i in dff.Color.unique()]
    selected_attr = [i for i in dff[selected_poke_attr].unique()]
    size = is_legendary+color+selected_attr
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=15,
            line=dict(color='blue', width=0.8),
            label=size,
            color=['rgb(50, 168, 160)', 'yellow', 'green',
                'purple', 'white', 'orange', 'rgb(131, 207, 56)', 'rgb(43, 196, 156)', 'rgb(28, 92, 156)', 'rgb(11, 120, 230)', 'rgb(232, 39, 120)', 'rgb(186, 103, 48)', 'rgb(23, 156, 76)', 'rgb(55, 21, 176)', 'rgb(100, 156, 123)', 'rgb(31, 66, 110)', 'rgb(186, 150, 48)', 'rgb(131, 207, 56)', 'rgb(232, 39, 120)']
        ),
        link=getData(size, color, dff, is_legendary,selected_poke_attr)

    )])
    return fig

def getData(size, color, dff, is_legendary, selected_poke_attr):

    result = {"source": [], "target": [], "value": [], "color": []}
    isLegLast = len(is_legendary)
    ColorLast = len(is_legendary) + len(color)
    AttrLast = len(size)
    for i in range(isLegLast):
        for j in range(isLegLast, ColorLast):
            isLegfilter = dff[dff.isLegendary == is_legendary[i]]
            colorfilter = isLegfilter[isLegfilter.Color == size[j]]
            if len(colorfilter) != 0:
                result["source"].append(i)
                result["target"].append(j)
                result["value"].append(len(colorfilter))
                result["color"].append(
                    'rgba'+str((0, random.randint(200, 255), random.randint(100, 255), 0.5)))
    for k in range(isLegLast, ColorLast):
        for l in range(ColorLast, AttrLast):
            #colorfilter = isLegfilter[isLegfilter.Color == size[k]]
            colorfilter = dff[dff.Color == size[k]]
            Attrfilter = colorfilter[colorfilter[selected_poke_attr] == size[l]]
            if len(Attrfilter) != 0:
                result["source"].append(k)
                result["target"].append(l)
                result["value"].append(len(Attrfilter))
                result["color"].append(
                    'rgba'+str((50, random.randint(200, 255), random.randint(100, 255), 0.5)))
    return result

@app.callback(
    Output('histogram-with-dropdown', 'figure'),
    [Input('poke-attr1', 'value'),
     Input('scatter-plot', 'selectedData')
     ])

def update_figure(selected_poke_attr1, selectedData):
    if selectedData:
        indices = [point['pointIndex'] for point in selectedData['points']]
        dff = df.iloc[indices, :]
    else:
        dff = df

    fig = px.histogram(
        dff, x=dff[selected_poke_attr1])
    fig.update_layout(
        title={
            'y': 1,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        margin={
            'b': 200, 'r': 20, 'l': 30, 't': 20
        },
        xaxis={
            'title': 'Pokemon\'s Detail View on ' + selected_poke_attr1
        },
        yaxis_title_text='Count',
        bargap=0.2,
        bargroupgap=0.1
    )
    return fig


@app.callback(
    Output(component_id='parallel', component_property='figure'),
    [
        Input(component_id='scatter-plot', component_property='selectedData')
    ]
)
def update_graph(selectedData):
    if selectedData:
        indices = [point['pointIndex'] for point in selectedData['points']]
        dff = df.iloc[indices, :]
    else:
        dff = df
    fig = px.parallel_categories(dff, dimensions=['Type_1', 'Color', 'Body_Style'],
                                 labels={'Type': 'Type_1', 'Color': 'Color',
                                         'Body Style': 'Body_Style'}
                                 )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
