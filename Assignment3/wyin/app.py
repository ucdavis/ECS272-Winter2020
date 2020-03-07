import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

df = pd.read_csv("../datasets/Los_Angeles_International_Airport_-_Passenger_Traffic_By_Terminal.csv")
df['ReportPeriod']=pd.to_datetime(df['ReportPeriod'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='ECS 272 Assignment 3'),

    html.Div(children='''
        Choose a terminal you are interested in.
    '''),

    dcc.Dropdown(
        id = 'terminal_dropdown',
        options = [
            {'label': 'Imperial Terminal', 'value': 'Imperial Terminal'},
            {'label': 'Misc. Terminal', 'value': 'Misc. Terminal'},
            {'label': 'Terminal 1', 'value': 'Terminal 1'},
            {'label': 'Terminal 2', 'value': 'Terminal 2'},
            {'label': 'Terminal 3', 'value': 'Terminal 3'},
            {'label': 'Terminal 4', 'value': 'Terminal 4'},
            {'label': 'Terminal 5', 'value': 'Terminal 5'},
            {'label': 'Terminal 6', 'value': 'Terminal 6'},
            {'label': 'Terminal 7', 'value': 'Terminal 7'},
            {'label': 'Terminal 8', 'value': 'Terminal 8'},
            {'label': 'Tom Bradley International Terminal', 'value': 'Tom Bradley International Terminal'},
        ],
        value = 'Imperial Terminal'
    ),

    dcc.Graph(
        id='basic_graph'
    ),

    html.Div(children='''
        Choose a year you are interested in.
    '''),

    dcc.Slider(
        id = 'year_slider',
        min = 2006,
        max = 2019,
        marks = {i: '{}'.format(i) for i in range(2006,2020)},
        value = 2006
    ),

    dcc.Graph(
        id='adv_graph'
    )
])

@app.callback(
    Output('basic_graph', 'figure'),
    [Input('terminal_dropdown', 'value')])
def update_basic_figure(terminal):
    figure={
        'data': [
            {'x': ["Domestic", "International"], 'y': [sum(df[df.Domestic_International == "Domestic"][df.Terminal == str(terminal)]["Passenger_Count"]),
                                                       sum(df[df.Domestic_International == "International"][df.Terminal == str(terminal)]["Passenger_Count"])],
                                                       'type': 'bar',
                                                       'name': 'temp'},
        ],
        'layout': {
            'title': 'Basic graph view'
        }
    }
    return figure

@app.callback(
    Output('adv_graph', 'figure'),
    [Input('year_slider', 'value')])
def update_advanced_figure(year):
    filtered_df = df[df['ReportPeriod'].dt.year == year][['Terminal', 'Domestic_International', 'Arrival_Departure']]
    figure = px.parallel_categories(filtered_df, dimensions_max_cardinality = 12)
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
