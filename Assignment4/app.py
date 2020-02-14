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

#import data frame
from cluster_comp import df, MAX_CLUSTERS

#globals
CURRENT_CLUSTER_NO = 3

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

#construct cluster options
cluster_option_list = []
for val in range(1,MAX_CLUSTERS):
    val += 1
    cluster_option_list.append({'label' : str(val)+ ' Clusters', 'value' : val})

#begin visualization
def render_visualization():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([

        html.Div([
            html.Div(html.H1("Young People Survey")),
        ],className="row", style={'width' : '100%'}),

        html.Div([

            html.Div(html.H4("Choose a cluster"), style={'width' : '30%'}, className='three columns'),

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
                    options=cluster_option_list,
                    value=3,
                    className='six columns',
                    style={'width': '45%'}
                )
            ], className="three columns", style={'backgroundColor' : 'rgb(220,220,220)', 'width' : '25%'})
        ],className="row"),

        html.Div([
            html.Div(
                    dcc.Graph(
                            id='3d-plot',
                            style={'height' : '50em'}
                        ),
                    className='six columns',
                    style={'width': '50em', 'height': '50em', 'backgroundColor' : 'rgb(0,0,0)'}
                ),
            html.Div(
                    dcc.Graph(
                        id='corr-heatmap',
                        style={'height' : '50em'}
                    ),
                    className='six columns',
                    style={'width': '50em', 'height' : '50em'}),
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
        
        #reset the current clusterNo
        CURRENT_CLUSTER_NO = clusterNo

        fig = go.Figure()

        for x in range(clusterNo):
            fig.add_trace(go.Scatter3d(x=df[df["clusterGrouping{}".format(clusterNo)] == str(x)]['xcoord'].tolist(),
                                        y=df[df["clusterGrouping{}".format(clusterNo)] == str(x)]['ycoord'].tolist(),
                                        z=df[df["clusterGrouping{}".format(clusterNo)] == str(x)]['zcoord'].tolist(),
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
        
        #choose cluster
        if click_data:
            chosen_cluster = str(click_data["points"][0]['curveNumber'])
        else:
            chosen_cluster = "0"
        
        df_selected = df[df['clusterGrouping' + str(CURRENT_CLUSTER_NO)] == chosen_cluster]
            
        #choose columns
        chosen_columns = []
        for choice in category_choices:
            chosen_columns = chosen_columns + question_categories[choice]

        df_selected = df_selected[chosen_columns]
        
        #matrix of correlated values
        #masked with triangular matrix (so don't have repeat values)
        matrix = df_selected.corr().values.tolist()
        mask = np.tri(len(df_selected.columns), k=0)
        matrix = np.ma.array(matrix, mask=mask)  #bug here, with categorical data

        fig = go.Figure(data=go.Heatmap(z=[np.flip(x) for x in matrix.filled(np.nan)],
                                        x=[x for x in np.flip(df_selected.columns)[:-1]],
                                        y=[x for x in df_selected.columns[:-1]],
                                        colorscale='gray_r',
                                        hoverongaps=False
                                        )
                        )

        fig.update_layout(title={'text' : "Correlation Coefficients in Cluster {}".format(chosen_cluster),
                                    'x' : 0.57,
                                    'xanchor' : 'center',
                                    'y' : 0.9,
                                    'yanchor' : 'middle'
                                },
                            titlefont={'size' : 25},
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

        for column in chosen_columns:
            for clusterNo in range(number_of_clusters):
                fig.add_trace(go.Violin(y=df[column][df["clusterGrouping{}".format(number_of_clusters)] == str(clusterNo)],
                                        name=column,
                                        legendgroup="Cluster {}".format(clusterNo),
                                        #box_visible=True,
                                        meanline_visible=True,
                                        line_color=default_colors[clusterNo],
                                        opacity=0.4)
                            )

        #for clusterNo in range(number_of_clusters):
        # clusterNo = 1

        # fig.add_trace(go.Violin(y=df[df["clusterGrouping{}".format(number_of_clusters)] == str(clusterNo)],
        #                         x=chosen_columns,
        #                         legendgroup="Cluster {}".format(clusterNo),
        #                         box_visible=True,
        #                         meanline_visible=True,
        #                         line_color=default_colors[clusterNo],
        #                         opacity=0.4,
        #                         points='all')
        #             )

        fig.update_traces(side='positive', points=False, width = 1.5)
        fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False, width=len(chosen_columns) * 100, autosize=False, height=750)

        return fig

    app.run_server(debug=True)

if __name__ == "__main__":
    render_visualization()
