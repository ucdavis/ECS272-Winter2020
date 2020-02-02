import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
import pandas as pd
import plotly.graph_objs as go
from collections import deque

import urllib.request as req
import pandas as pd
import csv

max_len = 50
times = deque(maxlen=max_len)
terminal = deque(maxlen=max_len)
Arrival_Departure = deque(maxlen=max_len)
Domestic_International = deque(maxlen=max_len)

graph2_dict = {
    'Terminal': terminal,
    'Arrival_Departure': Arrival_Departure,
    'Domestic_International': Domestic_International
}

def get_passenger_count_arr(data, index):
    result = []
    for i in range(len(data)):
        find_state = False
        for j in range(len(result) - 1, 0, -1):
            if data[i][1] == result[j][1] and data[i][index] == result[j][index]:
                find_state = True
                result[j][-1] = (int)(result[j][-1]) + (int)(data[i][-1])
        if find_state == False:
            result.append(data[i])
    return result

def preprocess():
    tmp_result = []
    with open('./Los_Angeles_International_Airport_-_Passenger_Traffic_By_Terminal.csv', 'r') as my_file:
        lines = csv.reader(my_file)
        count = 0
        for line in lines:
            count += 1
            tmp_date = line[1][:10]
            tmp_line = line
            if count != 1:
                tmp_line[1] = tmp_date[6:] + '/' + tmp_date[:2] + '/' + tmp_date[3:5]
            tmp_result.append(tmp_line)
        with open('./Los_Angeles_International_Airport_-_Passenger_Traffic_By_Terminal1.csv', 'w') as my_file_2:
            cw = csv.writer(my_file_2)
            cw.writerows(tmp_result)
        with open('arrival_departure.csv', 'w') as my_file_3:
            cw = csv.writer(my_file_3)
            tmp_result1 = []
            tmp_result1 = get_passenger_count_arr(tmp_result, 3)
            cw.writerows(tmp_result1)
        with open('Domestic_International.csv', 'w') as my_file_4:
            cw = csv.writer(my_file_4)
            tmp_result1 = []
            tmp_result1 = get_passenger_count_arr(tmp_result, 4)
            cw.writerows(tmp_result1)

def read_data():
    data = pd.read_csv('./Los_Angeles_International_Airport_-_Passenger_Traffic_By_Terminal1.csv')
    return data

def read_data_subitem(subject):
    if subject == 'Arrival_Departure':
        return pd.read_csv('arrival_departure.csv')
    elif subject == 'Domestic_International':
        return pd.read_csv('Domestic_International.csv')
    else:
        return pd.read_csv('./Los_Angeles_International_Airport_-_Passenger_Traffic_By_Terminal1.csv')

def get_date(data):
    return data['ReportPeriod']

def get_terminals(data):
    result = []
    for terminal in data[data.columns[2]]:
        result.append(str(terminal))
    return result

def get_count(data):
    result = []
    for count in data[data.columns[5]]:
        result.append(str(count))
    return result

def get_indicators(data):
    return data['Indicator Name'].Unique()

def get_arrival_departure(data):
    return data[data['Arrival_Departure'] == 'Arrival'], data[data['Arrival_Departure'] == 'Departure']

def get_domestic_international(data):
    return data[data['Domestic_International'] == 'Domestic'], data[data['Domestic_International'] == 'International']


preprocess()
data = read_data()
terminals = get_terminals(data)
counts = get_count(data)
dates = get_date(data)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash('Hello world!', external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'value': 'Terminal 1', 'label': 'Terminal 1'},
            {'value': 'Terminal 2', 'label': 'Terminal 2'},
            {'value': 'Terminal 3', 'label': 'Terminal 3'},
            {'value': 'Terminal 4', 'label': 'Terminal 4'},
            {'value': 'Terminal 5', 'label': 'Terminal 5'},
            {'value': 'Terminal 6', 'label': 'Terminal 6'},
            {'value': 'Terminal 7', 'label': 'Terminal 7'},
            {'value': 'Terminal 8', 'label': 'Terminal 8'},
            {'value': 'Tom Bradley International Terminal', 'label': 'Tom Bradley International Terminal'},
            {'value': 'Misc. Terminal', 'label': 'Misc. Terminal'},
            {'value': 'Imperial Terminal', 'label': 'Imperial Terminal'},
            {'value': '12', 'label': 'All'}
        ],
    ),
    dcc.Graph(id='my-graph'),
    dcc.Dropdown(
        id = 'my-dropdown-2',
        options = [
            {'value': 'Arrival_Departure', 'label': 'Arrival_Departure'},
            {'value': 'Domestic_International', 'label': 'Domestic_International'},
            {'value': 'Domestic_International_Arrival_Departure', 'label': 'Domestic_International_Arrival_Departure'},
        ]
    ),
    dcc.Graph(id='my-graph-2')
], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'})

@app.callback(
    Output('my-graph', 'figure'),
    [Input('my-dropdown', 'value')
    ])
def update_graph(selected_dropdown_value):
    dff = read_data()
    dff_dates = get_date(dff)
    dff_dates = pd.to_datetime(dff_dates).astype('datetime64[ns]')
    print(dff_dates)
    # print(dff[dff['Terminal'] == selected_dropdown_value]['Passenger_Count'])
    return {
        'data': [ dict(
            # x = str(dff_dates[dff['Terminal'] == selected_dropdown_value]),
            x = dff_dates,
            y = dff[dff['Terminal'] == selected_dropdown_value]['Passenger_Count'],
            text = dff[dff['Terminal'] == selected_dropdown_value]['Arrival_Departure'],
            mode = 'markers',
            marker={
                'size': 7,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis = {
                'title': 'Year',
                
            },
            yaxis = {
                'title': 'Count',
                'type': 'linear'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height = 450,
            hovermode='closest'
        )
    }

@app.callback(
    Output('my-graph-2', 'figure'),
    [Input('my-dropdown-2', 'value')]
)
def update_graph(selected_dropdown_value):
    dff = read_data_subitem(selected_dropdown_value)
    arrivals, departures = get_arrival_departure(dff)
    arrivals_date = get_date(arrivals)
    arrivals_date = pd.to_datetime(arrivals_date).astype('datetime64[ns]')
    departures_date = get_date(departures)
    departures_date = pd.to_datetime(departures_date).astype('datetime64[ns]')
    domestic, international = get_domestic_international(dff)
    domestic_date = get_date(domestic)
    domestic_date = pd.to_datetime(domestic_date).astype('datetime64[ns]')
    international_date = get_date(international)
    international_date = pd.to_datetime(international_date).astype('datetime64[ns]')

    domestic_arrival, international_arrival = get_domestic_international(arrivals)
    domestic_departure, international_departure = get_domestic_international(departures)
    domestic_arrival_date = get_date(domestic_arrival)
    domestic_arrival_date = pd.to_datetime(domestic_arrival_date).astype('datetime64[ns]')
    international_arrival_date = get_date(international_arrival)
    international_arrival_date = pd.to_datetime(international_arrival_date).astype('datetime64[ns]')
    domestic_departure_date = get_date(domestic_departure)
    domestic_departure_date = pd.to_datetime(domestic_departure_date).astype('datetime64[ns]')
    international_departure_date = get_date(international_departure)
    international_departure_date = pd.to_datetime(international_departure_date).astype('datetime64[ns]')

    if selected_dropdown_value == 'Arrival_Departure':
        # arrivals, departures = get_arrival_departure(dff)
        # arrivals_date = get_date(arrivals)
        # arrivals_date = pd.to_datetime(arrivals_date).astype('datetime64[ns]')
        # departures_date = get_date(departures)
        # departures_date = pd.to_datetime(departures_date).astype('datetime64[ns]')
        # print(arrivals['Passenger_Count'])
        return {
            'data': [
                dict (
                    fill= "tonexty", 
                    line= {
                        "color": "#f21602", 
                        "shape": "spline", 
                        "width": 0
                    }, 
                    name =  "arrival", 
                    type =  "scatter", 
                    x =  arrivals_date, 
                    y =  arrivals['Passenger_Count'],
                    fillcolor =  "#f21602"
                ),
                dict (
                    fill = "tonexty", 
                    line = {
                        "color": "#f2c382", 
                        "shape": "spline", 
                        "width": 0
                    }, 
                    name = "departure", 
                    type = "scatter", 
                    x = departures_date, 
                    y = departures['Passenger_Count'],
                    fillcolor = "#f2c382"
                ),
            ],
            'layout': 
            dict(
                xaxis = {
                "ticks": "outside", 
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
                yaxis = {
                    "ticks": "outside", 
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
                    "showticklabels": True
                },
                margin={'l': 60, 'b': 60, 't': 80, 'r': 60},
                height = 460,
                autosize = False, 
                hovermode = "x", 
                showlegend = False, 
                annotations = [
                {
                    "x": 0, 
                    "y": -0.13, 
                    "font": {"size": 12}, 
                    "text": "Brier Score data", 
                    "xref": "paper", 
                    "yref": "paper", 
                    "xanchor": "left", 
                    "yanchor": "bottom", 
                    "showarrow": False
                }
                ]
            )
    }
    elif selected_dropdown_value == 'Domestic_International':
        return {
            'data': [
                dict (
                    fill = "tonexty", 
                    line = {
                        "color": "#f7960e", 
                        "shape": "spline", 
                        "width": 0
                    }, 
                    name = "international", 
                    type = "scatter", 
                    x = international_date, 
                    y = international['Passenger_Count'],
                    fillcolor = "#f7960e"
                ),
                dict (
                    fill= "tonexty", 
                    line= {
                        "color": "#b7e4f7", 
                        "shape": "spline", 
                        "width": 0
                    }, 
                    name =  "domestic", 
                    type =  "scatter", 
                    x =  domestic_date, 
                    y =  domestic['Passenger_Count'],
                    fillcolor =  "#b7e4f7"
                ),
                
            ],
            'layout': dict(
                xaxis = {
                "ticks": "outside", 
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
                yaxis = {
                    "ticks": "outside", 
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
                    "showticklabels": True
                },
                margin={'l': 60, 'b': 60, 't': 80, 'r': 60},
                height = 460,
                autosize = False, 
                hovermode = "x", 
                showlegend = False, 
                annotations = [
                    {
                    "x": 0, 
                    "y": -0.13, 
                    "font": {"size": 12}, 
                    "xref": "paper", 
                    "yref": "paper", 
                    "xanchor": "left", 
                    "yanchor": "bottom", 
                    "showarrow": False
                    }
                ]
            )
        }
    elif selected_dropdown_value == 'Domestic_International_Arrival_Departure':
        return {
            'data': [
                dict (
                    fill = "tonexty", 
                    line = {
                        "color": "#f2c382", 
                        "shape": "spline", 
                        "width": 0
                    }, 
                    text = "international_arrival", 
                    type = "scatter", 
                    x = international_arrival_date, 
                    y = international_arrival['Passenger_Count'],
                    fillcolor = "#f2c382"
                ),
                dict (
                    fill = "tonexty", 
                    line = {
                        "color": "#25b8f7", 
                        "shape": "spline", 
                        "width": 0
                    }, 
                    text = "international_departure", 
                    type = "scatter", 
                    x = international_departure_date, 
                    y = international_departure['Passenger_Count'],
                    fillcolor = "#25b8f7"
                ),
                dict (
                    fill= "tonexty", 
                    line= {
                        "color": "#f21602", 
                        "shape": "spline", 
                        "width": 0
                    }, 
                    text =  "domestic_arrival", 
                    type =  "scatter", 
                    x =  domestic_arrival_date, 
                    y =  domestic_arrival['Passenger_Count'],
                    fillcolor =  "#f21602"
                ),
                dict (
                    fill = "tonexty", 
                    line = {
                        "color": "#b7e4f7", 
                        "shape": "spline", 
                        "width": 0
                    }, 
                    text = "domestic_departure", 
                    type = "scatter", 
                    x = domestic_departure_date, 
                    y = domestic_departure['Passenger_Count'],
                    fillcolor = "#b7e4f7"
                ),
            ],
            'layout': 
            dict(
                xaxis = {
                "ticks": "outside", 
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
                yaxis = {
                    "ticks": "outside", 
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
                    "showticklabels": True
                },
                margin={'l': 60, 'b': 60, 't': 80, 'r': 60},
                height = 460,
                autosize = False, 
                hovermode = "x", 
                showlegend = False, 
                annotations = [
                {
                    "x": 0, 
                    "y": -0.13, 
                    "font": {"size": 12}, 
                    "text": "Brier Score data", 
                    "xref": "paper", 
                    "yref": "paper", 
                    "xanchor": "left", 
                    "yanchor": "bottom", 
                    "showarrow": False
                }
                ]
            )
        }
    return {
        'data': [
            # dict (
            #     fill= "tonexty", 
            #     line= {
            #         "color": "#f21602", 
            #         "shape": "spline", 
            #         "width": 0
            #     }, 
            #     name =  "", 
            #     type =  "scatter", 
            #     x =  arrivals_date, 
            #     y =  arrivals['Passenger_Count'],
            #     fillcolor =  "#f21602"
            # ),
            # dict (
            #     fill = "tonexty", 
            #     line = {
            #         "color": "#f2c382", 
            #         "shape": "spline", 
            #         "width": 0
            #     }, 
            #     name = "", 
            #     type = "scatter", 
            #     x = departures_date, 
            #     y = departures['Passenger_Count'],
            #     fillcolor = "#f2c382"
            # ),
        ],
        'layout': dict(
            # xaxis = {
            #     "ticks": "outside", 
            #     "mirror": True, 
            #     "ticklen": 5, 
            #     "showgrid": False, 
            #     "showline": True, 
            #     "tickfont": {
            #       "size": 11, 
            #       "color": "rgb(107, 107, 107)"
            #     }, 
            #     "tickwidth": 1, 
            #     "showticklabels": True                
            # },
            # yaxis = {
            #     "ticks": "outside", 
            #     "title": "", 
            #     "mirror": True, 
            #     "ticklen": 5, 
            #     "showgrid": False, 
            #     "showline": True, 
            #     "tickfont": {
            #         "size": 11, 
            #         "color": "rgb(107, 107, 107)"
            #     }, 
            #     "zeroline": True, 
            #     "tickwidth": 1, 
            #     "showticklabels": True
            # },
            # margin={'l': 60, 'b': 60, 't': 80, 'r': 60},
            # height = 460,
            # autosize = False, 
            # hovermode = "x", 
            # showlegend = False, 
            # annotations = [
            #     {
            #     "x": 0, 
            #     "y": -0.13, 
            #     "font": {"size": 12}, 
            #     "text": "Brier Score data", 
            #     "xref": "paper", 
            #     "yref": "paper", 
            #     "xanchor": "left", 
            #     "yanchor": "bottom", 
            #     "showarrow": False
            #     }
            # ]
        )
    }



if __name__ == '__main__':
    app.run_server(debug=True)