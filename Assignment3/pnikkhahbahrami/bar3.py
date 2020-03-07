import urllib.request as req
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#load the dataset
dataFile = "/home/pooneh/Assignment3/datasets/LA.csv"
df = pd.read_csv(dataFile)
df['Time'] = pd.to_datetime(df.ReportPeriod)
df.Time = df.Time.dt.year

Flight_Type=df.Domestic_International.unique()

# Layout Design

app.layout = html.Div([
        html.H4(
        children='Number of passengers in each Terminal during different years separated based on International/Domestic flight',
    ),
        html.Div([
    dcc.RadioItems(id='chkBx_intdom',
        options=[{'label': i, 'value': i} for i in ['International', 'Domestic']],
        value='International',
        style={'width': '48%', 'display': 'inline-block'}),
    ]),
    dcc.Graph(id='bubble_Graph'),
    dcc.Slider(
        id='year_value',
        min=df['Time'].min(),
        max=df['Time'].max(),
        value=df['Time'].min(),
        marks={str(year): str(year) for year in df['Time'].unique()},
        step=None
    )
])

@app.callback(
    Output('bubble_Graph', 'figure'),
    [Input('year_value', 'value'),Input('chkBx_intdom', 'value')])
def update_figure(year_value, chkBx_intdom):
    df_year_filtered = df[df.Time == year_value]
    #filtered_df=df_year_filtered = df[df.Time == year_value]
    radio=""
    radio=chkBx_intdom
    df_IntDom_filtered=df_year_filtered[df_year_filtered['Domestic_International']==chkBx_intdom]

    terminals = []
    P_count = []
    for i in df_IntDom_filtered['Terminal'].unique():
        terminals.append(i)
    for t in terminals:
      new_df = df_IntDom_filtered[['Passenger_Count']][(df_IntDom_filtered['Terminal'] == t)]
      P_count.append(new_df.Passenger_Count.sum()) 
    return {'data': [{'x': terminals, 'y': P_count, 'type':'bar'}],
            'layout': dict(
                xaxis={'title': '#Passengers'},
                yaxis={'title': 'Terminal Name'},
                margin={'l': 100, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1}, hovermode='closest', transition = {'duration': 500})
}
if __name__ == '__main__':
    app.run_server(debug=True)
