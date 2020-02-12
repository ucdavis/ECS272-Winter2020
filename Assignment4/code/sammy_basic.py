import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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

# gets the ballot measures dataset; csv file should be in the datasets folder
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
    dbscan = KMeans(n_clusters=k)
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

def create_cluster_scatterplot(df, k=5):
    random.seed(21)
    labelled_df = label_clusters(df, k)
    fig = px.scatter(labelled_df, x='x', y='y', color='Cluster', hover_data=['Name'])
    fig.update_layout(showlegend=False)
    return fig

def create_basic_bar_chart():
    subset = dataset.loc[dataset['Type_1'] == 'Grass']

    sorted_subset = subset.sort_values(by='Total', ascending=False)
    sorted_subset_names = sorted_subset['Name'].values.tolist()
    sorted_subset_vals = sorted_subset['Total'].values.tolist()

    target_index = sorted_subset_names.index('Bulbasaur')

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

    bar_fig.add_trace(go.Bar(x=sorted_subset_names1, y=sorted_subset_vals1, marker_color=bar_colors1,
                             name='Other Pokemon', showlegend=False))
    bar_fig.add_trace(go.Bar(x=sorted_subset_names2, y=sorted_subset_vals2, marker_color=bar_colors2,
                             name='Selected Pokemon'))
    bar_fig.add_trace(go.Bar(x=sorted_subset_names3, y=sorted_subset_vals3, marker_color=bar_colors3,
                             name='Other Pokemon', showlegend=False))

    bar_chart_title = 'Grass Type Total Stats Rankings Bar Chart'
    bar_fig.update_layout(title={'text': bar_chart_title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                          xaxis={'showticklabels': False, 'title': 'Grass Type Pokemon by Descending Ranking'},
                          yaxis={'title': 'Total Stats'}, legend_itemclick=False, legend_itemdoubleclick=False)
    return bar_fig


def create_advanced_star_plot():
    data_sample = dataset.loc[dataset['Name'] == 'Bulbasaur']

    stats = ['HP', 'Attack', 'Defense', 'SP Attack', 'SP Defense', 'Speed']
    stat_vals = [data_sample.at[0, 'HP'], data_sample.at[0, 'Attack'], data_sample.at[0, 'Sp_Atk'],
                 data_sample.at[0, 'Sp_Def'], data_sample.at[0, 'Speed']]

    star_fig = go.Figure(data=go.Scatterpolar(r=stat_vals, theta=stats, fill='toself'))

    star_plot_title = 'Bulbasaur\'s Stats Star Plot'
    star_fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False,
        title={'text': star_plot_title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}
    )

    return star_fig

app.layout = html.Div(style={'padding': '1em', 'border-style': 'solid'}, children=[
    html.H2(
        'ECS 272 InfoVis Assignment 4',
        style={
            'textAlign': 'center',
        }
    ),

    html.Div([
        # PCA graph goes here
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        # basic bar graph goes here; will show the stats of one pokemon
        dcc.Graph(id='basic-bar-chart', figure=create_basic_bar_chart()),
        dcc.Graph(id='advanced-star-plot', figure=create_advanced_star_plot()),
        dcc.Graph(id='cluster_scatterplot', figure=create_cluster_scatterplot(dataset, 4))
    ], style={'display': 'inline-block', 'width': '49%'})

])


# from tutorial, can be modified to fit bar chart
#@app.callback(
#    dash.dependencies.Output('x-time-series', 'figure'),
#    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
#def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
#    country_name = hoverData['points'][0]['customdata']
#    dff = df[df['Country Name'] == country_name]
#    dff = dff[dff['Indicator Name'] == xaxis_column_name]
#    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
#    return create_time_series(dff, axis_type, title)

if __name__ == '__main__':
    app.run_server(debug=True)
