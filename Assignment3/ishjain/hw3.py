# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('terrorisndata.csv', encoding='latin-1')

years = df['iyear'].unique().tolist()

regions = df['region_txt'].unique().tolist()
regions_no = df['region'].unique().tolist()

attack_type = df['attacktype1_txt'].unique().tolist()
attack_type_no = df['attacktype1'].unique().tolist()

weaptype = df['weaptype1_txt'].unique().tolist()
weaptype_no = df['weaptype1'].unique().tolist()

country = df['country_txt'].unique().tolist()
country_no = df['country'].unique().tolist()

colors = {
    'background': '#0000',
    'text': '#111111'
}

app.layout = html.Div(children=[
    html.H1(children = "Visualization on Global Terrorism"),
    html.H3(children= "Data Visualization Assignment 3"),
    html.H3(children= "By Ishan Jain"),
    html.H3(children= "Visualization 1: Basic visualization : Bar graph"),
    html.Div([
        html.Label('Select year'),
        dcc.Slider(
            id='slider',
            min=int(df['iyear'].min()),
            max=int(df['iyear'].max()),
            value=int(df['iyear'].min()),
            marks={str(year): str(year) for year in df['iyear'].unique() if int(year)%5 == 0},
            step=None
        ),
        html.Label('Select a region'),
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': i, 'value': i} for i in regions
            ],
            value='North America',
        ),
    ],
        style={
            "width": '80%',
            'paddingLeft': 200,
            'paddingRight': 50,            
        }
    ),

    html.Div(
        id = 'output-graph'
    ),

    html.H3(children= "Visualization 2: Advanced visualization : Parallel Coordinates Graph"),
    html.Div([
        html.Label('Select begin year'),
        dcc.Dropdown(
            id='dropdown1',
            options=[
                {'label': i, 'value': i} for i in years
            ],
            value='1975',
        ),
        html.Label('Select end year (Larger than begin year)'),
        dcc.Dropdown(
            id='dropdown2',
            options=[
                {'label': i, 'value': i} for i in years
            ],
            value='1980',
        ),
        html.Label('Select countries'),
        dcc.Dropdown(
            id='dropdown3',
            options=[
                {'label': i, 'value': i} for i in country
            ],
            value=['United States', 'Greece', 'Philippines'],
            multi=True
        ),
    ],
        style={
            "width": '80%',
            'display': 'inline-block',
            'paddingLeft': 200,
            'paddingRight': 50,
            'boxSizing': 'border-box',
            
        }
    ),

    html.Div([
        dcc.Graph(
            id = 'cord-graph'
        )
    ]),

])


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='slider', component_property='value'),
    Input(component_id='dropdown', component_property='value')]
)
def update_graph(selected_year, selected_region):
    # print(selected_year)
    filtered_df = df.loc[df['iyear'] == selected_year]
    #print(filtered_df)
    df_by_continent = filtered_df[filtered_df['region_txt'] == selected_region]
    key_value = df_by_continent.attacktype1_txt.value_counts()
    x = []
    y = []
    for i,v in key_value.items():
        x.append(i)
        y.append(v)
    return dcc.Graph(
        id = 'example-graph',
        figure = {
            'data': [
                {'x' : x, 'y' : y, 'type' : 'bar', 'name' : 'Attack types',
                'marker':{
                    'color' : '#483D8B'
                    }
                }
            ],
            'layout' : {
                'title' : 'Terrorism Data: Attack Type',
                'hovermode' :'closest',
                'paper_bgcolor': colors['background'],
                'plot_bgcolor' : colors['background'],
                'height': 400,
                'font': {
                    'color': colors['text']
                }

            },
        }
    )


@app.callback(
    Output(component_id='cord-graph', component_property='figure'),
    [Input(component_id='dropdown1', component_property='value'),
    Input(component_id='dropdown2', component_property='value'),
    Input(component_id='dropdown3', component_property='value')]
)
def updateParCord(begin_year, end_year, selected_region):
    
    selected_year = []
    
    if not isinstance(selected_region, list):
        selected_region = [selected_region]
    for i in range(int(begin_year), int(end_year)+1):
        selected_year.append(int(i))
    
    filtered_df = df.loc[df['iyear'].isin(selected_year)]
    df_by_continent = filtered_df[df['country_txt'].isin(selected_region)]
    # print(selected_region)
    country_val =[]
    for i in range(len(selected_region)):
        for j in range(len(country)):
            if selected_region[i] == country[j]:
                country_val.append(country_no[j])
    # print(country_val)
    figure = go.Figure(data=
    go.Parcoords(
        line = dict(color = df_by_continent['country'],
                   colorscale = 'thermal',
                   ),
        dimensions=list([

            {
                'label': 'Weapon Type',
                'range': [0, len(weaptype_no)+1],
                'tickvals': weaptype_no,
                'ticktext': weaptype,
                'values': df_by_continent['weaptype1'].tolist()
            },
            {
                'label': 'Country',
                'range': [min(country_val), max(country_val)+1],
                'tickvals': country_val,
                'ticktext': selected_region,
                'values': df_by_continent['country'].tolist()
            },
            
            {
                'label': 'Attack Type',
                'range': [0, len(attack_type_no)],
                'tickvals': attack_type_no,
                'ticktext': attack_type,
                'values': df_by_continent['attacktype1'].tolist()
            },
            {
                'label': 'Success',
                'range': [0, 1],
                'tickvals': [0,1],
                'ticktext': ['No Success', 'Success'],
                'values': df_by_continent['success'].tolist()
            },

        ])
    ))

    figure.update_layout(
        title='Parallel Plot for terrorism data',
        plot_bgcolor='#FFFFE0',
        paper_bgcolor='#FFFFE0',
        height=450
    )
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
