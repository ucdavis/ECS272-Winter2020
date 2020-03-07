import plotly.graph_objects as go
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv(
    '/Users/Vincent/Google 云端硬盘/MS/Winter/ECS272 Info Visu/ECS272-Winter2020/Assignment4/pokemon/pokemon_alopez247.csv')
columns = df.columns

# Pie Chart
has_gen = len(df[df['hasGender'] == True].index)
not_has_gen = len(df[df['hasGender'] == False].index)

app.layout = html.Div(children=[
    html.H2(children='ECS272 Assignment 4'),
    html.H5(children=['Binxin Dong',
                      html.Br(),
                      'Shuotong Wang']),

    html.Div([
        html.P(['The visualization consists of three views:',
                html.Br(), '1. A pie chart showing whether the Pokémons has gender or not.',
                html.Br(), '2. A Scatter graph showing HP vs Speed of Pokémons.',
                html.Br(), '3. A Parallel Categorical graph showing Generation, Legendary or not, and Color of Lasso-selected Pokémons.',
                ])
    ]),

    html.Button('Clear Selection', id='clr_btn'),

    # Pie Chart + scatter plot
    html.Div([
        html.Div(dcc.Graph(id='pie_chart',
                           figure=go.Figure(
                               data=go.Pie(labels=['True', 'False'],
                                           values=[has_gen, not_has_gen],
                                           title='Has Gender vs. Not Has Gender of Pokémons'),
                               layout=go.Layout({'clickmode': 'event+select'})
                           )), style={'display': 'inline-block', 'width': '33%'}),
        html.Div([dcc.Graph(id='scatter_plot'),
                  html.Label('Select value of k for K-Mean Clustering:'),
                  dcc.Slider(
                      id='k_slider',
                      min=1,
                      max=5,
                      step=1,
                      value=3,
                      marks={i: 'K Value: {}'.format(i) if i == 3 else str(i) for i in range(1, 6)}
                  )
                  ], style={'display': 'inline-block', 'width': '66%'})
    ]),

    html.Div(dcc.Graph(id='parcat_plot'),
             style={'display': 'inline-block',
                    'width': '100%'}),

    # Support hidden view to pass dataFrame between callbacks
    html.Div(id='df_s', style={'display': 'none'})
])


@app.callback(
    Output('clr_btn', 'n_clicks'),
    [Input('pie_chart', 'clickData')]
)
def update_n_click(pie_event):
    if pie_event:
        return None


@app.callback(
    [Output('scatter_plot', 'figure'),
     Output('df_s', 'children')],
    [Input('pie_chart', 'clickData'),
     Input('k_slider', 'value'),
     Input('clr_btn', 'n_clicks')])
def display_scatter(clickData, k_value, n_clicks):
    df_s = pd.DataFrame(columns=columns)
    if clickData and clickData['points'][0]['pointNumber'] == 0:
        df_s = df[df['hasGender'] == True]
    elif clickData and clickData['points'][0]['pointNumber'] == 1:
        df_s = df[df['hasGender'] == False]
    else:
        df_s = df

    if n_clicks:
        df_s = df

    # Prepare Scatter Plot
    k_value = k_value if k_value else 3
    kmeans = KMeans(n_clusters=k_value).fit(df_s[['HP', 'Speed']])
    scatter_plot = go.Scatter(x=df_s['HP'],
                              y=df_s['Speed'],
                              #marker=dict(color=kmeans.labels_),
                              marker=dict(size = 6, line=dict(color='rgb(0, 0, 0)', width=0.5), color=kmeans.labels_, opacity=1),
                              mode='markers',
                              selected={'marker': {'color': 'royalblue'}},
                              unselected={'marker': {'opacity': 0.3}})
    layout = go.Layout(
        xaxis={'title': 'HP'},
        yaxis={'title': 'Speed'},
        dragmode='lasso',
        hovermode='closest')

    return [{'data': [scatter_plot], 'layout': layout},
            df_s.to_json(date_format='iso', orient='split')]


@app.callback(
    [Output('parcat_plot', 'figure')],
    [Input('scatter_plot', 'selectedData'),
     Input('df_s', 'children'),
     Input('clr_btn', 'n_clicks')])
def display_parcat(selectData, df_s, n_clicks):
    if not df_s:
        df_s = df
    else:
        df_s = pd.read_json(df_s, orient='split')

    if n_clicks:
        df_s = df

    color = np.zeros(len(df_s), dtype='uint8')
    colorscale = [[0, 'gray'], [1, 'royalblue']]

    categorical_dimensions = ['Generation', 'isLegendary', 'Color']
    dimensions = [dict(values=df_s[label], label=label) for label in categorical_dimensions]
    parcat_plot = go.Parcats(dimensions=dimensions,
                             line={'colorscale': colorscale, 'cmin': 0, 'cmax': 1, 'color': color, 'shape': 'hspline'}
                             )

    # Update parcats colors
    if selectData:
        new_color = np.zeros(len(df_s), dtype='uint8')
        for point in selectData['points']:
            new_color[point['pointIndex']] = 1

        parcat_plot.line.color = new_color

    return [{'data': [parcat_plot]}]


if __name__ == '__main__':
    app.run_server(debug=False)
