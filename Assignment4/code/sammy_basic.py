import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# gets the ballot measures dataset; csv file should be in the datasets folder
relative_path = os.path.join('..', 'dataset', 'pokemon_alopez247.csv')
dataset = pandas.read_csv(relative_path)


def create_basic_bar_chart():
    subset = dataset.loc[dataset['Type_1'] == 'Grass']

    sorted_subset = subset.sort_values(by='Total', ascending=False)
    sorted_subset_names = sorted_subset['Name'].values.tolist()
    sorted_subset_vals = sorted_subset['Total'].values.tolist()

    target_index = sorted_subset_names.index('Bulbasaur')

    bar_colors = ['lightslategray', ] * len(sorted_subset_names)
    bar_colors[target_index] = 'crimson'

    for index in range(len(sorted_subset_names)):
        ranking = index + 1
        sorted_subset_names[index] = sorted_subset_names[index] + ', #' + str(ranking)

    bar_fig = go.Figure(data=[
        go.Bar(x=sorted_subset_names, y=sorted_subset_vals, marker_color=bar_colors)
    ])

    bar_chart_title = 'Grass Type Total Stats Ranking Bar Chart'
    bar_fig.update_layout(title={'text': bar_chart_title, 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
    return bar_fig


def create_advanced_star_plot():
    data_sample = dataset.loc[dataset['Name'] == 'Bulbasaur']

    stats = ['HP', 'Attack', 'Defense', 'SP Attack', 'SP Defense', 'Speed']
    stat_vals = [data_sample.at[0, 'HP'], data_sample.at[0, 'Attack'], data_sample.at[0, 'Sp_Atk'],
                 data_sample.at[0, 'Sp_Def'], data_sample.at[0, 'Speed']]

    star_fig = go.Figure(data=go.Scatterpolar(r=stat_vals, theta=stats, fill='toself'))

    star_plot_title = 'Bulbasaur\'s Stats Bar Chart'
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
        dcc.Graph(id='advanced-star-plot', figure=create_advanced_star_plot())
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
