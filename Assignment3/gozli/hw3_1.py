import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

filename = "LAX_Terminal_Passengers.csv"

df = pd.read_csv(filename)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='The distribution of passenger in each terminal'),

    html.Div(children='''
        The distribution of passengers amount of each terminal in each month of the entire year of 2018.
    '''),

    html.Div([
        html.Label('Month'),
        dcc.Dropdown(
            id='month',
            options=[{'label': i, 'value': i} for i in ('01/01/2018 12:00:00 AM', '02/01/2018 12:00:00 AM', 
            '03/01/2018 12:00:00 AM', '04/01/2018 12:00:00 AM', '05/01/2018 12:00:00 AM', '06/01/2018 12:00:00 AM',
            '07/01/2018 12:00:00 AM', '08/01/2018 12:00:00 AM', '09/01/2018 12:00:00 AM', '10/01/2018 12:00:00 AM',
            '11/01/2018 12:00:00 AM', '12/01/2018 12:00:00 AM'
            )],
            value='',
            placeholder='Select...',
        )
    ],    
    style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '20px'}),

    dcc.Graph(
        id='distribution'
        )
])

@app.callback(
    Output(component_id='distribution', component_property='figure'),
    [
        Input(component_id='month', component_property='value')
    ]
)

def update_graph(month):
    filtered_df = df.loc[df['ReportPeriod'] == month]
    traces = []
    for i in filtered_df.ReportPeriod.unique():
        df_by_month = filtered_df[filtered_df['ReportPeriod'] == i]
        traces.append(go.Bar(
            x=df_by_month['Terminal'],
            y=df_by_month['Passenger_Count'],
            text=df_by_month['ReportPeriod'],
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(title='Passenger count for {}'.format(month))
    }

if __name__ == '__main__':
    app.run_server(debug=True)