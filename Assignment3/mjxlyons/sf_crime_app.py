#Matthew Lyons
#ECS 272, Kwan Liu-Ma
#Assignment 3

#analyzing San Francisco crime data
#https://www.kaggle.com/roshansharma/sanfranciso-crime-dataset

#dash app adapted from examples from:
#https://dash.plot.ly/getting-started-part-2
#https://plot.ly/python/sankey-diagram/

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import pandas as pd

from sf_crime_data import df, district_df, crime_df, day_crimes, hour_crimes, sankey_labels, sank_source, sank_target, sank_value

#css style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#colors we want to use
colors = {
    'background': '#FFFFFF',
    'text': '#222222'
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#start layout
app.layout = html.Div(
    style = {'textAlign':"center"},
    children = [
    
    #title
    html.H1("Visualizing San Francisco Crime Data"),
    html.H2("Matthew Lyons"),
    html.H2("ECS 272, Winter 2020"),
    
    #crime bar graph (define through callback)
    dcc.Graph(id='crime_time_bar'),
    
    #radio buttons to control bar graph
    html.Div(
        [
        dcc.RadioItems(
            id = "time_x_axis",
            options=[
                {'label': 'Days of Week','value':0},
                {'label': 'Hour','value':1}
            ],
            #default radio choice
            value=0
        ),
        ]
    ),
    
    #sankey graph
    dcc.Graph(
        id='sankey_cat',
        figure = {
            'data':[go.Sankey(
                node = {
                    'label':sankey_labels,
                },
                link = {
                    "source":sank_source, # indices correspond to labels, eg A1, A2, A2, B1, ...
                    "target":sank_target,
                    "value":sank_value
                }
            )],
            'layout': {
                'title': 'Sankey crimes',
                'plot_bgcolor':colors['background'],
                'paper_bgcolor':colors['background'],
                'font': {'color':colors['text'],'size':18}
            }
        
        }
    ),
    
    ]
)

#inputs to update graphs
radio_choice = [day_crimes,hour_crimes]
@app.callback(
    Output('crime_time_bar', 'figure'),
    [Input('time_x_axis', 'value'),
    ]
)
#arguments are in order of input
def update_graphs(time_radio_index):
    
    return{
        'data':[
            {'x':radio_choice[time_radio_index].index.to_list(),
            'y':radio_choice[time_radio_index].to_list(),
            'type':'bar'
            }
        ],
        'layout': {
            'title': 'Time of Crimes',
            'yaxis':{
                'title':"Crime occurrences over year"
            },
            'plot_bgcolor':colors['background'],
            'paper_bgcolor':colors['background'],
            'font': {'color':colors['text'],'size':18}
        }
        
    }
    

if __name__ == '__main__':
    app.run_server(debug=True)
