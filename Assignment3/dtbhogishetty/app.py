import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

data = pd.read_csv('Los_Angeles_International_Airport_-_Passenger_Traffic_By_Terminal.csv')
data['ReportPeriod'] = pd.to_datetime(data['ReportPeriod'])
data['Year'] = data['ReportPeriod'].dt.year
#data.drop(['DataExtractDate','ReportPeriod'],axis=1,inplace=True)
ddf = data.groupby(['Domestic_International','Year']).sum().reset_index()
#term_df = data.groupby(['Year']).sum().reset_index()
#data.drop('Arrival_Departure',axis=1)
#data['DataExtractDate']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def load_year():
    ddOps = (
     [{'label':year,'value':year} for year in ddf.Year]
    )
    return ddOps

app.layout = html.Div([
    html.Div([
        html.H2("Exploring the LAX airport")],
        style = {'text-align':'center','color':'#0099cc'}
    ),
    html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id='year-slider',
            min=ddf['Year'].min(),
            max=ddf['Year'].max(),
            value=ddf['Year'].min(),
            marks={str(y):str(y) for y in ddf['Year']},
            step=None
        )
    ]),
    html.Div([
        html.Div([
            html.H3("Terminal usage Frequency")],
            style = {'text-align':'center','color':'#0099cc','margin-top':'75px'}
        ),
        html.Div([
            dcc.Graph(id='graph-with-dropdown')],
            style = {'width':'80%','float':'left'}
        ),
        html.Div([
            dcc.Dropdown(id='year-dropdown',
            options=load_year(),
            placeholder="Select a year")],
            style = {'width':'20%','float':'right','margin-top':'100px'}
        )
    ],
    style = {'height':'500px'})
])

@app.callback(
    Output('graph-with-slider','figure'),
    [Input('year-slider','value')])
def update_figure(selected_year):
    temp_df = ddf[ddf['Year'] == selected_year]
    return {
        'data':[{
        'x':temp_df.Domestic_International,
        'y':temp_df.Passenger_Count,
        'type':'bar'
        }],
        'layout':dict(
            title='What type of travellers does LAX get?',
            xaxis={'title':'Type of Travel'},
            yaxis={'title':'Number of Passengers'},
            margin={'l':60,'b':60,'r':10},
            hovermode='closest',
            transition={'duration':800},

        )
    }

@app.callback(
    Output('graph-with-dropdown','figure'),
    [Input('year-dropdown','value')])
def update_figure(year):
    temp_df = data[data['Year'] == year]
    temp_df.drop(['DataExtractDate','ReportPeriod'],axis=1,inplace=True)
    fig = px.parallel_categories(temp_df)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
