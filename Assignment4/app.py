import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.manifold import TSNE 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# load responses as a DataFrame
with open("responses.csv") as f:
    df = pd.read_csv(f)

# load a dict to translate short column headers to full survey questions    
with open("columns.csv") as f:
    x = pd.read_csv(f)
    headerDict = pd.Series(x.original.values, index=x.short).to_dict()

# create a dataFrame of the numerical columns from the data; drop all the NaN values for now
df_num = df.select_dtypes(['number']).dropna().reset_index(drop=True)

# QUESTION: since we have a high-dimensionality data set, should we normalize the data set? 
def dummy_cluster_norm(data, numCluster):
    
    # instantiate kmeans object and perform clustering
    kmeans = KMeans(n_clusters = numCluster)
    kmeans.fit(preprocessing.normalize(data))
    
    # dimensionality reduction via PCA
    reduce_dim_data_df = pd.DataFrame(PCA(n_components=50).fit_transform(data))

    # dimensionality reduction via TSNE
    tsne_3d_df = pd.DataFrame(TSNE(n_components=3).fit_transform(reduce_dim_data_df))
    
    # append data with column of cluster labels and 3d coordinates
    data['clusterNo'] = kmeans.labels_
    data['xcoord'] = tsne_3d_df[0]
    data['ycoord'] = tsne_3d_df[1]
    data['zcoord'] = tsne_3d_df[2]
    
    return data


def render_visualization():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        html.Div(html.H1("Title")),
    
        html.Div(html.H4("Subtitle")),

        dcc.Graph(id='3d-plot'),

        dcc.Slider(
            id = 'cluster-slider',
            min = 2,
            max = 7,
            value = 3,
            marks={str(x): str(x) for x in range(2,8)},
            step = None
        )
    ])

    @app.callback(
        Output('3d-plot', 'figure'),
        [Input('cluster-slider', 'value')]
    )
    def update_figure(clusterNo):
        return px.scatter_3d(dummy_cluster_norm(df_num, clusterNo), x='xcoord', y='ycoord', z='zcoord', color='clusterNo')

    app.run_server(debug=True)


if __name__ == "__main__":
    render_visualization()