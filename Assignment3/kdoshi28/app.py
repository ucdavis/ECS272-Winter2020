import os
from random import randint

import dash
import flask

import plotly.graph_objects as go

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

### GLOBALS, DATA & INTIALISE THE APP ###



# This dict allows me to sort the weekdays in the right order
DAYSORT = dict(zip(['Friday', 'Monday', 'Saturday','Sunday', 'Thursday', 'Tuesday', 'Wednesday'],
                  [4, 0, 5, 6, 3, 1, 2]))

# Set the global font family
FONT_FAMILY =  "Arial" 
# Read in data from csv
csvLoc = 'Dataset/Police_Department_Incidents_-_Previous_Year__2016_.csv'
acc = pd.read_csv(csvLoc)
# Set up the Dash instance. Big thanks to @jimmybow for the boilerplate code


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Include the external CSS
cssURL = "https://rawgit.com/richard-muir/uk-car-accidents/master/road-safety.css"
app.css.append_css({
    "external_url": cssURL
})


## SETTING UP THE APP LAYOUT ##

# Main layout container

app.layout = html.Div(
    [
    html.H1(
        'Police Reports',
        style={
            'paddingLeft' : 50,
            'fontFamily' : FONT_FAMILY
            }
        ),
    
    html.Div([   # Holds the widgets & Descriptions
        
        html.Div([  

            html.H3(
                'In 2016, the San Fran suffered  many crimes.',
                style={
                    'fontFamily' : FONT_FAMILY
                }
                ),
            html.Div(
                'You can explore when and where the crimes happened using these filters.',
                ),
            
            html.Div(
                'Select the day of the crime:',
                style={
                    'paddingTop' : 20,
                    'paddingBottom' : 10
                }
            ),

            dcc.Checklist( # Checklist for the dats of week, sorted using the sorting dict created earlier
                options=[
                    {'label': day[:3], 'value': day} for day in sorted(acc['DayOfWeek'].unique(), key=lambda k: DAYSORT[k])
                ],
                value = [day for day in acc['DayOfWeek'].unique()],
                labelStyle={  # Different padding for the checklist elements
                    'display': 'inline-block',
                    'paddingRight' : 10,
                    'paddingLeft' : 10,
                    'paddingBottom' : 5,
                    },
                id="dayChecklist",
            )
                

        ],
        style={
            "width" : '60%', 
            'display' : 'inline-block', 
            'paddingLeft' : 50, 
            'paddingRight' : 10,
            'boxSizing' : 'border-box',
            }
        
        ),
        html.Div(
        style={
            "width" : '40%', 
            'float' : 'right', 
            'display' : 'inline-block', 
            'paddingRight' : 50, 
            'paddingLeft' : 10,
            'boxSizing' : 'border-box',
            'fontFamily' : FONT_FAMILY
            })

    ],
    style={'paddingBottom' : 20}),

    html.Div([  
        
        html.Div([  # Holds the barchart
            dcc.Graph(
                id="bar",
            )
            
        ],
        style={
            "width" : '100%', 
            'display' : 'inline-block', 
            'paddingRight' : 50, 
            'paddingLeft' : 5,
            'boxSizing' : 'border-box'
            })

    ]),

    html.Div([  
        
        html.Div([  # Holds the parallel set
            dcc.Graph(
                id="Parallel set",
            )
        ],
        style={
            "width" : '100%', 
            'display' : 'inline-block',
            'paddingTop':100, 
            'paddingRight' : 50, 
            'paddingLeft' : 5,
            'boxSizing' : 'border-box',
            'float' : 'right',
            'fontFamily' : FONT_FAMILY
            
            })

    ]),
])


## APP INTERACTIVITY THROUGH CALLBACK FUNCTIONS TO UPDATE THE CHARTS ##

# Callback function passes the current value of all three filters into the update functions.
# This on updates the bar.

@app.callback(
    Output(component_id='bar', component_property='figure'),
    [Input(component_id='dayChecklist', component_property='value'),
    ]
)


def updateBarChart(weekdays):

    filtered_df = acc[[
        'Category']][
            (acc['DayOfWeek'].isin(weekdays))
        ]
    
    #print(filtered_df['Category'].unique())
    #print(acc.Category.unique())
    traces = []

    for cat in acc.Category.unique():
        count = 0
        for i in filtered_df.Category:
            if i == cat:
                count += 1
        
        #print(count)
        count1 = [count]
        cat1 = [cat]
        traces.append({

            'type': 'bar',
            'y' : count1,
            'x' : cat1,
            'name' : cat
        })

    #print(traces)
    fig = {

        'data' : traces,
        'layout' : {
              'paper_bgcolor' : 'rgb(26,25,25)',
              'plot_bgcolor' : 'rgb(26,25,25)',
              'font' : {
                  'color' : 'rgb(250,250,250'
              },
              'height' : 500,
              'title' : 'Crimes by Category',
              
              'legend' : { # Horizontal legens, positioned at the bottom to allow maximum space for the chart
                  'orientation' : 'v',
                  'x' : 1,
                  'y' : 0,
                  'yanchor' : 'bottom',
                }
        }

    }

    return fig



@app.callback(
    Output(component_id='Parallel set', component_property='figure'),
    [Input(component_id='dayChecklist', component_property='value'),
    ]
)

def updateParallelSet(weekdays):
  
    filtered_df = acc[[
        'Category','PdDistrict','Resolution','Time']][
            (acc['DayOfWeek'].isin(weekdays))
        ]
    
    #print(list(filtered_df.Category)

    traces = []
    count = 0
    
    cat = []
    catu = []
    c = []
    pddis = []
    pddisu = []
    p = []
    res = []
    resu = []
    r = []

    count = 0

    cdic = {}
    for i in filtered_df.Category.unique():
        c.append(count)
        cdic[i] = count 
        count += 1
    
    pdic = {}
    count = 0
    for i in filtered_df.PdDistrict.unique():
        p.append(count)
        pdic[i] = count 
        pddisu.append(i)
        count += 1
    
    #print(pddisu)
    rdic = {}
    count = 0

    for i in filtered_df.Resolution.unique():
        r.append(count)
        rdic[i] = count 
        count += 1
    
    for i in filtered_df.Category:
        cat.append(cdic[i])
    
    for i in filtered_df.PdDistrict:
        pddis.append(pdic[i])
    
    for i in filtered_df.Resolution:
        res.append(rdic[i])


    if not c:
        c.append(0)
        p.append(0)
        r.append(0)
        
    

    fig = go.Figure(data=
        go.Parcoords(
        line_color = 'blue',
        dimensions = list([
            
            dict(
                 range = [0,p[-1]],
                 tickvals = p,
                 ticktext = pddisu,
                 label = 'PdDistrict', 
                 values = pddis),
            dict(
                 range = [0,r[-1]],
                 tickvals = r,
                 ticktext = list(filtered_df.Resolution.unique()),
                 label = 'Resolution', 
                 values = res,
                 ),
            dict(
                 range = [0,c[-1]],
                 tickvals = c,
                 ticktext = list(filtered_df.Category.unique()) ,
                 label = 'Category', 
                 values = cat)
        ])
    )
)

    fig.update_layout(
    plot_bgcolor = 'rgb(26,25,25)',
    paper_bgcolor = 'rgb(26,25,25)',
    font = dict(
                  color = 'rgb(250,250,250)'
    ),
    height = 750,
    title = 'Parallel Coordinates Plot'
)
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)