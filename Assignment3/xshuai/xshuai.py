import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import urllib.request as req
from dash.dependencies import Input, Output
import plotly.express as px



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dataset = req.urlopen('http://stream.cs.ucdavis.edu/datasets/LAX_Terminal_Passengers.csv')
data = pd.read_csv(dataset)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

terminal0= data['Terminal'].unique().tolist()
arrivals= data['Arrival_Departure'].unique().tolist()
domestics= data['Domestic_International'].unique().tolist()
months=['01','02','03','04','05','06','07','08','09','10','11','12']


app.layout = html.Div([
    html.H1('ECS272 Assignment 3 ---- Xinlin Shuai'),
    html.H2('Basic visualization'),
    html.Br(),
    html.Div('This basic visualization uses Line chart'),
    html.Div('It shows the number of 4 kinds (1.Arrival_Domestic 2.Arrival_International 3.Departure_Domestic 4.Departure_International) of the whole year at one terminal'),
    dcc.Dropdown(id='year',options=[
        {'label':i,'value':i} for i in range (2006,2019)],
        value = 2008
        ),
    dcc.Dropdown(id='terminal',options=[
        {'label': terminal00,'value':terminal00} for terminal00 in terminal0],
        value = 'Terminal 2'
        ),
    dcc.Graph(id='line'),
    html.Br(),
    html.H2('Advanced visualization'),
    html.Div('This advanced visualization uses Sankey Diagram'),
    html.Div('It shows this year the passengers of every month, every terminal, every Domestic_International, Arrival_Departure'),
    dcc.Dropdown(id='year2',options=[
        {'label':i,'value':i} for i in range (2006,2020)],
        value = 2008
    ),
    dcc.Graph(id='sankey')
    ]
,style={'textAlign': 'center'})



@app.callback(
    Output('line','figure'),
    [Input('terminal','value'),
     Input('year','value')]
    )
def update(terminal1,year1):
    newdata1 = data[data['ReportPeriod'].str.slice(start=6,stop=10) == (str(year1))]
    newdata2 = newdata1[newdata1['Terminal'] == terminal1]
    result1=[]
    result2=[]
    result3=[]
    result4=[]
    for month in months:
        n3 = newdata2[newdata2['ReportPeriod'].str.slice(start=0, stop=2) == month]
        n0 = n3[n3['Arrival_Departure']=='Arrival'][n3['Domestic_International']=='Domestic']
        result1.append(sum(n0["Passenger_Count"]))
        n01 = n3[n3['Arrival_Departure']=='Arrival'][n3['Domestic_International']=='International']
        result2.append(sum(n01["Passenger_Count"]))
        n02 = n3[n3['Arrival_Departure']=='Departure'][n3['Domestic_International']=='Domestic']
        result3.append(sum(n02["Passenger_Count"]))
        n03 = n3[n3['Arrival_Departure']=='Departure'][n3['Domestic_International']=='International']
        result4.append(sum(n03["Passenger_Count"]))
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months,y=result1,mode='lines+markers',name='Arrival_Domestic'))
    fig.add_trace(go.Scatter(x=months,y=result2,mode='lines+markers',name='Arrival_International'))
    fig.add_trace(go.Scatter(x=months,y=result3,mode='lines+markers',name='Departure_Domestic'))
    fig.add_trace(go.Scatter(x=months,y=result4,mode='lines+markers',name='Departure_International'))
      
    fig.update_layout(title='Number of Passengers Through The Whole Year {} At Terminal {}'.format(year1,terminal1)
                      ,xaxis_title='Month',
                      yaxis_title='Number of Passengers')

    return fig




@app.callback(
    Output('sankey','figure'),
    [Input('year2','value')]
    )
def update_figure(year2):
    newdata = data[data['ReportPeriod'].str.slice(start=6,stop=10) == (str(year2))][['ReportPeriod','Terminal', 'Domestic_International', 'Arrival_Departure']]
    figure = px.parallel_categories(newdata)
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
