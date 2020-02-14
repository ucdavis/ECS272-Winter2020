import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import pandas
import os
import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# gets the pokemon dataset; csv file should be in the dataset folder
relative_path = os.path.join('..', 'dataset', 'pokemon_alopez247.csv')
dataset = pandas.read_csv(relative_path)

def get_stat_vector(df):
    df_copy = df.copy()
    df_copy['HP'] = df.apply(lambda row: (row['HP']/255), axis=1)
    df_copy['Attack'] = df.apply(lambda row: (row['Attack']/154), axis=1)
    df_copy['Defense'] = df.apply(lambda row: (row['Defense']/230), axis=1)
    df_copy['Sp_Atk'] = df.apply(lambda row: (row['Sp_Atk']/160), axis=1)
    df_copy['Sp_Def'] = df.apply(lambda row: (row['Sp_Def']/230), axis=1)
    df_copy['Speed'] = df.apply(lambda row: (row['Speed']/160), axis=1)
    stat_vectors = df_copy[['HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed']].copy()
    return stat_vectors.values

def get_clusters(stat_vectors, k):
    dbscan = KMeans(n_clusters=k, random_state=0)
    clustering = dbscan.fit(stat_vectors)
    return clustering.labels_.tolist()

def apply_labels(labels, df):
    df['Cluster'] = df.apply(lambda row: labels[row['Number'] - 1], axis=1)
    return df

# To reduce redunant computation, dataframe and PCA'd data is returned
def label_clusters(df, k):
    stat_vectors = get_stat_vector(df)
    # PCA into 2-space
    pca = PCA(n_components=2)
    pc = pca.fit_transform(stat_vectors)
    pc = np.concatenate((np.asarray(df), pc), 1)
    labels = ['Number', 'Name', 'Type_1', 'Type_2', 'Total', 'HP', 'Attack', 'Defense', 'Sp_Atk',
    'Sp_Def', 'Speed', 'Generation', 'isLegendary', 'Color', 'hasGender', 'Pr_Male', 'Egg_Group_1',
    'Egg_Group_2', 'hasMegaEvolution', 'Height_m', 'Weight_kg', 'Catch_Rate', 'Body_Style', 'x', 'y']
    new_df = pandas.DataFrame(data=pc, index=pc[0:,0], columns=labels)
    clusters = get_clusters(stat_vectors, k)
    return apply_labels(clusters, new_df)

# creates the cluster scatter plot
def create_cluster_scatterplot(df, k=5):
    random.seed(21)
    labelled_df = label_clusters(df, k)
    labelled_df['Cluster'] = labelled_df['Cluster'].astype(str)
    fig = px.scatter(labelled_df, x='x', y='y', color='Cluster', hover_data=['Name'],
                     category_orders={'Cluster': [str(index) for index in range(10)]})
    fig.update(layout_coloraxis_showscale=False)
    fig.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        title={'text': 'K-Means Scatter Plot On PCA\'d Data', 'y': 0.97, 'x': 0.5,
               'xanchor': 'center', 'yanchor': 'top'}
    )
    return fig

# creates the basic bar chart
def create_basic_bar_chart(pokemon_name):
    pokemon_type1 = dataset.loc[dataset['Name'] == pokemon_name, 'Type_1'].values[0]

    # gets all pokemon with the same main type as the selected
    subset = dataset.loc[dataset['Type_1'] == pokemon_type1]

    # sort the pokemon based on their total stats, descending
    sorted_subset = subset.sort_values(by='Total', ascending=False)
    sorted_subset_names = sorted_subset['Name'].values.tolist()
    sorted_subset_vals = sorted_subset['Total'].values.tolist()

    target_index = sorted_subset_names.index(pokemon_name)

    # label each pokemon with their ranking
    for index in range(len(sorted_subset_names)):
        ranking = index + 1
        sorted_subset_names[index] = sorted_subset_names[index] + ', #' + str(ranking)

    # bars that occur before the selected pokemon
    sorted_subset_names1 = sorted_subset_names[:target_index]
    sorted_subset_vals1 = sorted_subset_vals[:target_index]
    bar_colors1 = ['lightslategray', ] * len(sorted_subset_names1)

    # selected pokemon's bar
    sorted_subset_names2 = [sorted_subset_names[target_index]]
    sorted_subset_vals2 = [sorted_subset_vals[target_index]]
    bar_colors2 = ['crimson']

    # bars that occur after the selected pokemon
    sorted_subset_names3 = sorted_subset_names[target_index + 1:]
    sorted_subset_vals3 = sorted_subset_vals[target_index + 1:]
    bar_colors3 = ['lightslategray', ] * len(sorted_subset_names3)

    bar_fig = go.Figure()

    # creates traces for bars
    bar_fig.add_trace(go.Bar(x=sorted_subset_names1, y=sorted_subset_vals1, marker_color=bar_colors1,
                             name='Other Pokemon', showlegend=False))
    bar_fig.add_trace(go.Bar(x=sorted_subset_names2, y=sorted_subset_vals2, marker_color=bar_colors2,
                             name='Selected Pokemon'))
    bar_fig.add_trace(go.Bar(x=sorted_subset_names3, y=sorted_subset_vals3, marker_color=bar_colors3,
                             name='Other Pokemon', showlegend=False))

    # creates the actual bar chart
    bar_chart_title = str(pokemon_type1) + ' Main Type Total Stats Rankings Bar Chart'
    x_title = 'Pokemon Whose Main Type is ' + str(pokemon_type1) + ' by Descending Ranking'
    bar_fig.update_layout(title={'text': bar_chart_title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                          xaxis={'showticklabels': False, 'title': x_title},
                          yaxis={'title': 'Total Stats'}, legend_itemclick=False, legend_itemdoubleclick=False,
                          legend=dict(x=-.1, y=1.2), margin=dict(l=10, r=20, t=5, b=20))
    return bar_fig

# creates the advanced star plot
def create_advanced_star_plot(pokemon_name):
    # gets the pokemon's row
    data_sample = dataset.loc[dataset['Name'] == pokemon_name]

    stats = ['HP', 'Attack', 'Defense', 'SP Attack', 'SP Defense', 'Speed']
    stat_vals = [data_sample['HP'].values[0], data_sample['Attack'].values[0], data_sample['Sp_Atk'].values[0],
                 data_sample['Sp_Def'].values[0], data_sample['Speed'].values[0]]

    # creates the actual figure with the pokemon's stats
    star_fig = go.Figure(data=go.Scatterpolar(r=stat_vals, theta=stats, fill='toself', name='Pokemon Stats'))

    star_plot_title = str(pokemon_name) + '\'s Stats Star Plot'
    star_fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 255]
            ),
        ),
        showlegend=False,
        title={'text': star_plot_title, 'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
        margin=dict(l=55, r=55, t=55, b=55)
    )

    return star_fig

app.layout = html.Div(style={'padding': '1em', 'border-style': 'solid'}, children=[
    # main title
    html.H2(
        'ECS 272 InfoVis Assignment 4',
        style={
            'textAlign': 'center'
        }
    ),

    # parent flex container
    html.Div([
        # left side container
        html.Div([

            # left side's header
            html.H4(
                'Overview',
                style={
                    'textAlign': 'center'
                }
            ),

# container for slider and its header
            html.Div([
                # slider's header
                html.Label(
                    'Number of clusters',
                    style={
                        'textAlign': 'center',
                        'height': '5vh'
                    }
                ),

                # slider that controls how many clusters are used in the scatter plot
                html.Div([
                    dcc.Slider(
                        id='clusters',
                        min=2,
                        max=9,
                        step=1,
                        marks={
                            index: str(index) for index in range(2, 10)
                        },
                        value=4
                    )
                ], style={'margin-left': '4vw', 'margin-right': '4vw'})
            ], style={'height': '12vh'}),

            # overview graph; cluster scatter plot that uses PCA and k-means
            dcc.Graph(style={'height': '95vh'}, id='cluster_scatterplot',
                      figure=create_cluster_scatterplot(dataset, 4),
                      hoverData={'points': [{'customdata': ['Bulbasaur']}]}),



        ], style={'width': '50%', 'float': 'left'}),

        # right side's container
        html.Div([
            # right side's header
            html.H4(
                'Detailed View',
                style={
                    'textAlign': 'center',
                }
            ),

            # basic bar graph; shows the rankings of pokemon with the same main type as the selected
            dcc.Graph(style={'height': '55vh'}, id='basic-bar-chart'),
            # advanced star plot; shows the selected pokemon's stat breakdown
            dcc.Graph(style={'height': '55vh'}, id='advanced-star-plot')

        ], style={'width': '50%', 'float': 'left'})
    ], style={'display': 'flex'})

])

# callback that updates the basic bar chart when a hover event occurs with the scatter plot
@app.callback(
    dash.dependencies.Output('basic-bar-chart', 'figure'),
    [dash.dependencies.Input('cluster_scatterplot', 'hoverData')])
def update_bar_chart(hover_data):
    pokemon_name = hover_data['points'][0]['customdata'][0]
    return create_basic_bar_chart(pokemon_name)

# callback that updates the advanced star plot when a hover event occurs with the scatter plot
@app.callback(
    dash.dependencies.Output('advanced-star-plot', 'figure'),
    [dash.dependencies.Input('cluster_scatterplot', 'hoverData')])
def update_bar_chart(hover_data):
    pokemon_name = hover_data['points'][0]['customdata'][0]
    return create_advanced_star_plot(pokemon_name)

# callback that updates the scatter plot depending on how many clusters are selected in the slider
@app.callback(
    dash.dependencies.Output('cluster_scatterplot', 'figure'),
    [dash.dependencies.Input('clusters', 'value')])
def update_clusters(value):
    return create_cluster_scatterplot(dataset, value)

if __name__ == '__main__':
    app.run_server(debug=True)
