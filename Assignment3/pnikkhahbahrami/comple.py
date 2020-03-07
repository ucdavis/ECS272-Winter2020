import urllib.request as req
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import ipywidgets as widgets

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dataFile = "/home/pooneh/Assignment3/datasets/LA.csv"
df = pd.read_csv(dataFile)
df['Time'] = pd.to_datetime(df.ReportPeriod)
df.Time = df.Time.dt.year


app.layout = html.Div([
        html.H4(
        children='Number of passengers in each Terminal during different years separated based on International/Domestic flight',
    ),
    dcc.Graph(id='bubble_Graph'),
])

# Create dimensions
Time_dim = go.parcats.Dimension(
    values=df.Time,
    categoryorder='category ascending',
    label="Year"
)

Terminal_dim = go.parcats.Dimension(
    values=df.Terminal,
    label="Terminal"
)

Passengers_dim = go.parcats.Dimension(
  values=df.Passenger_Count,
  label="Passengers",
  categoryarray=[0, 1],
  ticktext=['empty', 'crowded'],
)

# Create parcats trace
color = df.Domestic_International;
colorscale = [['Domestic', 'lightsteelblue'], ['International', 'mediumseagreen']];



@app.callback(
     Output('bubble_Graph', 'figure'))
def update_figure():
    fig=go.Figure(data = [go.Parcats(dimensions=[Time_dim, Terminal_dim, Passengers_dim],
    line={'color': color,'colorscale': colorscale},
    hoveron='color',
    hoverinfo='count+probability',
    labelfont={'size': 18, 'family': 'Times'},
    tickfont={'size': 16, 'family': 'Times'},
    arrangement='freeform')])
    return {fig}

if __name__ == '__main__':
    app.run_server(debug=True)
