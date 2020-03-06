import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
from ipywidgets import widgets

import pandas as pd
import numpy as np

df = pd.read_csv("/Users/dongbinxin/Desktop/Police_Department_Incidents_-_Previous_Year__2016_.csv")
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df2 = df[1:1000]

# Build parcats dimensions
categorical_dimensions = ['Resolution', 'PdDistrict', 'DayOfWeek'];
dimensions = [dict(values=df2[label], label=label) for label in categorical_dimensions]

# Build colorscale
color = np.zeros(len(df2), dtype='uint8')
colorscale = [[0, 'gray'], [1, 'red']]

# Build figure as FigureWidget
fig = go.FigureWidget(
    #data=[go.Scatter(x=cars_df.X[1:1000], y=cars_df.Y[1:1000],
    data=[go.Scatter(x=df2.X, y=df2.Y,
    marker={'color': 'gray'}, mode='markers', selected={'marker': {'color': 'red'}},
    unselected={'marker': {'opacity': 0.3}}),
          go.Parcats(
         domain={'y': [0, 0.4]},dimensions=dimensions,
        line={'colorscale': colorscale, 'cmin': 0,
              'cmax': 1, 'color': color, 'shape': 'hspline'})
    ])

fig.update_layout(
        height=800, xaxis={'title': 'longitude'},
        yaxis={'title': 'latitude', 'domain': [0.6, 1]},
        dragmode='lasso', hovermode='closest')

def update_color(trace, points, state):
    # Update scatter selection
    fig.data[0].selectedpoints = points.point_inds

    # Update parcats colors
    new_color = np.zeros(len(df2), dtype='uint8')
    new_color[points.point_inds] = 1
    fig.data[1].line.color = new_color

# Register callback on scatter selection...
fig.data[0].on_selection(update_color)
# and parcats click
fig.data[1].on_click(update_color)

#build a dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
available_Categorys = df['Category'].unique()
app.layout = html.Div([
    html.H2('Basic visualization'),
    dcc.Graph(id='Category-graphic'),
    dcc.Dropdown(
        id='xaxis-column',
        options=[{'label': i, 'value': i} for i in available_Categorys],
        value='WEAPON LAWS'
    ),

    html.Br(),
    html.Br(),
    html.H2('Advanced visualization'),
    dcc.Graph(figure= fig),
],style={'textAlign': 'center'})


@app.callback(
    Output('Category-graphic', 'figure'),
    [Input('xaxis-column', 'value')])
def update_figure(selected_Category):
    filtered_df = df[df.Category == selected_Category]
    traces = []
    for i in filtered_df.PdDistrict.unique():
        df_by_PdDistrict = filtered_df[filtered_df['PdDistrict'] == i]
        traces.append(dict(
            x=df_by_PdDistrict['X'],
            y=df_by_PdDistrict['Y'],
            text=df_by_PdDistrict['Resolution'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'linear', 'title': 'longtitude'},
            yaxis={'title': 'altitude'},
            margin={'l': 60, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)


