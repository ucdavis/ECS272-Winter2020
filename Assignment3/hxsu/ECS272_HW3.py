# ECS 272 HW3 2020 Winter Quarter
# Hang Su 916634573

# Import packages
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import urllib.request as req
import numpy as np
from dash.dependencies import Input, Output

# load the dataset from data server
dataset = req.urlopen('http://stream.cs.ucdavis.edu/datasets/LAX_Terminal_Passengers.csv')
data = pd.read_csv(dataset)

# Prepcocessing of data, dropping data with missing value
data = data.dropna()



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Options for dropdown menu
available_indicators = data['Domestic_International'].unique()
available_indicators_2 = data['Arrival_Departure'].unique()

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='passenger_type_1',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='Domestic'
        )
    ],
        style={'width': '48%', 'display': 'inline-block'}

    ),
    dcc.Graph(id='indicator-graphic_1'),

    html.Div([
        dcc.Dropdown(
            id='passenger_type_2',
            options=[{'label': i, 'value': i} for i in available_indicators_2],
            value='Arrival'
        )
    ],
        style={'width': '48%', 'display': 'inline-block'}
    ),

    dcc.Graph(id='indicator-graphic_2')

])

# Update Figure 1, basic one
@app.callback(
    Output('indicator-graphic_1', 'figure'),
    [Input('passenger_type_1', 'value')])
def update_graph(passenger_type_1):
    dff = data.loc[data['Domestic_International'] == passenger_type_1]
    keys = ['Terminal']
    groups = dff.groupby(keys, as_index=keys, sort=True)
    vis_1 = groups['Passenger_Count'].sum().to_frame().reset_index()
    x = vis_1['Terminal']
    y = vis_1['Passenger_Count']

    return {
        'data': [
            {'x': x, 'y': y, 'type': 'bar', 'name': passenger_type_1},
        ],
        'layout': {
            'title': 'Overall passengers of LAX (01/01/2006 to 03/01/2019)'
        }
    }

# Update figure 2, the advanced one
@app.callback(
    Output('indicator-graphic_2', 'figure'),
    [Input('passenger_type_2', 'value')])
def update_graph(passenger_type_2):
    dff = data[data['Arrival_Departure'] == passenger_type_2]
    # Months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    Time = ['01/01/', '02/01/', '03/01/', '04/01/', '05/01/', '06/01/', '07/01/', '08/01/', '09/01/', '10/01/',
            '11/01/', '12/01/']
    keys = ['Terminal']

    groups = dff.groupby(keys, as_index=keys, sort=True)

    stream_temp = np.zeros((11, 12))
    terminal_list = list(groups.groups.keys())
    for i in range(11):
        # v1 = vis3[vis3["Terminal"] == terminal_list[i]]
        for j in range(12):
            data3 = dff[dff['ReportPeriod'].str.contains(Time[j]) == True]
            groups = data3.groupby(keys, as_index=keys, sort=True)
            # Total number of passengers in January for different terminals
            vis3 = groups['Passenger_Count'].sum().to_frame().reset_index()
            if j < 3:
                vis3['Passenger_Count'] = vis3['Passenger_Count'].div(14)
            else:
                vis3['Passenger_Count'] = vis3['Passenger_Count'].div(13)

            vis3['Passenger_Count'] = vis3['Passenger_Count'].astype('int64')

            stream_temp[i, j] = vis3[vis3["Terminal"] == terminal_list[i]].Passenger_Count

    stream = np.zeros((11, 12))

    # Data for stream graph
    for n in range(12):
        y_max = np.sum([stream_temp[k, n] for k in range(11)])
        for m in range(11):
            stream[m, n] = np.sum([stream_temp[k, n] for k in range(m + 1)]) - y_max / 2

    traces = []
    colors = ["#C1C8C8", "#5AA8BB", "#b7e4f7", "#25b8f7", "#edbdb8", "#f21602", "#f2c382", "#f7960e", "#8f8ff7",
              "#0202ef", "#cdcdd8"]
    for k in range(11):
        trace = {
            "fill": "tonexty",
            "line": {
                "color": colors[k],
                "shape": "spline",
                "width": 0
            },
            "name": terminal_list[0],
            "type": "scatter",
            "x": month,
            "y": stream[k],
            "hovertext": [terminal_list[k] + ":" + str(stream_temp[k, i]) for i in range(12)],
            "hoverinfo": "text",
            "fillcolor": colors[k]

        }
        traces.append(trace)

    return {
        'data': traces,
        'layout': {
            "title": "Averaged Monthly passenger count of LAX ((01/01/2006 to 03/01/2019))",
            "width": 1400,
            "xaxis": {
                "ticks": "Outside",
                "ticktext": month,
                "tickvals": 1,
                "mirror": True,
                "ticklen": 5,
                "showgrid": False,
                "showline": True,
                "tickfont": {
                    "size": 11,
                    "color": "rgb(107, 107, 107)"
                },
                "tickwidth": 1,
                "showticklabels": True
            },
            "yaxis": {
                "ticks": "",
                "title": "",
                "mirror": True,
                "ticklen": 5,
                "showgrid": False,
                "showline": True,
                "tickfont": {
                    "size": 11,
                    "color": "rgb(107, 107, 107)"
                },
                "zeroline": True,
                "tickwidth": 1,
                "showticklabels": False,
            },
            "height": 600,
            "margin": {
                "b": 60,
                "l": 60,
                "r": 60,
                "t": 80
            },
            "autosize": False,
            "hovermode": "x",
            "showlegend": False

        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)
