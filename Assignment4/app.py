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

#import data frame
from cluster_comp import df, MAX_CLUSTERS

#globals
CURRENT_CLUSTER_NO = 3

#load the csv, if first time
#moved to data_comp

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

#construct cluster options
option_list = []
for val in range(1,MAX_CLUSTERS):
    val += 1
    option_list.append({'label' : str(val)+ ' Clusters', 'value' : val})

#begin visualization
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
                options=option_list,
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
        global CURRENT_CLUSTER_NO
        
        #reset the current clusterNo
        CURRENT_CLUSTER_NO = clusterNo

        ## if different cluster chosen, make new clusters
        #if clusterNo != CURRENT_CLUSTER_NO:
        #    df = dummy_cluster_norm(df, clusterNo)

        # 3d scatter plot of new data after df
        return px.scatter_3d(df, x='xcoord', y='ycoord', z='zcoord', color='clusterGrouping' + str(CURRENT_CLUSTER_NO))

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
        
        df_selected = df[df['clusterGrouping' + str(CURRENT_CLUSTER_NO)] == chosen_cluster]

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
                fig.add_trace(go.Violin(y=df[column][df['clusterGrouping' + str(CURRENT_CLUSTER_NO)] == str(clusterNo)],
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
