# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import urllib.request as req
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

dataset = req.urlopen('http://stream.cs.ucdavis.edu/datasets/LAX_Terminal_Passengers.csv')
data = pd.read_csv(dataset).to_numpy()

indicators2 = ['Departure', 'Arrival'] # index 37 38
indicators1 = ['Domestic', 'International'] # index 39 40
terminals = ["Imperial Terminal", "Misc. Terminal", "Terminal 1", "Terminal 2", "Terminal 3",
             "Terminal 4", "Terminal 5", "Terminal 6", "Terminal 7", "Terminal 8",
             "Tom Bradley International Terminal"] # index 26 - 36
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'] # index 14 - 25
years = list() # index 0 - 13
for i in range(2006, 2020):
    years.append(str(i))

yearData = dict()
for i in range(len(years)):
    monthData = dict()
    for j in range(len(months)):
        termData = dict()
        for k in range(len(terminals)):
            ind1Data = dict()
            for l in range(len(indicators1)):
                ind2Data = dict()
                for m in range(len(indicators2)):
                    ind2Data[indicators2[m]] = 0
                ind1Data[indicators1[l]] = ind2Data
            termData[terminals[k]] = ind1Data
        monthData[months[j]] = termData
    yearData[years[i]] = monthData

for i in range(5870):
    time = data[i][1][0:10]
    year = time[6:]
    month = time[:2]
    tmn = data[i][2]
    cat1 = data[i][3]
    cat2 = data[i][4]
    num = data[i][5]
    yearData[year][month][tmn][cat2][cat1] = num

label = years + months + terminals + indicators1 + indicators2
color = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080'] # index%11
source = list()
target = list()
value = list()

### process data
#yearCount = list()
def getData(y0, y1, m0, m1, t):
    global source, target, value
    source = []
    target = []
    value = []
    for i in range(y0, y1+1):
        monthCount = list()
        for j in range(m0, m1+1):
            termCount = list()
            for term in terminals:
                if t != -1 and terminals.index(term) != t:
                    continue
                else:
                    cat1Count = list()
                    for cat1 in indicators1:
                        cat2Count = list()
                        for cat2 in indicators2:
                            n0 = yearData[years[i]][months[j]][term][cat1][cat2]
                            cat2Count.append(n0)
                            source.append(label.index(cat1))
                            target.append(label.index(cat2))
                            value.append(n0)
                        n1 = sum(cat2Count)
                        cat1Count.append(n1)
                        source.append(label.index(term))
                        target.append(label.index(cat1))
                        value.append(n1)
                    n2 = sum(cat1Count)
                    termCount.append(n2)
                    source.append(label.index(months[j]))
                    target.append(label.index(term))
                    value.append(n2)
            n3 = sum(termCount)
            monthCount.append(n3)
            source.append(label.index(years[i]))
            target.append(label.index(months[j]))
            value.append(n3)

getData(0, 13, 0, 11, -1)
app.layout = html.Div([
    html.Div([
            html.Div([
                'From Year ',
                dcc.Dropdown(
                    id='fromYear',
                    options=[{'label': i, 'value': i} for i in years],
                    value='2006'
                )
            ],
            style={'width': '20%', 'display': 'inline-block'}),

            html.Div([
                'to Year ',
                dcc.Dropdown(
                    id='toYear',
                    options=[{'label': i, 'value': i} for i in years],
                    value='2019'
                ),
            ],style={'width': '20%', 'display': 'inline-block'}),

            html.Div([
                'From Month ',
                dcc.Dropdown(
                    id='fromMonth',
                    options=[{'label': i, 'value': i} for i in months],
                    value='01'
                ),
            ],style={'width': '20%', 'display': 'inline-block'}),

            html.Div([
                'to Month ',
                dcc.Dropdown(
                    id='toMonth',
                    options=[{'label': i, 'value': i} for i in months],
                    value='12'
                ),
            ],style={'width': '20%', 'display': 'inline-block'}),

            html.Div([
                'Terminal ',
                dcc.Dropdown(
                    id='Terminal',
                    options=[{'label': i, 'value': i} for i in (terminals+['All'])],
                    value='All'
                ),
            ],style={'width': '20%', 'display': 'inline-block'})
        ]),

    dcc.Graph(id='indicator-graphic',
              figure=go.Figure(
                  data=[go.Sankey(
                    node = dict(
                      pad = 40,
                      thickness = 30,
                      line = dict(color = "gray", width = 0.5),
                      label = label,
                      color = [color[i%11] for i in range(len(label))]
                    ),
                    link = dict(
                      source = source,
                      target = target,
                      value = value,
                      line = dict(color = "gray", width = 0.5)
                  ))],
              ),
              style={'height': 800}
            ),
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('fromYear', 'value'),
     Input('toYear', 'value'),
     Input('fromMonth', 'value'),
     Input('toMonth', 'value'),
     Input('Terminal', 'value')])
def update_graph(year_0, year_1, month_0, month_1, term):
    termIndex = -1
    if term != 'All':
        termIndex = terminals.index(term)
    getData(years.index(year_0), years.index(year_1), months.index(month_0), months.index(month_1), termIndex)
    return {
        'data': [go.Sankey(
                node = dict(
                  pad = 40,
                  thickness = 30,
                  line = dict(color = "gray", width = 0.5),
                  label = label,
                  color = [color[i%11] for i in range(len(label))]
                ),
                link = dict(
                  source = source,
                  target = target,
                  value = value,
                  line = dict(color = "gray", width = 0.5)
              ))]
    }


if __name__ == '__main__':
    app.run_server(debug=False)
