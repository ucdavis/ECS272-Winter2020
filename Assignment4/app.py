import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE 

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go

import pickle

def dummy_cluster_norm(data, numCluster):
    
    data_num = data.select_dtypes(['number'])

    # instantiate kmeans object and perform clustering
    kmeans = KMeans(n_clusters = numCluster)
    kmeans.fit(data_num)
    
    # dimensionality reduction via PCA -> 50
    reduce_dim_data_df = pd.DataFrame(PCA(n_components=50).fit_transform(data_num))

    # dimensionality reduction via TSNE -> 3
    tsne_3d_df = pd.DataFrame(TSNE(n_components=3).fit_transform(reduce_dim_data_df))
    
    # append data with column of cluster labels and 3d coordinates
    # coordinates are normalized to fall in the range [0,1]
    data['clusterNo'] = kmeans.labels_.astype(str)
    data['xcoord'] = tsne_3d_df[0].apply(lambda x : x / tsne_3d_df[0].max())
    data['ycoord'] = tsne_3d_df[1].apply(lambda x : x / tsne_3d_df[1].max())
    data['zcoord'] = tsne_3d_df[2].apply(lambda x : x / tsne_3d_df[2].max())
    
    CURRENT_CLUSTER_NO = numCluster

    return data

CURRENT_CLUSTER_NO = 3

try:

    # load dataFrame of preprocessed data
    with open("__temp", 'rb') as f:
        df = pickle.load(f)

except:

    # load responses as a DataFrame from raw CSV
    with open("responses.csv") as f:
        df = pd.read_csv(f)
    
    # fill in missing values with the average of each column and
    # perform initial clustering
    df.fillna(df.mean(), inplace=True)
    df = dummy_cluster_norm(df, 3)
    
    # save preprocessed data
    with open("__temp", "wb") as f:
        pickle.dump(df, f)

# load a dict to translate short column headers to full survey questions    
with open("columns.csv") as f:
    x = pd.read_csv(f)
    headerDict = pd.Series(x.original.values, index=x.short).to_dict()

# create dict of categories for survey questions
question_categories = {
    "Music" : list(df.columns[0:19]),
    "Movies" : list(df.columns[19:31]),
    "Hobbies" : list(df.columns[31:63]),
    "Phobias" : list(df.columns[63:73]),
    "Health" : list(df.columns[73:76]),
    "Personality" : list(df.columns[76:133]),
    "Spending" : list(df.columns[133:140]),
    "Demographics" : list(df.columns[140:150])
}


default_colors = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#d62728',  # brick red
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
    '#2ca02c',  # cooked asparagus green
]

def render_visualization():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([

        html.Div([
            html.Div([

                dcc.Checklist(
                    id = 'question-dropdown',
                    options=[
                        {'label' : 'Music', 'value' : 'Music'},
                        {'label' : 'Movies', 'value' : 'Movies'},
                        {'label' : 'Hobbies', 'value' : 'Hobbies'},
                        {'label' : 'Phobias', 'value' : 'Phobias'},
                        {'label' : 'Health', 'value' : 'Health'},
                        {'label' : 'Personality', 'value' : 'Personality'},
                        {'label' : 'Spending', 'value' : 'Spending'},
                        {'label' : 'Demographics', 'value' : 'Demographics'}],
                    value=['Music','Movies'],
                    className='six columns',
                    style={'width': '45%'}
                ),

                dcc.RadioItems(
                    id = 'cluster-dropdown',
                    options=[
                        {'label' : '2 Clusters', 'value' : 2},
                        {'label' : '3 Clusters', 'value' : 3},
                        {'label' : '4 Clusters', 'value' : 4},
                        {'label' : '5 Clusters', 'value' : 5},
                        {'label' : '6 Clusters', 'value' : 6},
                        {'label' : '7 Clusters', 'value' : 7}],
                    value=3,
                    className='six columns',
                    style={'width': '45%'}
                )
            ], className="three columns", style={'backgroundColor' : 'rgb(220,220,220)', 'width' : '25%'}),
            
            html.Div([
                html.Div(html.H1("Young People Survey")),
            
                html.Div(html.H4("Subtitle")),
            ],className="three columns", style={'width' : '60%'})
        ],className="row"),

        html.Div([
            html.Div(
                    dcc.Graph(
                            id='3d-plot',
                            style={'height' : '900px'}
                        ),
                    className='six columns',
                    style={'width': '48%', 'height': '1000px'}
                ),
            html.Div(
                    dcc.Graph(
                        id='corr-heatmap',
                        style={'height' : '900px'}
                    ),
                    className='six columns',
                    style={'width': '48%', 'height' : '1000px'}),
        ], className="row", style={}),
        
        html.Div(dcc.Graph(id='violins',style={'width':'100%'}),
                style={'maxWidth' : '100%', 'overflowX' : 'scroll'},
                className='row')

    ])

    # updates the 3d scatterplot of survey response clusters
    @app.callback(
        Output('3d-plot', 'figure'),
        [Input('cluster-dropdown', 'value')]
    )
    def update_figure(clusterNo):

        global df
        global CURRENT_CLUSTER_NO

        if clusterNo != CURRENT_CLUSTER_NO:
            df = dummy_cluster_norm(df, clusterNo)

        fig = go.Figure()

        for x in range(clusterNo):
            fig.add_trace(go.Scatter3d(x=df[df.clusterNo == str(x)]['xcoord'].tolist(),
                                        y=df[df.clusterNo == str(x)]['ycoord'].tolist(),
                                        z=df[df.clusterNo == str(x)]['zcoord'].tolist(),
                                        mode='markers',
                                        marker={'color' : default_colors[x]},
                                        name="Cluster {}".format(x)
                                    )
            )

        fig.update_layout(showlegend=True, legend={'x' : 0.8, 'y' : 0.9, 'bordercolor': "Black", 'borderwidth': 1})

        return  fig#px.scatter_3d(df, x='xcoord', y='ycoord', z='zcoord', color='clusterNo')


    # updates the heatmap of correlation coefficients
    @app.callback(
        Output('corr-heatmap', 'figure'),
        [Input('question-dropdown', 'value'),
        Input('3d-plot', 'clickData')]
    )
    def update_heatmap(category_choices, click_data):
        if click_data:
            chosen_cluster = str(click_data["points"][0]['curveNumber'])
        else:
            chosen_cluster = "0"
        
        df_selected = df[df['clusterNo'] == chosen_cluster]

        chosen_columns = []
        for choice in category_choices:
            chosen_columns = chosen_columns + question_categories[choice]

        df_selected = df_selected[chosen_columns]
        
        matrix = df_selected.corr().values.tolist()
        mask = np.tri(len(df_selected.columns), k=0)
        matrix = np.ma.array(matrix, mask=mask)

        fig = go.Figure(data=go.Heatmap(z=[np.flip(x) for x in matrix.filled(np.nan)],
                                        x=[x for x in np.flip(df_selected.columns)[:-1]],
                                        y=[x for x in df_selected.columns[:-1]],
                                        colorscale='gray_r',
                                        hoverongaps=False
                                        )
                        )

        fig.update_layout(title={'text' : "Correlation Coefficients in Cluster {}".format(chosen_cluster),
                                    'x' : 0.34,
                                    'xanchor' : 'left',
                                    'y' : 0.85,
                                    'yanchor' : 'middle'
                                },
                            titlefont={'size' : 30},
                            xaxis={'showgrid' : False},
                            yaxis={'showgrid' : False},
                            plot_bgcolor='rgb(255,255,255)'
                        )
        
        return fig


    # updates the violin plot of survey responses
    @app.callback(
        Output('violins', 'figure'),
        [Input('question-dropdown', 'value'),
        Input('cluster-dropdown', 'value')]
    )
    def update_violins(category_choices, number_of_clusters):

        chosen_columns = []
        for choice in category_choices:
            chosen_columns = chosen_columns + question_categories[choice]

        fig = go.Figure()

        # for column in chosen_columns:
        #     for clusterNo in range(number_of_clusters):
        #         fig.add_trace(go.Violin(y=df[column][df['clusterNo'] == str(clusterNo)],
        #                                 x=headerDict[column],
        #                                 legendgroup="Cluster {}".format(clusterNo),
        #                                 #box_visible=True,
        #                                 meanline_visible=True,
        #                                 line_color=default_colors[clusterNo],
        #                                 opacity=0.4)
        #                     )
        for clusterNo in range(number_of_clusters):
            fig.add_trace(go.Violin(y=df[chosen_columns][df['clusterNo'] == str(clusterNo)],
                                    x=chosen_columns,
                                    legendgroup="Cluster {}".format(clusterNo),
                                    box_visible=True,
                                    meanline_visible=True,
                                    line_color=default_colors[clusterNo],
                                    opacity=0.4)
                        )

        #fig.update_traces(side='positive', points=False, width = 1.5)
        fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False, width=len(chosen_columns) * 100, autosize=False)

        return fig

    app.run_server(debug=True)

if __name__ == "__main__":
    render_visualization()