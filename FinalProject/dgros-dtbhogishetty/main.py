from typing import List
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
from pandas import DataFrame
from data_constants import feats_all, feats_numeric, feats_ordinal, feat_colors, feats_bool, bool_colors
from dataproc import load_data, vectorize_examples, run_tsne
from plottool import make_sankey
from util import setup_cache

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = load_data()

cache = setup_cache(app)

# IDs
id_dimreduct_feats = "dimreduct-feats"
###

sankey_feats = ['Body_Style', 'Type_1', 'Egg_Group_1']


def build_highlight_stat_dropdown():
    return dcc.Dropdown(
        id='highlight-stat-dropdown',
        options=[
            {"label": feat, "value": feat}
            for feat in feats_all
        ],
        value="Type_1"
    )


def build_dim_reduction_feats_selector():
    return dcc.Dropdown(
        id=id_dimreduct_feats,
        options=[
            {"label": feat, "value": feat}
            for feat in feats_all
        ],
        value=[feat for feat in feats_all],
        multi=True,
        clearable=False
    )


def build_layout():
    return html.Div([
        html.Div([
            html.H1("Exploring Pokémon Data")
        ], style={'text-align': 'center'}),
        html.Div([
            html.Div([
                html.H4("T-SNE Dimensionality Reduction"),
                html.Div([
                    html.Label("Dimensionality Reduction Features (what features we consider):"),
                    build_dim_reduction_feats_selector(),
                    html.Plaintext(
                        'Note, that updates to these inputs reruns the dimensionality'
                        'reduction and can take significant time.'
                    ),
                    html.Label("Marker Color Feature:"),
                    build_highlight_stat_dropdown(),
                ]),
                dcc.Loading(dcc.Graph(
                    id='pokemon-scatter', style={"height": "70vh"}
                )),
                html.Plaintext(
                    "Click on a Pokémon to view stats."
                ),
            ], style={'flex': '0 0 60%', 'height': '100%'}),
            html.Div([
                html.Div(
                    [
                        html.Div(dcc.Graph(
                            figure=px.bar()
                        ))
                    ],
                    id='pokemon-stats',
                    style={"display": 'inline-block', "width": "35vw"}
                ),
                html.Div([
                    dcc.Graph(
                        id='pokemon-sankey',
                        style={"width": "35vw", "height": "50%"}
                    ),
                    html.Plaintext(
                        f"Parallel Coordinates Sankey showing {', '.join(sankey_feats)}",
                        style={"margin": "auto", "width": "100%", "text-align": "center"}
                    )
                ], style={"display": 'inline-block'}),
            ], style={'flex': '0 0 40%', "margin": "auto"}),
        ], style={'display': "flex", "height": "90vh", "margin": "aut"})
    ])

app.layout = build_layout()

@cache.memoize()
def get_tsne_cached(dimreduct_feats: List[str]):
    print("Running tsne")
    vecs = vectorize_examples(df, dimreduct_feats)
    return run_tsne(vecs)


# Run the get_tsne on init so that it will show loading screen until this is ready
get_tsne_cached(feats_all)


@app.callback(
    Output('pokemon-scatter', 'figure'),
    [
        Input('highlight-stat-dropdown', 'value'),
        Input(id_dimreduct_feats, 'value')
    ])
def build_scatter(highlight_stat: str, dimreduct_feats: List[str]):
    tsne = get_tsne_cached(dimreduct_feats)

    def build_color(vals):
        if highlight_stat in feats_numeric + feats_ordinal:
            return vals
        elif highlight_stat in feats_bool:
            return [bool_colors[v] for v in vals]
        else:
            relevant_colors = feat_colors[highlight_stat]
            return [relevant_colors[str(v)] for v in vals]

    text = [
        f"{name} --- {highlight_val}"
        for name, highlight_val in zip(df['Name'], df[highlight_stat])
    ]

    fig = go.Figure(
        data=go.Scatter(
            x=tsne[:, 0],
            y=tsne[:, 1],
            mode='markers',
            text=text,
            hoverinfo='text',
            marker={
                "color": build_color(df[highlight_stat]),
                "colorscale": "PuBu"
            },
            customdata=df['Name']
        ),
        layout=go.Layout(
            autosize=True,
            margin=dict(l=0, r=0, t=10, b=0)
        )
    )
    return fig


@app.callback(
    Output('pokemon-sankey', 'figure'),
    [Input('pokemon-scatter', 'clickData')])
def build_sankey(clickData):
    #categorical_dimensions = ['Type_1', 'Body_Style']
    #dimensions = [dict(values=df[label], label=label) for label in categorical_dimensions]
    #return go.Parcats(
    #    dimensions=dimensions,
    #)
    if clickData:
        name = clickData['points'][0]['customdata']
        selected_row = df.loc[df['Name'] == name].to_dict()

        def highlight_node(field, value):
            return list(selected_row[field].values())[0] == value
    else:
        highlight_node = None

    return {"data": [make_sankey(df, sankey_feats, highlight_node)]}


@app.callback(
Output('pokemon-stats', 'children'),
[Input('pokemon-scatter', 'clickData')])
def display_click_data(clickData):
    #using this to get index of the point
    if clickData is None:
        raise PreventUpdate
    name = clickData['points'][0]['customdata']
    ddf = df[df['Name'] == name]
    bar_x = ['HP','Normal Attack','Normal Defense','Special Attack','Special Defence','Speed']
    bar_y = ddf['HP'].append(ddf['Attack']).append(ddf['Defense']).append(ddf['Sp_Atk']).append(ddf['Sp_Def']).append(ddf['Speed'])
    fig = px.bar(x=bar_x, y=bar_y,labels={'x': name + ' Stats' ,'y': 'Value'})
    fig.update_yaxes(range=[0,255])
    return dcc.Graph(figure=fig)


if __name__ == '__main__':
    app.run_server(debug=True)
