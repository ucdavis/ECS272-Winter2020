# Sammy Jia sajia ecs272 InfoVis asg3
# Uses the Ballot Measures dataset

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# gets the ballot measures dataset; csv file should be in the datasets folder
dataset = pandas.read_csv('../datasets/List_of_Historical_Ballot_Measures.csv')

# breaks the years into groups; there are 5 groups
min_year = dataset['Year'].min()
max_year = dataset['Year'].max()
year_range = int(((max_year - min_year + 1) / 5) - 1) # determines how big each group is

# holds the first year of each year group
unique_years = [min_year]
for index in range(4):
    unique_years.append(int(unique_years[index] + year_range + 1))

# labels each row based on their year group
for index in dataset.index:
    row = dataset.iloc[index]
    curr_year = row['Year']
    if curr_year <= unique_years[1]:
        dataset.at[index, 'Year Group'] = 0
    elif curr_year <= unique_years[2]:
        dataset.at[index, 'Year Group'] = 1
    elif curr_year <= unique_years[3]:
        dataset.at[index, 'Year Group'] = 2
    elif curr_year <= unique_years[4]:
        dataset.at[index, 'Year Group'] = 3
    else:
        dataset.at[index, 'Year Group'] = 4


app.layout = html.Div(style={'padding': '1em', 'border-style': 'solid'}, children=[
    html.H2(
        'ECS 272 InfoVis Assignment 3 - Sammy Jia',
        style={
            'textAlign': 'center',
        }
    ),

    # basic graph - scatter plot
    dcc.Graph(id='basic-graph'),
    # basic graph's slider; selects which year group to use
    dcc.Slider(
        id='basic-year-slider',
        min=dataset['Year Group'].min(),
        max=dataset['Year Group'].max(),
        value=dataset['Year Group'].min(),
        marks={index: str(unique_years[index]) + ' - ' + str(unique_years[index] + year_range) for index in range(5)},
        step=None
    ),

    # advanced graph - alluvial diagram
    dcc.Graph(id='advanced-graph'),
    # advanced graph's slider; selects which year group to use
    dcc.Slider(
        id='advanced-year-slider',
        min=dataset['Year Group'].min(),
        max=dataset['Year Group'].max(),
        value=dataset['Year Group'].min(),
        marks={index: str(unique_years[index]) + ' - ' + str(unique_years[index] + year_range) for index in range(5)},
        step=None
    )
])


# basic graph's callback function; used when slider is interacted with
# updates the basic graph with the selected year group; is a scatter plot
@app.callback(
    Output('basic-graph', 'figure'),
    [Input('basic-year-slider', 'value')])
def update_basic_figure(selected_year_group):
    # selects the year group's data
    filtered_dataset = dataset[dataset['Year Group'] == selected_year_group]

    # gets the data points from the data set
    traces = []
    for i in filtered_dataset['Pass or Fail'].unique():
        dataset_by_pass_or_fail = filtered_dataset[filtered_dataset['Pass or Fail'] == i]
        traces.append(dict(
            x=dataset_by_pass_or_fail['No Votes'],
            y=dataset_by_pass_or_fail['Yes Votes'],
            text=dataset_by_pass_or_fail['Subject'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    # returns the components needed to update the scatter plot
    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'linear', 'title': 'Number of No Votes',
                   'range': [0, dataset['No Votes'].max() + int(10000)]},
            yaxis={'title': 'Number of Yes Votes',
                   'range': [0, dataset['Yes Votes'].max() + int(20000)]},
            margin={'l': 70, 'b': 70, 't': 10, 'r': 40},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition={'duration': 1000},
            title={'text': "Basic Graph - Ballot Measure Yes/No Vote Scatter Plot By Decade",
                   'y': 0.9,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'size': 20}
        )
    }


# color scale for the advanced graph
colorscale = [[0, 'lightpink'], [1, 'lightblue']]


# advanced graph's callback function; used when slider is interacted with
# updates the advanced graph with the selected year group; is an alluvial diagram
@app.callback(
    Output('advanced-graph', 'figure'),
    [Input('advanced-year-slider', 'value')])
def update_advanced_figure(selected_year_group):
    # selects the year group's data
    filtered_dataset = dataset[dataset['Year Group'] == selected_year_group]

    # creates the pass or fail column's dimension
    pass_dim = go.parcats.Dimension(
        values=filtered_dataset['Pass or Fail'],
        label='Pass or Fail'
    )
    # creates the by column's dimension
    by_dim = go.parcats.Dimension(
        values=filtered_dataset['By'],
        label='Placed on Ballot By'
    )
    # creates the type measure column's dimension
    type_dim = go.parcats.Dimension(
        values=filtered_dataset['Type Measure'],
        label='Ballot Type of Measure'
    )

    # converts the pass or fail column into a binary list
    color_list = [0 if result == 'F' else 1 for result in filtered_dataset['Pass or Fail']]

    # returns the components needed to update the alluvial diagram
    return {
        'data': [go.Parcats(dimensions=[pass_dim, by_dim, type_dim],
                            line={'color': color_list, 'colorscale': colorscale},
                            hoveron='color', hoverinfo='probability',
                            labelfont={'size': 17, 'family': 'Times'},
                            tickfont={'size': 12, 'family': 'Times'},
                            arrangement='freeform')],
        'layout': dict(
            title={
                'text': "Advanced Graph - Ballot Measure Alluvial Diagram By Decade",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            margin={'b': 20},
            titlefont={'size': 20}
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
