import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv('.\Police_Department_Incidents_-_Previous_Year__2016_.csv').dropna()
df['Date']=df['Date'].map(lambda x: int( x[0:2]) )
Date_df=df['Date'].unique()
Date_df.sort()

district_df = df['PdDistrict'].unique()
district_df=district_df.tolist()
district_df.sort()

df['Hour']=df['Time'].map(lambda x:int(x[0:2]))
df.loc[df.Hour<4,'Period'] = '0-4'
df.loc[(df.Hour<8) & (df.Hour>=4),'Period'] = '4-8'
df.loc[(df.Hour<12) & (df.Hour>=8) ,'Period'] = '8-12'
df.loc[(df.Hour<16) & (df.Hour>=12) ,'Period'] = '12-16'
df.loc[(df.Hour<20) & (df.Hour>=16) ,'Period'] = '16-20'
df.loc[(df.Hour<=24) & (df.Hour>=20),'Period'] = '20-24'

category_df=df['Category'].unique()
category_df=category_df.tolist()
category_df.sort()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(
            children='Places of crime in different districts in different months',
            style = dict(textAlign = 'center')),

    html.Label('Month'),

    html.Div([
          dcc.Dropdown(
          id='xaxis-column',
          options=[{'label': i, 'value': i} for i in Date_df],
          value=1
    )
    ],
        style={'width': '5%', 'display': 'inline-block'}),

    dcc.Graph(id='scatter_graph'),

    html.H1(
            children='Criminal Dispositions in Different Blocks at Different Time Periods',
            style = dict(textAlign = 'center')),

    html.Div([
        html.Div([
            html.Label('Category')
        ]
        ,style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Month')
        ]
        ,style={'width': '48%', 'float': 'right','display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='Category_dropdown',
                options=[{'label': i, 'value': i} for i in category_df],
                value='ARSON'
            )
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='Date_dropdown',
                options=[{'label': i, 'value': i} for i in Date_df],
                value=1
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
     dcc.Graph(id='parallel_graph')
])

@app.callback(
    Output('scatter_graph', 'figure'),
    [Input('xaxis-column', 'value')])
def update_figure(xaxis_column_name):
    filtered_df = df[df['Date'] == xaxis_column_name]
    traces = []
    for i in district_df:
        df_by_district = filtered_df[filtered_df['PdDistrict'] == i]
        traces.append(dict(
            x=df_by_district['X'],
            y=df_by_district['Y'],
            text=df_by_district['Category'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 8,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Latitude'},
            yaxis={'title': 'Longitude'},
            margin={'l': 60, 'b': 40, 't': 40, 'r': 60},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
    }


@app.callback(
    Output('parallel_graph', 'figure'),
    [Input('Category_dropdown', 'value'), Input('Date_dropdown','value')])
def update_figure(selected_category,selected_date):
    filtered_df = df[df['Date'] == selected_date ]
    dff=filtered_df[filtered_df['Category']== selected_category]
    category_dim = go.parcats.Dimension(
        values=dff['PdDistrict'].tolist(),
        label="District"
    )

    resolution_dim = go.parcats.Dimension(
        values=dff['Resolution'].tolist(),
        label="Resolution"
    )

    day_dim=go.parcats.Dimension(
        values=dff['Period'].tolist(),
        label="Time Period"
    )
    data=[go.Parcats(dimensions=[category_dim,resolution_dim,day_dim],
                     #line={'shape': 'hspline','colorbar':{'lenmode':'pixels','len':30}},
                     line={'shape':'hspline'},
                     hoverinfo = 'count+probability',arrangement='freeform')]

    return {
        'data':data
    }

if __name__ == '__main__':
    app.run_server(debug=True)