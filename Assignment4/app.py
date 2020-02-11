import plotly.express as px
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import time
df = pd.read_csv("./pokemon_alopez247.csv")
types = sorted(list(set(df['Type_1'])))
current_type = None
prev_clicked_basic_type = None
prev_clicked_advanced_type = None
prev_clicked_cluster_type = None
import simplejson as json
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='ECS 272 Assignment 4'),

    html.Div(children='''
        Choose the k value for k-means clustering.
    '''),

    dcc.Dropdown(
        id = 'kmeans_dropdown',
        options = [
            {'label': '2', 'value': 2},
            {'label': '3', 'value': 3},
            {'label': '4', 'value': 4},
            {'label': '5', 'value': 5},
        ],
        value = 2
    ),

    dcc.Graph(
        id='basic_graph',
        # clickData=None
    ),

    dcc.Graph(
        id='adv_graph'
    ),

    dcc.Graph(
        id='clustering_graph'
    ),
    html.Div(id='intermediate-value', style={'display': 'none'})
])
@app.callback(
    Output('intermediate-value', 'children'), 
    [Input('basic_graph', 'clickData')])
def updateSelection(clickData):
    print("intermediate")
    global prev_clicked_basic_type
    current_clickData = None
    if(clickData):
        clicked_type = clickData['points'][0]['label']
        if prev_clicked_basic_type != clicked_type:
            prev_clicked_basic_type = clicked_type
            current_clickData = clickData
            print("assign")
        else:
            prev_clicked_basic_type = None
            print("clear")
    inter_data = '{"selectedData": "None"}'
    inter_obj = json.loads(inter_data)
    inter_obj['selectedData'] = json.dumps(current_clickData)
    res = json.dumps(inter_obj)
    # print(inter_obj)
    return res
    
        
    
@app.callback(
    Output('basic_graph', 'figure'),
    [Input('intermediate-value', 'children')])
def update_basic_figure(selectedData):
    print("a")
    local_colors = ['blue']*len(types)
    selectedData = json.loads(selectedData)
    clickpoint = selectedData['selectedData']
    # print(clickpoint)
    if clickpoint != 'null':
        clickpoint = json.loads(clickpoint)
        # print(clickpoint)
        clicked_type = clickpoint['points'][0]['label']
        local_colors[types.index(clicked_type)] = 'green'

    counts = [len(df[df.Type_1 == type]) for type in types]
    fig = go.Figure(data=[go.Bar(
        x = types,
        y = counts,
        marker_color=local_colors # marker color can be a single color value or an iterable
    )])
    fig.update_layout(title_text='Overview')
    return fig

@app.callback(
    Output('adv_graph', 'figure'),
    [Input('basic_graph', 'clickData')])
def update_advanced_figure(clickData):
    print("b")
    global prev_clicked_advanced_type
    if clickData:
        #select type logic implementation
        clicked_type = clickData['points'][0]['label']


        if prev_clicked_advanced_type != clicked_type:
            prev_clicked_advanced_type = clicked_type
            fig = px.treemap(df[df.Type_1 == clicked_type], 
                            path=['Type_1', 'Name'], values='Total',
                              hover_data=['Name'],
                              color_continuous_scale='RdBu')
        else:
            fig = px.treemap(df, path=['Type_1', 'Name'], values='Total',
                              hover_data=['Name'],
                              color_continuous_scale='RdBu')
            prev_clicked_advanced_type = None
    else:
        fig = px.treemap(df, path=['Type_1', 'Name'], values='Total',
                          hover_data=['Name'],
                          color_continuous_scale='RdBu')
    return fig

def cluster(n_clusters, x):
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(x)
    Z = kmeans.predict(x)
    return kmeans, Z

@app.callback(
    Output('clustering_graph', 'figure'),
    [Input('intermediate-value', 'children'), Input('kmeans_dropdown', 'value')])
def update_clustering_figure(selectedData, value):
    print("c")
    selectedData = json.loads(selectedData)
    kmeans_val = value
    clickpoint = selectedData['selectedData']
    print(clickpoint)
    if clickpoint != 'null':
        clickpoint = json.loads(clickpoint)
        print("in here")
        clicked_type = clickpoint['points'][0]['label']
        # if prev_clicked_cluster_type != clicked_type:
        #     prev_clicked_cluster_type = clicked_type
        local_df = df[df.Type_1 == clicked_type]
        stats = local_df.iloc[:, 5:11]
        normalized_stats = stats
        for i in stats.columns:
            mini, maxi = stats[i].min(), stats[i].max()
            normalized_stats[i] = (stats[i] - mini) / (maxi - mini)
        pca = PCA(n_components=2).fit(normalized_stats)
        stats2d = pca.transform(normalized_stats)
        df_stats2d = pd.DataFrame(stats2d, index=local_df.index)

        model, z = cluster(kmeans_val, normalized_stats.iloc[:,0:5])
        trace = go.Scatter(x=df_stats2d.iloc[:, 0],
                            y=df_stats2d.iloc[:, 1],
                            text=local_df['Name'],
                            name='',
                            mode='markers',
                            marker=go.Marker(opacity=0.5,
                                            color=z),
                            showlegend=False
        )
    #     else:
    #         prev_clicked_cluster_type = clicked_type
    #         stats = df.iloc[:, 5:11]
    #         normalized_stats = stats
    #         for i in stats.columns:
    #             mini, maxi = stats[i].min(), stats[i].max()
    #             normalized_stats[i] = (stats[i] - mini) / (maxi - mini)
    #         pca = PCA(n_components=2).fit(normalized_stats)
    #         stats2d = pca.transform(normalized_stats)
    #         model, z = cluster(kmeans_val, normalized_stats.iloc[:,0:5])
    #         prev_clicked_cluster_type = None
    #         trace = go.Scatter(x=stats2d[:, 0],
    #                          y=stats2d[:, 1],
    #                          text=df['Name'],
    #                          name='',
    #                          mode='markers',
    #                          marker=go.Marker(opacity=0.5,
    #                                            color=z),
    #                          showlegend=False
    # )
    else:
        print("error")
        stats = df.iloc[:, 5:11]
        normalized_stats = stats
        for i in stats.columns:
            mini, maxi = stats[i].min(), stats[i].max()
            normalized_stats[i] = (stats[i] - mini) / (maxi - mini)
        pca = PCA(n_components=2).fit(normalized_stats)
        stats2d = pca.transform(normalized_stats)
        model, z = cluster(kmeans_val, normalized_stats.iloc[:,0:5])
        trace = go.Scatter(x=stats2d[:, 0],
                         y=stats2d[:, 1],
                         text=df['Name'],
                         name='',
                         mode='markers',
                         marker=go.Marker(opacity=0.5,
                                           color=z),
                         showlegend=False
         )
    layout = go.Layout(title='k-means clustering of catch_rate and total stats',
                     xaxis=go.XAxis(showgrid=False,
                                     zeroline=False,
                                     showticklabels=False),
                     yaxis=go.YAxis(showgrid=False,
                                     zeroline=False,
                                     showticklabels=False),
                     hovermode='closest'
    )
    data = go.Data([trace])
    fig = go.Figure(data=data, layout=layout)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)