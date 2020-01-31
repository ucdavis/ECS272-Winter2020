import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

file = pd.read_csv("../datasets/globalterrorismdb_0718dist.csv",encoding = "ISO-8859-1")

Xoptions = ["attacktype1_txt",
                         "city",
                         "targtype1_txt",
                         "targsubtype1_txt",
                         "corp1",
                         "target1",
                         "gname",
                         "weaptype1_txt"]




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Tao Wang Assignment 3'),
    html.H1(children='Global Terrorist Data from 1970 - 2017'),

    html.Div(children='''
    Terrorist Data Analysis in different countries
'''),
        html.Div(
            dcc.Dropdown(
                id = "xaxiscolumn",
                options=[{"label": i,"value": i} for i in file["country_txt"].unique()],
                value="United States"
            ),style={'width': '48%', 'display': 'inline-block'}
        ),
        html.Div(
            dcc.Dropdown(
                id = "yaxiscolumn",
                options=[{"label":i,"value":i} for i in Xoptions],
                value="attacktype1_txt"
            ),style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
    ),
    dcc.Graph(
        id="simple"),
    dcc.Slider(
        id = "year-slider",
        min = 1970,
        max = 2017,
        value = 1970,
        marks={str(year) : str(year)for year in range(1970,2018)},
    ),
    html.Br(),
    html.Div(
            dcc.Dropdown(
                id = "xaxis-region",
                options=[{"label": i,"value": i} for i in file["region_txt"].unique()],
                value="North America"
            )
        ),
    dcc.Graph(
        id="Sankey"
    )



])

@app.callback(
    Output("simple","figure"),
    [Input("xaxiscolumn","value"),
     Input("yaxiscolumn","value"),
     Input("year-slider","value")]
)
def update_simple(xaxis_column,yaxis_column,year_value):
    dff = file[file["iyear"] == year_value]

    fig = px.histogram(dff, x=dff[dff["country_txt"] == xaxis_column][yaxis_column])
    return fig


def collectData(all_data,dff,country):

    result = {"source":[],"target":[],"value":[]}
    countrylast = len(country)
    attacklast = len(all_data) - 2
    for i in range(countrylast):
        for j in range(countrylast,attacklast):
            countryfilter = dff[dff.country_txt == country[i]]
            attackfilter = countryfilter[countryfilter.attacktype1_txt == all_data[j]]
            if len(attackfilter) != 0:
                result["source"].append(i)
                result["target"].append(j)
                result["value"].append(len(attackfilter))
    for i in range(countrylast,attacklast):
        attackfilter = dff[dff.attacktype1_txt == all_data[i]]
        count_attacks = len(attackfilter)
        suicidefilter = attackfilter[attackfilter.suicide == 1]
        count_suicide = len(suicidefilter)
        if len(suicidefilter) != 0:
            result["source"].append(i)
            result["target"].append(len(all_data) - 2)
            result["value"].append(count_suicide)
        result["source"].append(i)
        result["target"].append(len(all_data) - 1)
        result["value"].append(count_attacks - count_suicide)

    return result



def pickcolor(all_data,country):
    result = len(all_data) * [""]
    color = ["red","blue","green","yellow","pink"]
    countrylast = len(country)
    attacklast = len(all_data) - 2
    for i in range(countrylast):
        result[i] = color[i % len(color)]
    for i in range(countrylast,attacklast):
        result[i] = color[::-1][(i - countrylast )% len(color)]
    result[-1] = "green"
    result[-2] = "yellow"

    return result







@app.callback(
    Output('Sankey','figure'),
    [Input('year-slider','value'),
     Input('xaxis-region','value')])
def update_map(time,region):
    dff = file[file["iyear"] == time]
    dff = dff[dff["region_txt"] == region]
    country = [i for i in dff.country_txt.unique()]
    attack = [i for i in dff.attacktype1_txt.unique()]
    all_data = country + attack + ["Suicide", "Not Suicide"]

    fig = go.Figure(data = [go.Sankey(
        node = dict(

            pad = 15,
            thickness = 15,
            line = dict(color = "black", width = 0.5),
            label = all_data,
            color = pickcolor(all_data,country)
        ),
        link = collectData(all_data,dff,country)



    )])
    fig.update_layout(hovermode = "x",

                      title = "Global Terrorism Database<br>Analysis of Weapons and Suicidal in different continents"

                      )
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
