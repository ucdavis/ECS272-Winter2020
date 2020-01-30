import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

import plotly.figure_factory as ff

import numpy as np

import plotly.graph_objects as go
import plotly.express as px

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    buf = response.read()
    counties = json.loads(buf.decode('utf-8'))
    #counties = json.load(response)

#Style Sheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__ , external_stylesheets = external_stylesheets)

#Read CSV
dff = pd.read_csv('PDI.csv')
#Query and count
print(dff[dff.Category == 'WARRANTS'].shape[0])
#Generating Table
def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )
#generate_table(dff)
#Column Names
column_names = dff.columns
#print(column_names)

#Types of Categories of crime
crime_categories = dff['Category'].unique()
#print(crime_categories, type(crime_categories))

#Types of Districts
district_names = dff['PdDistrict'].unique()
#print(district_names)

#Days of the Week
days_of_week = dff['DayOfWeek'].unique()

#App Layout
app.layout = html.Div(children=[
    html.H1(children = "SF Crime Data"),
    html.H3(children= "Customize Graph"),
    html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': i, 'value': i} for i in crime_categories
            ],
            value=['WEAPON LAWS', 'WARRANTS'],
            multi=True
        ),
        dcc.Checklist(
            id='dayCheck',
            options=[
                {'label': i, 'value': i} for i in days_of_week
            ],
            value=['Sunday', 'Monday'],
            labelStyle={  # Different padding for the checklist elements
                'display': 'inline-block',
                'paddingRight': 10,
                'paddingLeft': 10,
                'paddingBottom': 5,
            },

        )
    ],
        style={
            "width": '50%',
            'display': 'inline-block',
            'paddingLeft': 10,
            'paddingRight': 60,
            'boxSizing': 'border-box',
        }
    ),

    html.Div([
        html.H3(children= "Parallel Coordinate Plot"),
        dcc.Graph(
            id = 'par-graph'
        )
    ]),

    html.Div(
        id = 'output-graph'
    ),

    html.Div([
        html.H3(children= "Scatter Map Plot of Crimes across San Francisco"),
        dcc.Graph(
            id = 'output-map'
        )
    ])


])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='dropdown', component_property='value'),
    Input(component_id='dayCheck', component_property='value')]
)


def update_graph(input_data, day):
    #print(input_data)
    #print("hello")
    #print(dff[dff.DayOfWeek == i] for i in day)
    #print(type(day))
    crime_list = []

    for i in input_data:
        crime_list.append(dff[(dff.Category == i) & (dff.DayOfWeek.isin(day))].shape[0])
    return dcc.Graph(
        id = 'example-graph',
        figure = {
            'data': [
                {'x' : input_data, 'y' : crime_list,
                 'type' : 'bar',
                'marker':{
                    'color' : '#0277bd'
                    }
                }
            ],
            'layout' : {
                'title' : 'Crime Data',
                'hovermode' :'closest',
                'paper_bgcolor': '#e1f5fe',
                'plot_bgcolor' : '#e1f5fe',
                'height': 500,

            },

        }
    )

@app.callback(
    Output(component_id='output-map', component_property='figure'),
    [Input(component_id='dropdown', component_property='value'),
    Input(component_id='dayCheck', component_property='value')]
)
def updatemap(input_data, day):
    #print('INSIDE UPDATE MAP')

    px.set_mapbox_access_token("pk.eyJ1Ijoic21taXNocmEiLCJhIjoiY2s1eGF0aGNtMWJvczNxbXg2dDJiaG1kaiJ9.UOxmGAsTrKH_m4wCZTgrNg")
    df = px.data.carshare()
    #print(df.head())
    #print(df.dtypes)
    #print(dff.head())

    #Size is number of offurences of the category of crime
    #Color is number of unique types of crimes

    #plotsize is a list
    filtered_df = dff[[
        'Category', 'PdDistrict', 'Resolution', 'Time', 'X', 'Y']][
        (dff['DayOfWeek'].isin(day) & dff['Category'].isin(input_data))
    ]

    #Number the crime
    crime_dict = {}

    i = 0
    for crime in filtered_df['Category'].unique():
        crime_dict[crime] = i
        i += 1

    #crimeSize
    crimeSize = []
    for index,row in filtered_df.iterrows():
        crimeSize.append(crime_dict[row['Category']])

    #print('Number of records ', filtered_df.shape[0])
    #print(len(crimeSize))

    #CrimeColor
    #At a particular latitude and longitude , highest number of crimes -> category

    crime_list = []

    colorDict = {}
    crimeDict = {}

    x_list = []
    y_list = []
    crime_list = []
    num_crime_list = []
    count = 0
    for index in filtered_df.index:
        x = float(filtered_df['X'][index])
        y = float(filtered_df['Y'][index])
        #Get X and Y and store in list
        #x_list.append(x)
        #y_list.append(y)

        crime = input_data[0]

        #location and highest number of crimes
        #tempCount = filtered_df[(filtered_df.X == x) & (filtered_df.Y == y)].shape[0]
        flag = 0

        for i in input_data:
            tempCount = filtered_df[(filtered_df.X == x) & (filtered_df.Y == y) & (filtered_df.Category == i)].shape[0]
            if colorDict.get((x, y), 0) > tempCount:
                flag = 0
                continue
            else:
                flag = 1
                colorDict[(x, y)] = tempCount
                crime = i

        #num_crime_list.append(colorDict.get((x,y), 0))
        #Location and highest crime category
        crimeDict[(x,y)] = crime

        #print('Appended' ,count, num_crime_list[count], crime_list[count])
        #count += 1


    #Getting X and Y
    xy_list = colorDict.keys()
    for i in xy_list:
        x_list.append(i[0])
        y_list.append(i[1])
    for (x,y) in colorDict:
        num_crime_list.append(colorDict[(x,y)])
    for (x,y) in crimeDict:
        crime_list.append(crime_dict[crimeDict[(x,y)]])
    #print('xlist', len(x_list))
    #print('ylist', len(y_list))
    #print('Num crime',len(num_crime_list))
    #print('crime_list',len(crime_list))
    #print(len(crimeDict))

    #Create a new data frame (X,Y,Crime,NumberofCrime)
    d = {'X' : x_list, 'Y' : y_list, 'Crime' : crime_list, 'NumOfCrime' : num_crime_list}
    new_df = pd.DataFrame(data=d)
    #print(new_df.head())
    #print(new_df.dtypes)



    fig = px.scatter_mapbox(new_df, lat="Y", lon="X", color="Crime", size="NumOfCrime",
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)


    return fig

@app.callback(
    Output(component_id='par-graph', component_property='figure'),
    [Input(component_id='dropdown', component_property='value'),
     Input(component_id='dayCheck', component_property='value')]
)

def updateParCord(input_data, day):
    crimeList = []
    districtList = []
    resolutionList = []
    timeList = []

    crimeCount = 0
    districtCount = 0
    resolutionCount = 0
    #timeCount = 0

    crimeDict = {}
    districtDict = {}
    resolutionDict = {}
    timeDict = {}

    #Dataframe based on input parameters
    updated_df = dff[['PdDistrict','Category','X','Y','Resolution','Time']][(dff['DayOfWeek'].isin(day) & dff['Category'].isin(input_data))]


    #Maps the Category to a Value to be used later on
    crime_names = []
    for index in input_data:
        crimeList.append(crimeCount)
        crimeDict[index] = crimeCount
        crimeCount += 1
        crime_names.append(index)

    #Maps District Names to Value to be used later on
    district_names = []
    for index in updated_df['PdDistrict'].unique():
        districtList.append(districtCount)
        districtDict[index] = districtCount
        districtCount += 1
        district_names.append(index)

    #Maps various Resolution to Value to be used later on
    resolution_names = []
    for index in updated_df['Resolution'].unique():
        resolutionList.append(resolutionCount)
        resolutionDict[index] = resolutionCount
        resolutionCount += 1
        resolution_names.append(index)

    #Maps various Times to Value to be used later on
    # Get time for AM vs PM Crimes
    time_names = []
    time_names.append("AM")
    time_names.append("PM")

    timeDict["AM"] = 0
    timeDict["PM"] = 1

    timeList.append(0)
    timeList.append(1)
    '''
    for index in updated_df['Time']:
        timeList.append(timeCount)
        hour,minutes = index.split(":")
        if int(hour) > 12:
            timeDict["PM"] = timeCount
        else:
            timeList.append(0)
    '''

    #List of Crimes, District, Resolution and Time for Displaying on Parallel Coordinate Plots
    crimeCat = []
    district = []
    resol = []
    time = []
    for index in updated_df['Resolution']:
        resol.append(resolutionDict[index])
    for index in updated_df['PdDistrict']:
        district.append(districtDict[index])
    for index in updated_df['Category']:
        crimeCat.append(crimeDict[index])
    for index in updated_df['Time']:
        hour, minutes = index.split(":")
        if int(hour) > 12:
            time.append(timeDict["PM"])
        else:
            time.append(timeDict["AM"])



    figure = go.Figure(data=
    go.Parcoords(
        line = {
            'color' : crimeCat,
            'colorscale' : px.colors.cyclical.IceFire,
            'showscale' : True

        },
        dimensions=list([

            {
                'label': 'Crime Categories',
                'range': [0, len(input_data)],
                'tickvals': crimeList,
                'ticktext': crime_names,
                'values': crimeCat
            },
            {
                'label': 'District Name',
                'range': [0, len(district_names)],
                'tickvals': districtList,
                'ticktext': district_names,
                'values': district
            },
            {
                'label': 'Time',
                'range': [0, len(time_names)],
                'tickvals': timeList,
                'ticktext': time_names,
                'values': time
            },
            {
                'label': 'Resolution',
                'range': [0, len(resolution_names)],
                'tickvals': resolutionList,
                'ticktext': resolution_names,
                'values': resol
            }


        ])
    ))

    figure.update_layout(
        plot_bgcolor='#e1f5fe',
        paper_bgcolor='#e1f5fe',
    )
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)