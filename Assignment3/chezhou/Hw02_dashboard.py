import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv('../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

color_dict = {}
count = 0
for i in df['Category'].unique():
    color_dict[i] = count
    count += 5
color_code = []
for i in df['Category']:
    color_code.append(color_dict[i])
df['Color'] = color_code

week_dict = {}
count = 0
for i in df['DayOfWeek'].unique():
    week_dict[i] = count
    count += 5
week_code = []
for i in df['DayOfWeek']:
    week_code.append(week_dict[i])
df['Week'] = week_code

pd_dict = {}
count = 0
for i in df['PdDistrict'].unique():
    pd_dict[i] = count
    count += 5
pd_code = []
for i in df['PdDistrict']:
    pd_code.append(pd_dict[i])
df['Pd'] = pd_code

res_dict = {}
count = 0
for i in df['Resolution'].unique():
    res_dict[i] = count
    count += 5
res_code = []
for i in df['Resolution']:
    res_code.append(res_dict[i])
df['Res'] = res_code

df.index = pd.to_datetime(df["Time"], format="%H:%M")

app.layout = html.Div([
    html.Div([
        html.H1(
            children='Scatter Plot for Robbery/Assult/Trespass Position',
            style={'textAlign': 'center'}
        ),
        dcc.Graph(id='scatter-with-slider'),
        dcc.Slider(
            id='time-slider',
            min=0,
            max=23,
            step=1,
            value=0,
            marks={hour: str(hour) + ":00 - " + str(hour+1) + ":00" for hour in range(0, 24)},
        )
    ]),
    html.Div([
        html.H1(
            children='Parallel Coordinate Plot for Incidents',
            style={'textAlign': 'center'}
        ),
        html.H1('select the color scale...', style={'font-size': '150%'}),
        dcc.Dropdown(
            id='parallel-color-change',
            options=[
                {'label': 'YIGnBu Colorscale', 'value': 'ylgnbu'},
                {'label': 'RdBu Colorscale', 'value': 'rdbu'},
                {'label': 'Jet Colorscale', 'value': 'jet'},
                {'label': 'Electric Colorscale', 'value': 'electric'}
            ],
            value='electric'
        ),
        dcc.Graph(id='parallel-coordinate'),
    ]),
])

@app.callback(
    Output('scatter-with-slider', 'figure'),
    [Input('time-slider', 'value')])
def update_scatter_figure(selected_time):
    hour_start = str(selected_time) + ":00"
    hour_end = str(selected_time) + ":59"
    filtered_df = df.between_time(hour_start, hour_end)
    traces = []
    crime = ["ROBBERY", "ASSAULT", "TRESPASS"]
    for i in crime:
        df_by_category = filtered_df[filtered_df["Category"] == i]
        traces.append(dict(
            x=df_by_category["Y"],
            y=df_by_category["X"],
            text=df_by_category["Descript"],
            mode="markers",
            marker={
                'size': 5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Longitude', 'range': [37.7, 37.82]},
            yaxis={'title': 'Latitude', 'range': [-122.55, -122.3]},
            margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500}
        )
    }

@app.callback(
    Output('parallel-coordinate', 'figure'),
    [Input('parallel-color-change', 'value')])
def update_parallel_figure(selected_color):
    week_text = [i for i in week_dict]
    week_vals = [week_dict[i] for i in week_text]
    
    pd_text = [i for i in pd_dict]
    pd_vals = [pd_dict[i] for i in pd_text]
    
    res_text = [i for i in res_dict]
    res_vals = [res_dict[i] for i in res_text]

    color_text = [i for i in color_dict]
    color_vals = [color_dict[i] for i in color_text]

    fig = go.Figure(
        data=go.Parcoords(
            line=dict(
                color=df['Color'],
                colorscale=selected_color,
                showscale=True,
                cmin=min(color_code),
                cmax=max(color_code),
                colorbar=dict(
                    tickvals=color_vals,
                    ticktext=color_text
                )
            ),
        dimensions = list([
            dict(
                tickvals = week_vals,
                ticktext = week_text,
                label = 'Day of Week', values = df['Week']
            ),
            dict(
                tickvals = pd_vals,
                ticktext = pd_text,
                label = 'Police Department District', values = df['Pd']
            ),
            dict(
                tickvals = res_vals,
                ticktext = res_text,
                label = 'Resolution', values = df['Res'] 
            )
        ])
        )
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)