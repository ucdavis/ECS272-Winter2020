import dash
import datetime
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import urllib.request as req
import pandas as pd

# load the dataset from our data server for ECS 272 Winter 2020
dataset = req.urlopen('http://stream.cs.ucdavis.edu/datasets/LAX_Terminal_Passengers.csv')
df = pd.read_csv(dataset)

available_indicators = ['Domestic_International', 'Terminal', 'Arrival_Departure']

terminals = df['Terminal'].unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': 'white'}, children=[
    html.H1(children='EEC272 HW_3 Mingye Fu'),

    html.Div([
    html.Div(children='Bar Chart - passenger count (dropdown menu for different x axis columns)', style={
        'textAlign': 'center',
        'color': 'black',
        'fontSize': 30
    }),

    html.Div(children=[
        dcc.Dropdown(
            id='x_column',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='Terminal'
        )
    ],
        style={'width': '30%', 'display': 'inline-block'}),


    dcc.Graph(id='bar_chart'),
    ]),

    html.Div([

    html.Div(children='Stream graph - Domestic/International/Departure/Arrival vs Date (dropdown menu for different terminals)', style={
        'textAlign': 'center',
        'color': 'black',
        'fontSize': 30
    }),

    html.Div(children=[
        dcc.Dropdown(
            id='Terminal',
            options=[{'label': i, 'value': i} for i in terminals],
            value='Terminal 2'
        )
    ],
        style={'width': '30%', 'display': 'inline-block'}),

    dcc.Graph(id='stream')
    ])
])





@app.callback(
    Output('bar_chart', 'figure'),
    [Input('x_column', 'value')]
)
def update_graph(x_column):
    keys = [x_column]
    groups = df.groupby(keys)
    result1 = groups['Passenger_Count'].sum().to_frame().reset_index()
    return go.Figure(data=go.Bar(x=result1[x_column], y=result1['Passenger_Count']))


@app.callback(
    Output('stream', 'figure'),
    [Input('Terminal', 'value')]
)
def updata_graph(Terminal):
    dff = df[df['Terminal'] == Terminal]

    # Stack plot of passenger count
    arrival_international = dff[(dff['Arrival_Departure'] == 'Arrival') & (dff['Domestic_International'] == 'International')]
    groups = arrival_international.groupby(['ReportPeriod'], sort=False)
    df1 = groups['Passenger_Count'].sum().to_frame().reset_index()

    arrival_domestic = dff[(dff['Arrival_Departure'] == 'Arrival') & (dff['Domestic_International'] == 'Domestic')]
    groups =  arrival_domestic.groupby(['ReportPeriod'], sort=False)
    df2 = groups['Passenger_Count'].sum().to_frame().reset_index()

    departure_domestic = dff[(dff['Arrival_Departure'] == 'Departure') & (dff['Domestic_International'] == 'Domestic')]
    groups = departure_domestic.groupby(['ReportPeriod'], sort=False)
    df3 = groups['Passenger_Count'].sum().to_frame().reset_index()

    departure_international = dff[
        (dff['Arrival_Departure'] == 'Departure') & (dff['Domestic_International'] == 'International')]
    groups = departure_international.groupby(['ReportPeriod'], sort=False)
    df4 = groups['Passenger_Count'].sum().to_frame().reset_index()

    x = df['ReportPeriod'].unique()

    y_mean = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []

    for y, dfi in [(y1, df1), (y2, df2), (y3, df3), (y4, df4)]:
        j = 0
        for i in range(len(x)):
            if len(dfi[dfi['ReportPeriod'] == x[i]]) == 0:
                y.append(0)
            else:
                y.append(dfi['Passenger_Count'].values.tolist()[j])
                j = j + 1

    y1_real = y1.copy()
    y2_real = y2.copy()
    y3_real = y3.copy()
    y4_real = y4.copy()

    for i in range(len(x)):
        y2[i] = y2[i] + y1[i]
        y3[i] = y3[i] + y2[i]
        y4[i] = y4[i] + y3[i]
        y_mean.append(1 / 5 * (y1[i] + y2[i] + y3[i] + y4[i]))
        y5.append(y4[i] - y_mean[i])
        y4[i] = y3[i] - y_mean[i]
        y3[i] = y2[i] - y_mean[i]
        y2[i] = y1[i] - y_mean[i]
        y1[i] = - y_mean[i]

    x = pd.to_datetime(x)

    return {
        'data': [
            {
                'uid': '6adf8f',
                'line': {
                    'color': '#6a3f39',
                    'width': 0
                },
                'mode': 'lines',
                'name': 'International arrival',
                'type': 'scatter',
                'x': x,
                'y': y1,
                "hovertext": [str(x[i]) for i in range(len(x))],
                "hoverinfo": "text",
            },
            {
                'uid': '721fab',
                'fill': 'tonexty',
                'line': {
                    'color': '#6a3f39',
                    'shape': 'spline',
                    'width': 0
                },
                'name': 'Domestic arrival',
                'type': 'scatter',
                'x': x,
                'y': y2,
                "hovertext": ['International arrival:' + str(y1_real[i]) for i in range(len(y1))],
                "hoverinfo": "text",
                'fillcolor': '#6a3f39'
            },
            {
                'uid': 'fd616d',
                'fill': 'tonexty',
                'line': {
                    'color': '#a87c79',
                    'shape': 'spline',
                    'width': 0
                },
                'name': 'Domestic departure',
                'type': 'scatter',
                'x': x,
                'y': y3,
                "hovertext": ['Domestic arrival:' + str(y2_real[i]) for i in range(len(y2))],
                "hoverinfo": "text",
                'fillcolor': '#a87c79'
            },
            {
                'uid': '76d02d',
                'fill': 'tonexty',
                'line': {
                    'color': '#C0C0C0',
                    'shape': 'spline',
                    'width': 0
                },
                'name': 'International departure',
                'type': 'scatter',
                'x': x,
                'y': y4,
                "hovertext": ['Domestic departure:' + str(y3_real[i]) for i in range(len(y3))],
                "hoverinfo": "text",
                'fillcolor': '#C0C0C0',
            },
            {
                "uid": "408cb8",
                "fill": "tonexty",
                "line": {
                    "color": "#808080",
                    "shape": "spline",
                    "width": 0
                },
                "name": "",
                "type": "scatter",
                "x": x,
                'y': y5,
                "hovertext": ['International departure:' + str(y4_real[i]) for i in range(len(y4))],
                "hoverinfo": "text",
                "fillcolor": "#808080"
            }
        ],

        'layout': {
            'title': '',
            'width': 1500,
            'xaxis': {
                'type': 'DateTime',
                # 'type': 'linear',
                'range': [datetime.datetime(2006, 1, 1), datetime.datetime(2019, 3, 1)],
                'ticks': 'outside',
                'mirror': False,
                'ticklen': 5,
                'showgrid': True,
                'showline': True,
                'tickfont': {
                    'size': 11,
                    'color': 'rgb(107, 107, 107)'
                },
                'autorange': False,
                'tickwidth': 5,
                'showticklabels': True
            },
            'yaxis': {
                'type': 'linear',
                'range': [
                    -2000000,
                    2000000
                ],
                'ticks': 'outside',
                'title': '',
                'mirror': True,
                'ticklen': 1,
                'showgrid': False,
                'showline': True,
                'tickfont': {
                    'size': 11,
                    'color': 'rgb(107, 107, 107)'
                },
                'zeroline': False,
                'autorange': True,
                'tickwidth': 5,
                'showticklabels': False
            },
            'height': 800,
            'margin': {
                'b': 60,
                'l': 60,
                'r': 60,
                't': 80
            },
            'autosize': False,
            'hovermode': 'x',
            'showlegend': False,
            'annotations': [
                {
                    'x': 0,
                    'y': 0,
                    'font': {
                        'size': 12
                    },
                    'text': '',
                    'xref': 'paper',
                    'yref': 'paper',
                    'xanchor': 'left',
                    'yanchor': 'bottom',
                    'showarrow': False
                }
            ],
            'breakpoints': []
        },
        'frames': []
    }


if __name__ == '__main__':
    app.run_server(debug=True)
