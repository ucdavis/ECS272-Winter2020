import dash
import random
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
df = pd.read_csv(
    'Police_Department_Incidents_-_Previous_Year__2016_.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H3("Crime data of San Francisco by histogram")],
        style={'text-align': 'center', 'color': 'blue'}
    ),
    dcc.Dropdown(
        id='xaxis-column',
        options=[
            {'label': 'Category', 'value': 'Category'},
            {'label': 'PdDistrict', 'value': 'PdDistrict'},
            {'label': 'Resolution', 'value': 'Resolution'}
        ],
        value='Category',
        placeholder="Select by your choice",
    ),
    html.Br(),
    html.Div([dcc.Graph(id='histogram-with-slider')]),
    dcc.Slider(
        id='DayOfWeek-slider',
        min=1,
        max=7,
        value=1,
        marks={1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
               4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'},
        step=None
    ),
    html.Div([
        html.Div([
            html.H3("Category/Resoultion by DayOfWeek and Region")],
            style={'text-align': 'center',
                   'color': 'blue', 'margin-top': '75px'}),
        html.Div(dcc.Dropdown(
            id='xaxis-column1',
            options=[
                {'label': 'Category', 'value': 'Category'},
                {'label': 'Resolution', 'value': 'Resolution'}
            ],
            value='Resolution',
            placeholder="Select by your choice",
        )),
        html.Div(html.Div(dcc.Graph(id='Sankey-with-dropdown')))
    ])
])

@app.callback(
    Output('histogram-with-slider', 'figure'),
    [Input('xaxis-column', 'value'),
    Input('DayOfWeek-slider', 'value')
    ])
def update_figure(xaxis_column_name, selected_DayOfWeek):
    mapp = {1: 'Monday', 2: 'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday',7:'Sunday'}
    filtered_df = df[df.DayOfWeek == mapp[selected_DayOfWeek]]
    #crime_category = filtered_df['Descript']
    fig = px.histogram(
        filtered_df, x=filtered_df[xaxis_column_name], title=xaxis_column_name+' by DayOfWeek')
    fig.update_layout(
        title={
            'y': 1,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        margin={
            'b': 200, 'r': 20, 'l': 30, 't': 20
            },
        xaxis={
            'title': 'Description'
        },
        yaxis_title_text='Count', 
        bargap=0.2,  
        bargroupgap=0.1  
    )
    return fig

@app.callback(
    Output('Sankey-with-dropdown', 'figure'),
    [Input('xaxis-column1', 'value')])

def update_Sankey(xaxis_column1_name):
    dff = df[xaxis_column1_name]
    week = [i for i in df.DayOfWeek.unique()]
    region = [i for i in df.PdDistrict.unique()]
    other_type = [i for i in df[xaxis_column1_name].unique()]
    size = week + region + other_type
    fig = go.Figure(data = [go.Sankey(
        node = dict(
            pad = 15,
            thickness = 15,
            line = dict(color = 'blue',width = 0.8),
            label = size,
            color=['rgb(50, 168, 160)', 'yellow', 'green',
                   'purple', 'white', 'orange', 'rgb(131, 207, 56)', 'rgb(43, 196, 156)', 'rgb(28, 92, 156)', 'rgb(11, 120, 230)', 'rgb(232, 39, 120)', 'rgb(186, 103, 48)', 'rgb(23, 156, 76)', 'rgb(55, 21, 176)', 'rgb(100, 156, 123)', 'rgb(31, 66, 110)', 'rgb(186, 150, 48)', 'rgb(131, 207, 56)', 'rgb(232, 39, 120)']
        ),
        link=getData(size, dff, week, xaxis_column1_name)
    )])
    return fig


def getData(size, dff, week, xaxis_column1_name):
    result = {"source": [], "target": [], "value": [],"color":[]}
    region = [i for i in df.PdDistrict.unique()]
    DOWLast = len(week)
    PdDistrictlast = len(week) + len(region)
    OTlast = len(size)
    for i in range(DOWLast):
        for j in range(DOWLast, PdDistrictlast):
            DOWfilter = df[df.DayOfWeek == week[i]]
            Distfilter = DOWfilter[DOWfilter.PdDistrict == size[j]]
            if len(Distfilter) != 0:
                result["source"].append(i)
                result["target"].append(j)
                result["value"].append(len(Distfilter))
                result["color"].append(
                    'rgba'+str((0, random.randint(200, 255), random.randint(100, 255), 0.5)))
    for k in range(DOWLast, PdDistrictlast):
        for l in range(PdDistrictlast, OTlast):
            Distfilter = DOWfilter[DOWfilter.PdDistrict == size[k]]
            OTfilter = Distfilter[Distfilter[xaxis_column1_name] == size[l]]
            if len(OTfilter) != 0:
                result["source"].append(k)
                result["target"].append(l)
                result["value"].append(len(OTfilter))
                result["color"].append(
                    'rgba'+str((50, random.randint(200, 255), random.randint(100, 255), 0.5)))
    return result

if __name__ == '__main__':
    app.run_server(debug=True)




