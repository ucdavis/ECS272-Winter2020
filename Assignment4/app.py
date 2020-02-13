import pandas as pd

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
    
    global CURRENT_CLUSTER_NO
    CURRENT_CLUSTER_NO = numCluster

    return data

CURRENT_CLUSTER_NO = 3

try:
    with open("__temp", 'rb') as f:
        df = pickle.load(f)
except:
    # load responses as a DataFrame
    with open("responses.csv") as f:
        df = pd.read_csv(f)
    df.fillna(df.mean(), inplace=True)
    df = dummy_cluster_norm(df, 3)
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

def render_visualization():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        html.Div(html.H1("Title")),
    
        html.Div(html.H4("Subtitle")),

        html.Div([
                
            dcc.Graph(id='3d-plot', style={'width': '50%'}),

            dcc.Dropdown(
                id = 'cluster-dropdown',
                options=[
                    {'label' : '2 Clusters', 'value' : 2},
                    {'label' : '3 Clusters', 'value' : 3},
                    {'label' : '4 Clusters', 'value' : 4},
                    {'label' : '5 Clusters', 'value' : 5},
                    {'label' : '6 Clusters', 'value' : 6},
                    {'label' : '7 Clusters', 'value' : 7}],
                value=3,
                style={'width': '53%'}
            )
        ]),

        html.Div([
                
            dcc.Graph(id='corr-heatmap', style={'width': '100%'}),

            dcc.Dropdown(
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
                multi=True,
                style={'width': '53%'}
            )
        ]),

        html.Div(dcc.Graph(id='violins',style={'width':'100%'}),style={'maxWidth' : '1000px', 'overflowX' : 'scroll'})

    ])

    @app.callback(
        Output('3d-plot', 'figure'),
        [Input('cluster-dropdown', 'value')]
    )
    def update_figure(clusterNo):
        global df

        if clusterNo != CURRENT_CLUSTER_NO:
            df = dummy_cluster_norm(df, clusterNo)

        return px.scatter_3d(df, x='xcoord', y='ycoord', z='zcoord', color='clusterNo')

    @app.callback(
        Output('corr-heatmap', 'figure'),
        [Input('question-dropdown', 'value'),
        Input('3d-plot', 'clickData')]
    )
    def update_heatmap(category_choices, click_data):
        if click_data:
            chosen_cluster = str(click_data["points"][0]['marker.color'])
        else:
            chosen_cluster = "0"
        
        df_selected = df[df['clusterNo'] == chosen_cluster]

        chosen_columns = []
        for choice in category_choices:
            chosen_columns = chosen_columns + question_categories[choice]

        df_selected = df_selected[chosen_columns]
        
        return go.Figure(data=go.Heatmap(z=df_selected.corr().values.tolist(), x=df_selected.columns, y=df_selected.columns, colorscale='gray'))

    @app.callback(
        Output('violins', 'figure'),
        [Input('question-dropdown', 'value')]
    )
    def update_violins(category_choices):

        chosen_columns = []
        for choice in category_choices:
            chosen_columns = chosen_columns + question_categories[choice]

        fig = go.Figure()

        for column in chosen_columns:
            for clusterNo in range(3):
                fig.add_trace(go.Violin(y=df[column][df['clusterNo'] == str(clusterNo)],
                                        name=headerDict[column],
                                        scalegroup=headerDict[column],
                                        legendgroup=clusterNo,
                                        #box_visible=True,
                                        meanline_visible=True,
                                        line_color='rgb({},0,0)'.format(255/(clusterNo+1)),
                                        opacity=0.3)
                            )

        fig.update_traces(side='positive', points=False, width = 1.5)
        fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False, width=len(chosen_columns) * 100, autosize=False)

        return fig

    app.run_server(debug=True)

if __name__ == "__main__":
    render_visualization()
