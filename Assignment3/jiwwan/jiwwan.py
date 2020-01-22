# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import urllib.request as req
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

# load the dataset from data server for ECS 272 Winter 2020
dataset = req.urlopen('http://stream.cs.ucdavis.edu/datasets/LAX_Terminal_Passengers.csv')
data = pd.read_csv(dataset)



import plotly.graph_objects as go
from plotly.graph_objects import *


# indicator: Domestic or International
available_indicators = data['Domestic_International'].unique()




# ==================================== Dash setting ==================================

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.Div(children='''
        LAX terminal passengers data visualization. By Jingwei Wan
    '''),

    html.Div([
        dcc.Dropdown(
            id = 'Dome_Inte',
            options = [{'label': i, 'value': i} for i in available_indicators],
            value = 'Domestic'
        )
    ],
    style={'width': '48%', 'display': 'inline-block'}
),

    dcc.Graph(
        id='indicator-graphic'
    ),



    html.Div([
        dcc.Dropdown(
            id = 'Dome_Inte2',
            options = [{'label': i, 'value': i} for i in available_indicators],
            value = 'Domestic'
        )
    ],
    style={'width': '48%', 'display': 'inline-block'}
),


    dcc.Graph(
        id='indicator-graphic2'
    )

])


# The first graph: Average number of passengers of each terminal through all these years
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('Dome_Inte', 'value')])
def update_graph(Dome_Inte):
    dff = data[data['Domestic_International'] == Dome_Inte]
    keys1 = ['Terminal']
    groups1 = dff.groupby(keys1, as_index=keys1, sort=False)
    result1 = groups1['Passenger_Count'].mean().to_frame().reset_index()

    x = result1['Terminal']
    y = result1['Passenger_Count']
    xy = zip(x, y)
    xy = sorted(xy)
    x_sorted = [x for x, y in xy]
    y_sorted = [y for x, y in xy]

    # plot the average number of passengers of each terminal
    fig1 = go.Figure(
        data=[go.Bar(x=x_sorted, y=y_sorted)],
        layout=go.Layout(
            title=go.layout.Title(text='Average number of passengers of each terminal')
        )
    )
    return fig1


# The second graph: Number of passengers of each terminal from 2006 to 2019 (streamgraph)
@app.callback(
    Output('indicator-graphic2', 'figure'),
    [Input('Dome_Inte2', 'value')])
def update_graph(Dome_Inte):
    dff = data[data['Domestic_International'] == Dome_Inte]

    # ============================= passengers of each terminal v.s. years ====================================================================
    keys2 = ['Terminal']
    groups2 = dff.groupby(keys2, as_index=keys2, sort=False)  # group by terminal
    terminal_list = list(groups2.groups.keys())  # get the name list of terminal

    # store the number of passengers
    pas = []
    for name, group in groups2:
        subgroup = group.groupby(['ReportPeriod'], as_index=['ReportPeriod'], sort=False)
        subresult = subgroup['Passenger_Count'].sum().to_frame().reset_index()
        pas.append(list(subresult['Passenger_Count']))
    for i in range(len(pas)):
        temp = np.zeros(len(pas[-1])).tolist()
        temp[:len(pas[i])] = pas[i]
        pas[i] = temp

    # Get time data
    years = np.arange(len(pas[0]))

    # Modify our data to satisfy the requirement of streamgraph
    pasTemp = np.zeros((len(pas), len(pas[0])))


    for i in range(len(pas[0])):
        yMax = np.sum([pas[k][i] for k in range(len(pas))])
        for j in range(len(pas)):
            pasTemp[j, i] = np.sum([pas[k][i] for k in range(j + 1)]) - yMax / 2


    trace1 = {
        "fill": "tonexty",
        "line": {
            "color": "#cdcdd8",
            "shape": "spline",
            "width": 0
        },
        "name": terminal_list[0],
        "type": "scatter",
        "x": years,
        "y": pasTemp[0],
        "hovertext": [terminal_list[0] + ': ' + str(pas[0][i]) for i in range(len(pas[0]))],
        "hoverinfo": "text",
        "fillcolor": "#cdcdd8"
    }
    trace2 = {
        "fill": "tonexty",
        "line": {
            "color": "#0202ef",
            "shape": "spline",
            "width": 0
        },
        "name": terminal_list[1],
        "type": "scatter",
        "x": years,
        "y": pasTemp[1],
        "hovertext": [terminal_list[1] + ': ' + str(pas[1][i]) for i in range(len(pas[0]))],
        "hoverinfo": "text",
        "fillcolor": "#0202ef"
    }
    trace3 = {
        "fill": "tonexty",
        "line": {
            "color": "#8f8ff7",
            "shape": "spline",
            "width": 0
        },
        "name": terminal_list[2],
        "type": "scatter",
        "x": years,
        "y": pasTemp[2],
        "hovertext": [terminal_list[2] + ': ' + str(pas[2][i]) for i in range(len(pas[0]))],
        "hoverinfo": "text",
        "fillcolor": "#8f8ff7"
    }
    trace4 = {
        "fill": "tonexty",
        "line": {
            "color": "#f7960e",
            "shape": "spline",
            "width": 0
        },
        "name": terminal_list[3],
        "type": "scatter",
        "x": years,
        "y": pasTemp[3],
        "hovertext": [terminal_list[3] + ': ' + str(pas[3][i]) for i in range(len(pas[0]))],
        "hoverinfo": "text",
        "fillcolor": "#f7960e"
    }
    trace5 = {
        "fill": "tonexty",
        "line": {
            "color": "#f2c382",
            "shape": "spline",
            "width": 0
        },
        "name": terminal_list[4],
        "type": "scatter",
        "x": years,
        "y": pasTemp[4],
        "hovertext": [terminal_list[4] + ': ' + str(pas[4][i]) for i in range(len(pas[0]))],
        "hoverinfo": "text",
        "fillcolor": "#f2c382"
    }
    trace6 = {
        "fill": "tonexty",
        "line": {
            "color": "#f21602",
            "shape": "spline",
            "width": 0
        },
        "name": terminal_list[5],
        "type": "scatter",
        "x": years,
        "y": pasTemp[5],
        "hovertext": [terminal_list[5] + ': ' + str(pas[5][i]) for i in range(len(pas[0]))],
        "hoverinfo": "text",
        "fillcolor": "#f21602"
    }
    trace7 = {
        "fill": "tonexty",
        "line": {
            "color": "#edbdb8",
            "shape": "spline",
            "width": 0
        },
        "name": terminal_list[6],
        "type": "scatter",
        "x": years,
        "y": pasTemp[6],
        "hovertext": [terminal_list[6] + ': ' + str(pas[6][i]) for i in range(len(pas[0]))],
        "hoverinfo": "text",
        "fillcolor": "#edbdb8"
    }
    trace8 = {
        "fill": "tonexty",
        "line": {
            "color": "#25b8f7",
            "shape": "spline",
            "width": 0
        },
        "name": terminal_list[7],
        "type": "scatter",
        "x": years,
        "y": pasTemp[7],
        "hovertext": [terminal_list[7] + ': ' + str(pas[7][i]) for i in range(len(pas[0]))],
        "hoverinfo": "text",
        "fillcolor": "#25b8f7"
    }
    trace9 = {
        "fill": "tonexty",
        "line": {
            "color": "#b7e4f7",
            "shape": "spline",
            "width": 0
        },
        "name": terminal_list[8],
        "type": "scatter",
        "x": years,
        "y": pasTemp[8],
        "hovertext": [terminal_list[8] + ': ' + str(pas[8][i]) for i in range(len(pas[0]))],
        "hoverinfo": "text",
        "fillcolor": "#b7e4f7"
    }
    trace10 = {
        "fill": "tonexty",
        "line": {
            "color": "#5AA8BB",
            "shape": "spline",
            "width": 0
        },
        "name": terminal_list[9],
        "type": "scatter",
        "x": years,
        "y": pasTemp[9],
        "hovertext": [terminal_list[9] + ': ' + str(pas[9][i]) for i in range(len(pas[0]))],
        "hoverinfo": "text",
        "fillcolor": "#5AA8BB"
    }
    trace11 = {
        "fill": "tonexty",
        "line": {
            "color": "#C1C8C8",
            "shape": "spline",
            "width": 0
        },
        "name": terminal_list[10],
        "type": "scatter",
        "x": years,
        "y": pasTemp[10],
        "hovertext": [terminal_list[10] + ': ' + str(pas[10][i]) for i in range(len(pas[0]))],
        "hoverinfo": "text",
        "fillcolor": "#C1C8C8"
    }

    layout = {
        "title": "Number of passengers of each terminal from 2006 to 2019",
        "width": 1400,
        "xaxis": {
            "ticks": "outside",
            "ticktext": [str(i) for i in range(2006, 2021)],
            "tickvals": [12 * i for i in range(14)],
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
    fig2 = Figure(data=[trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11],
                  layout=layout)

    return fig2








if __name__ == '__main__':
    app.run_server(debug=True)