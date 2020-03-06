import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('http://stream.cs.ucdavis.edu/datasets/SF_Historical_Ballot_Measures.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


default_values = ["Year", "Yes Votes", "No Votes", "Percent"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': x, 'value': x} for x in df.Letter
        ],
        value=default_values
    ),

    dcc.Graph(
        id='plot-graph',
#        figure=draw_parallel_plot(df, default_values)
),
    html.Div(id="table")
])


@app.callback(
    Output('plot-graph', 'figure'),
    [Input('demo-dropdown', 'value')])
def update_figure(value):
    dimensions = []
    for axe in value:
        dimensions.append(
            dict(range = [df[axe].min(),df[axe].max()],
                 tickvals = [],
                 label = axe, values = df[axe]),
        )
    fig = go.Figure(data=
    go.Parcoords(
        line = dict(color = df['Year'],
                    colorscale = 'earth',
                    ),
        dimensions = dimensions
    )
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)