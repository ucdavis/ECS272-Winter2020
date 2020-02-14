# ECS 272 HW4
# layout part
# Written by Jingwei Wan and Mingye Fu

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from data_preprocessing import *

from ParallelCoordinate import ParallelCoordinate
from BarPlot import BarPlot
from PiePlot import PiePlot
from ScatterPlot import ScatterPlot

data = OriginalData()
header = data.columns

feature_list = header[0:26].append(header[28:len(header)])
cate_list = header[26:28]

available_alc = cate_list.tolist()
available_x = feature_list.tolist()
available_methods = ['None', 'PCA', 'T-SNE']

dict_features = {
    "school": "student's school",
    "sex": "student's gender",
    "age": "student's age",
    "address": "home address type",
    "famsize": "family size",
    "Pstatus": "parent's cohabitation status",
    "Medu": "mother's education",
    "Fedu": "father's education",
    "Mjob": "mother's job",
    "Fjob": "father's job",
    "reason": "reason to choose this school",
    "guardian": "student's guardian",
    "traveltime": "home to school travel time",
    "studytime": "weekly study time",
    "failures": "number of class failures",
    "schoolsup": "extra educational support",
    "famsup": "family educational support",
    "paid": "extra paid classes",
    "activities": "extra-curricular activities",
    "nursery": "attended nursery school",
    "higher": "higher education wish",
    "internet": "Internet access at home",
    "romantic": "with a romantic relationship",
    "famrel": "quality of family relationships",
    "freetime": "free time after school",
    "goout": "going out with friends",
    "Dalc": "workday alcohol consumption",
    "Walc": "weekend alcohol consumption",
    "health": "current health status score",
    "absences": "number of school absences",
    "G1": "first period grade",
    "G2": "second period grade",
    "G3": "final grade"
}

# ================================== Dash setting ========================================
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.Div(children='Student Alcohol Consumption Data Visualization',
             style={'text-align': 'center',
                    'color': 'rgba(245, 240, 214, 1)',
                    'font-family': 'Courier New, monospace',
                    'font-size': '40px',
                    'padding-top': '50px',
                    'background-image': 'https://images.unsplash.com/photo-1571613316887-6f8d5cbf7ef7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1951&q=80'}
             ),

    html.Div(children=[
        html.Img(src='https://www.pinclipart.com/picdir/big/486-4868250_beer-bottle-icon-png-beer-clipart.png',
                 style={
                     'height': '10%',
                     'width': '10%',
                     'text-align': 'right',
                     'padding-top': '0px',
                     'padding-left': '5%',
                     'float': 'left'

                 },
                 ),

        html.Div(children='Group member: Jingwei Wan & Mingye Fu',
                 style={'text-align': 'center',
                        'color': 'rgba(245, 240, 214, 1)',
                        'font-family': 'FreeMono, monospace',
                        'font-size': '20px',
                        'width': '60%',
                        'padding-top': '100px',
                        'margin': 'auto',
                        'padding-bottom': '50px',
                        }
                 ),

        html.Div(
            children='The data were obtained in a survey of students in secondary school. It contains a lot of interesting ' +
                     'social, gender and study information about students. The main point here is to find out the relationship between these ' +
                     'attributes and student alcohol consumption. By clicking the drop down menu below, you can choose which alcohol consumption '
                     'type to show.',
            style={'color': 'rgba(245, 240, 214, 1)',
                   'font-family': 'Courier New, monospace',
                   'font-size': '20px',
                   'width': '60%',
                   'padding-top': '0px',
                   'margin': 'auto',
                   'padding-bottom': '0px',
                   }
            ),

    ]
    ),

    html.Div([
        dcc.Dropdown(
            id='cate',
            options=[{'label': dict_features[i], 'value': i} for i in cate_list],
            value=cate_list[0]
        )
    ],
        style={'width': '30%',
               'padding-top': '50px',
               'margin-left': '20%',
               'font-family': 'FreeMono, monospace'
               }
    ),

    html.Div(
        children='1. Overview - parallel Coordinate',
        style={'color': 'rgba(245, 240, 214, 1)',
               'font-family': 'Courier New, monospace',
               'font-size': '30px',
               'width': '60%',
               'padding-top': '50px',
               'margin': 'auto',
               'padding-bottom': '0px',
               }
    ),

    html.Div(
        children='In this overview, all features or attributes are shown in the Sankey diagram below.'
                 ' Deeper color means heavier alcohol consumption.',
        style={'color': 'rgba(245, 240, 214, 1)',
               'font-family': 'Courier New, monospace',
               'font-size': '20px',
               'width': '60%',
               'padding-top': '30px',
               'margin': 'auto',
               'padding-bottom': '0px',
               }
    ),

    html.Div(
        dcc.Graph(id='Parallel Coordinate'),
        style={'overflow': 'auto',
               'text-align': 'center',
               'width': '80%',
               'margin': 'auto',
               }

    ),

    html.Div(
        children='2. Overview - Scatter Plot',
        style={'color': 'rgba(245, 240, 214, 1)',
               'font-family': 'Courier New, monospace',
               'font-size': '30px',
               'width': '60%',
               'padding-top': '50px',
               'margin': 'auto',
               'padding-bottom': '0px',
               }
    ),

    html.Div(
        children="One of the visualization methods (PCA, T-SNE) can be selected from the dropdown menu. "
                 "\'None\' option is for users to customize x and y axis from one of the available data properties.",
        style={'color': 'rgba(245, 240, 214, 1)',
               'font-family': 'Courier New, monospace',
               'font-size': '20px',
               'width': '60%',
               'padding-top': '30px',
               'margin': 'auto',
               'padding-bottom': '0px',
               }
    ),

    html.Div([
        html.Div(["visualization method", dcc.Dropdown(
            id='visualization_method',
            options=[{'label': i, 'value': i} for i in available_methods],
            value='PCA'
        )]),
    ],
        style={'width': '30%',
               'padding-top': '50px',
               'margin-left': '20%',
               'font-family': 'FreeMono, monospace'}
    ),

    html.Div(id = 'columns',children = [
        html.Label(["x-axis", dcc.Dropdown(
            id='x_column',
            value='G1'
        )]),
        html.Label(["y-axis", dcc.Dropdown(
            id='y_column',
            value='G3'
        )])
    ],
        style={'width': '30%',
               'padding-top': '50px',
               'margin-left': '20%',
               'font-family': 'FreeMono, monospace',
               'display': 'inline-block'}
    ),

    html.Div([
        dcc.Graph(id='scatter_plot')
    ],
        style={'width': '60%',
               'text-align': 'center',
               'padding-top': '20px',
               'margin': 'auto',
               'overflow': 'auto'},
    ),

    html.Div(
        children='3. Detail view',
        style={'color': 'rgba(245, 240, 214, 1)',
               'font-family': 'Courier New, monospace',
               'font-size': '30px',
               'width': '60%',
               'padding-top': '50px',
               'margin': 'auto',
               'padding-bottom': '0px',
               }
    ),

    html.Div(
        children='In the detail view, the relation between one arbitrary feature and alcohol consumption'
                 ' is shown below. Feature can be chosen through the drop down menu. The pie chart shows the '
                 'proportion of each category of one feature.',
        style={'color': 'rgba(245, 240, 214, 1)',
               'font-family': 'Courier New, monospace',
               'font-size': '20px',
               'width': '60%',
               'padding-top': '30px',
               'margin': 'auto',
               'padding-bottom': '0px',
               }
    ),

    html.Div([
        dcc.Dropdown(
            id='feature',
            options=[{'label': dict_features[i], 'value': i} for i in feature_list],
            value=feature_list[0]
        )
    ],
        style={'width': '30%',
               'padding-top': '50px',
               'margin-left': '20%',
               'font-family': 'FreeMono, monospace'}
    ),

    html.Div([
        dcc.Graph(id='bar',
                  hoverData={'points': [{'x': 'GP'}]}
                  )
    ],
        style={'width': '60%',
               'text-align': 'center',
               'padding-top': '20px',
               'margin': 'auto',
               'overflow': 'auto'},
    ),

    html.Div([
        dcc.Graph(id='pie')
    ],
        style={'width': '60%',
               'padding-top': '20px',
               'margin': 'auto',
               'overflow': 'auto'},
    ),

],

    style={'background-color': 'rgb(140, 95, 111)',
           'background-image': "url('beer.png')",
           'background-repeat': 'no-repeat',
           'margin': '0'},

)


@app.callback(
    Output('Parallel Coordinate', 'figure'),
    [Input('cate', 'value')]
)
def update_graph(cate):
    fig = ParallelCoordinate(data, cate, feature_list, dict_features)
    return fig


@app.callback(
    Output('bar', 'figure'),
    [Input('feature', 'value'), Input('cate', 'value')]
)
def update_graph(feature, cate):
    fig = BarPlot(data, cate, feature, dict_features)
    return fig


@app.callback(
    Output('pie', 'figure'),
    [Input('bar', 'hoverData'),
     Input('feature', 'value'),
     Input('cate', 'value')])
def update_pie(hoverData, feature, cate):
    fig = PiePlot(data, hoverData, feature, cate, dict_features)

    return fig

@app.callback(
    [Output('x_column', 'options'),
    Output('y_column', 'options'),
    Output('columns', 'style')],
    [Input('visualization_method', 'value')]
)
def update_selections(method):
    if method == 'None':
        return [{'label': dict_features[i], 'value': i} for i in available_x], [{'label': dict_features[i], 'value': i} for i in available_x], {'width': '30%',
               'padding-top': '50px',
               'margin-left': '20%',
               'font-family': 'FreeMono, monospace',
               'display': 'inline-block'}
    else:
        return [],[], {'width': '30%',
               'padding-top': '50px',
               'margin-left': '20%',
               'font-family': 'FreeMono, monospace',
               'display': 'none'}

@app.callback(
    [Output('scatter_plot', 'figure')],
    [Input('visualization_method', 'value'),
    Input('cate','value'),
     Input('x_column','value'),
    Input('y_column','value')
    ]
)

def update_scatter(method, cate, x_column, y_column):
    return ScatterPlot(data, method, cate, x_column, y_column)


if __name__ == '__main__':
    app.run_server(debug=True)
