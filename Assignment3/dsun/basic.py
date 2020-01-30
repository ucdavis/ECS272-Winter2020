# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import urllib.request as req
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

### Data processing ###
dataset = req.urlopen('http://stream.cs.ucdavis.edu/datasets/LAX_Terminal_Passengers.csv')
data = pd.read_csv(dataset).to_numpy()

terminals = ["Imperial Terminal", "Misc. Terminal", "Terminal 1", "Terminal 2", "Terminal 3",
             "Terminal 4", "Terminal 5", "Terminal 6", "Terminal 7", "Terminal 8",
             "Tom Bradley International Terminal"]
terminalData = []
months = list()
years = list()

for i in range(len(terminals)):
    categories = {"dep-dom": dict(), "arr-dom": dict(), "dep-int": dict(), "arr-int": dict()}
    terminalData.append(categories)

for i in range(5870):
    time = data[i][1][0:10]
    year = time[6:]
    if not(time in months):
        months.append(time)
    if not(year in years):
        years.append(year)
    tmn = data[i][2]
    cat1 = data[i][3]
    cat2 = data[i][4]
    num = data[i][5]
    index = terminals.index(tmn)
    if cat1 == "Departure" and cat2 == "Domestic":
        terminalData[index]["dep-dom"][time] = num
    elif cat1 == "Arrival" and cat2 == "Domestic":
        terminalData[index]["arr-dom"][time] = num
    elif cat1 == "Departure" and cat2 == "International":
        terminalData[index]["dep-int"][time] = num
    elif cat1 == "Arrival" and cat2 == "International":
        terminalData[index]["arr-int"][time] = num

processedData = []
for i in range(len(terminals)):
    tmn = terminals[i]
    tData = terminalData[i]
    if "dep-dom" in tData.keys():
        depdom = tData["dep-dom"]
        for m in months:
            if m in depdom.keys():
                processedData.append([tmn, "Departure", "Domestic", m[:2], m[6:], depdom[m]])
            else:
                processedData.append([tmn, "Departure", "Domestic", m[:2], m[6:], 0])
    else:
        for m in months:
            processedData.append([tmn, "Departure", "Domestic", m[:2], m[6:], 0])

    if "arr-dom" in tData.keys():
        arrdom = tData["arr-dom"]
        for m in months:
            if m in arrdom.keys():
                processedData.append([tmn, "Arrival", "Domestic", m[:2], m[6:], arrdom[m]])
            else:
                processedData.append([tmn, "Arrival", "Domestic", m[:2], m[6:], 0])
    else:
        for m in months:
            processedData.append([tmn, "Arrival", "Domestic", m[:2], m[6:], 0])

    if "dep-int" in tData.keys():
        depint = tData["dep-int"]
        for m in months:
            if m in depint.keys():
                processedData.append([tmn, "Departure", "International", m[:2], m[6:], depint[m]])
            else:
                processedData.append([tmn, "Departure", "International", m[:2], m[6:], 0])
    else:
        for m in months:
            processedData.append([tmn, "Departure", "International", m[:2], m[6:], 0])

    if "arr-int" in tData.keys():
        arrint = tData["arr-int"]
        for m in months:
            if m in arrint.keys():
                processedData.append([tmn, "Arrival", "International", m[:2], m[6:], arrint[m]])
            else:
                processedData.append([tmn, "Arrival", "International", m[:2], m[6:], 0])
    else:
        for m in months:
            processedData.append([tmn, "Arrival", "International", m[:2], m[6:], 0])

indicators1 = ['Departure', 'Arrival']
indicators2 = ['Domestic', 'International']
columns = ['Terminal', 'Indicator1', 'Indicator2', 'Month', 'Year', 'Count']
df = pd.DataFrame(data=processedData, columns=columns)
#print(df[:5])

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='terminals',
                options=[{'label': i, 'value': i} for i in (terminals)],
                value='Terminal 1'
            )
        ],
        style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='category1',
                options=[{'label': i, 'value': i} for i in indicators1],
                value='Departure'
            ),
        ],style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='category2',
                options=[{'label': i, 'value': i} for i in indicators2],
                value='Domestic'
            ),
        ],style={'width': '30%', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=int(years[0]),
        max=int(years[-1]),
        value=int(years[0]),
        marks={year : year for year in years},
        step=None
    )
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('terminals', 'value'),
     Input('category1', 'value'),
     Input('category2', 'value'),
     Input('year--slider', 'value')])
def update_graph(term, indicator_1,
                 indicator_2, year_value):

    dff = df[(df['Year'] == str(year_value)) & (df['Terminal'] == term) & (df['Indicator1'] == indicator_1) & (df['Indicator2'] == indicator_2)]
    return {
        'data': [dict(
            x=dff['Month'],
            y=dff['Count'],
            text=dff['Count'],
            #mode='markers',
            marker={
                'line': {'color': 'rgb(55, 83, 109)'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': 'Month',
                'type': 'linear'
            },
            yaxis={
                'title': 'Passenger Count',
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=False)
