import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

df = pd.read_csv('http://stream.cs.ucdavis.edu/datasets/SF_Historical_Ballot_Measures.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(Year): str(Year) for Year in df['Year'].unique()},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.Year == selected_year]
    traces = []
    for i in filtered_df.Letter.unique():
        df_by_continent = filtered_df[filtered_df['Type Measure'] == i]
        traces.append(dict(
            x=df_by_continent['Yes Votes'],
            y=df_by_continent['No Votes'],
            text=df_by_continent['Subject'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Yes Votes', 'range':[10000, 310000]},
            yaxis={'title': 'No Votes', 'range':[10000, 240000]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)