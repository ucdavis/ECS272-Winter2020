#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import requests
import json
from collections import Counter


# In[ ]:


film = pd.read_csv("Film_Locations_in_San_Francisco.csv")


# # Heatmap and Dropdown Preprocessing

# In[ ]:


film_heat = film.groupby(["Production Company", "Release Year"], as_index = False).agg({'Locations': pd.Series.nunique})
conditions = [
    (film_heat['Release Year'] >= 1915) & (film_heat['Release Year'] < 1925),
    (film_heat['Release Year'] >= 1925) & (film_heat['Release Year'] < 1935),
    (film_heat['Release Year'] >= 1935) & (film_heat['Release Year'] < 1945),
    (film_heat['Release Year'] >= 1945) & (film_heat['Release Year'] < 1955),
    (film_heat['Release Year'] >= 1955) & (film_heat['Release Year'] < 1965),
    (film_heat['Release Year'] >= 1965) & (film_heat['Release Year'] < 1975),
    (film_heat['Release Year'] >= 1975) & (film_heat['Release Year'] < 1985),
    (film_heat['Release Year'] >= 1985) & (film_heat['Release Year'] < 1995),
    (film_heat['Release Year'] >= 1995) & (film_heat['Release Year'] < 2005),
    (film_heat['Release Year'] >= 2005) & (film_heat['Release Year'] < 2015),
    (film_heat['Release Year'] >= 2015) & (film_heat['Release Year'] < 2025)
]

choices = ['1915-1924', '1925-1934', '1935-1944', '1945-1954', '1955-1964',
           '1965-1974', '1975-1984', '1985-1994', '1995-2004', '2005-2014',
           '2015-2019']

film_heat['Time Period'] = np.select(conditions, choices, default='none')

film_heat['PC'] = film_heat['Production Company'].apply(lambda x: ''.join(i[0] for i in x.split()))

timeframe = film_heat['Time Period'].unique()
timeframe.sort()

time_default = '2015-2019'
film_heat_default = film_heat[(film_heat['Time Period'] == time_default)]


# # Arc Diagram and Slider Preprocessing

# In[ ]:


film_slider = film[film["Release Year"] >=2000]
initial_year_value = 2015

film_dropped = film.copy()
film_dropped.drop('Locations', axis=1, inplace=True)
film_dropped.drop('Fun Facts', axis=1, inplace=True)
film_dropped = film_dropped.drop_duplicates()

film_1 = film_dropped[["Release Year", "Actor 1", "Actor 2"]]
film_2 = film_dropped[["Release Year", "Actor 1", "Actor 3"]]
film_2 = film_2.rename(columns = {'Actor 3':'Actor 2'})
film_3 = film_dropped[["Release Year", "Actor 2", "Actor 3"]]
film_3 = film_3.rename(columns = {'Actor 2':'Actor 1','Actor 3':'Actor 2'})

film_final_ug = pd.concat([film_1, film_2])
film_final_ug = pd.concat([film_final_ug, film_3])

film_final_int = film_final_ug.groupby(["Release Year", "Actor 1", "Actor 2"]).size().to_frame('Links').reset_index()
film_final=film_final_int[(film_final_int['Release Year'] == initial_year_value)]

film_json_string = film_final.to_json(orient='records')
film_json = json.loads(film_json_string)
edges = [(item['Actor 1'], item['Actor 2'])  for item in film_json]
interact_strength = [item['Links'] for item in film_json]
keys = sorted(set(interact_strength)) 

actors1 = film_final[["Actor 1","Links"]]
actors2 = film_final[["Actor 2","Links"]]
actors2 = actors2.rename(columns = {'Actor 2':'Actor 1'})
actors = pd.concat([actors1, actors2])
actors = actors.groupby(["Actor 1"]).sum().reset_index()

node_data = []
for index, rows in actors.iterrows():
    temp_list =[rows['Actor 1'], rows['Links']] 
    node_data.append(temp_list)
values = [item[1] for item in node_data]
L = len(set(film_final['Actor 1'].tolist() + film_final['Actor 2'].tolist()))
labels = []
labels = [list[0] for list in node_data]

widths = [2+k*1 for k in range(25)]#+ [5+k*0.25 for k in range(8)]+[9+k*0.25 for k in range(7)]
d = dict(zip(keys, widths))  
nwidths = [d[val] for val in interact_strength] 

def get_b1(b0, b2):
    # b0, b1 list of x, y coordinates
    if len(b0) != len(b2) != 2:
        raise ValueError('b0, b1 must be lists of two elements')
    b1 = 0.5 * (np.asarray(b0)+np.asarray(b2))+         0.5 * np.array([0,1.0]) * np.sqrt(3) * np.linalg.norm(np.array(b2)-np.array(b0))
    return b1.tolist()


def dim_plus_1(b, w):#lift the points b0, b1, b2 to 3D points a0, a1, a2 (see Gallier book)
    #b is a list of 3 lists of 2D points, i.e. a list of three 2-lists 
    #w is a list of numbers (weights) of len equal to the len of b
    if not isinstance(b, list) or  not isinstance(b[0], list):
        raise ValueError('b must be a list of three 2-lists')
    if len(b) != len(w)   != 3:
        raise ValueError('the number of weights must be  equal to the nr of points')
    else:
        a = np.array([point + [w[i]] for (i, point) in enumerate(b)])
        a[1, :2] *= w[1]
        return a
    
    
def Bezier_curve(bz, nr): #the control point coordinates are passed in a list bz=[bz0, bz1, bz2] 
    # bz is a list of three 2-lists 
    # nr is the number of points to be computed on each arc
    t = np.linspace(0, 1, nr)
    #for each parameter t[i] evaluate a point on the Bezier curve with the de Casteljau algorithm
    N = len(bz) 
    points = [] # the list of points to be computed on the Bezier curve
    for i in range(nr):
        aa = np.copy(bz) 
        for r in range(1, N):
            aa[:N-r,:] = (1-t[i]) * aa[:N-r,:] + t[i] * aa[1:N-r+1,:]  # convex combination of points
        points.append(aa[0,:])                                  
    return np.array(points)


def Rational_Bezier_curve(a, nr):
    discrete_curve = Bezier_curve(a, nr ) 
    return [p[:2]/p[2] for p in discrete_curve]


pl_density = [[0.0, 'rgb(230,240,240)'],
              [0.1, 'rgb(187,220,228)'],
              [0.2, 'rgb(149,197,226)'],
              [0.3, 'rgb(123,173,227)'],
              [0.4, 'rgb(115,144,227)'],
              [0.5, 'rgb(119,113,213)'],
              [0.6, 'rgb(120,84,186)'],
              [0.7, 'rgb(115,57,151)'],
              [0.8, 'rgb(103,35,112)'],
              [0.9, 'rgb(82,20,69)'],
              [1.0, 'rgb(54,14,36)']]


# # Plotting

# In[ ]:


data = []
tooltips = [] 
xx = []
yy = []

hover_text = [f'{labels[k]}, {values[k]} collaborations' for k in range(L)]
node_trace = dict(type='scatter',
                  x=list(range(L)),
                  y=[0]*L,
                  mode='markers',
                  marker=dict(size=12, 
                              color=values, 
                              colorscale=pl_density,
                              showscale=False,
                              line=dict(color='rgb(50,50,50)', width=0.75)),
                  text=hover_text,
                  hoverinfo='text')
X = list(range(L)) # node x-coordinates
nr = 75 
for i, (j, k) in enumerate(edges):
    if labels.index(j) < labels.index(k):
        tooltips.append('interactions(' + j + ', ' + k + ')=' + str(interact_strength[i]))
    else:
        tooltips.append('interactions(' + k + ', ' + j + ')=' + str(interact_strength[i]))
    b0 = [X[labels.index(j)], 0.0]
    b2 = [X[labels.index(k)], 0.0]
    b1 = get_b1(b0, b2)
    a = dim_plus_1([b0, b1, b2], [1, 0.5, 1])
    pts = Rational_Bezier_curve(a, nr)
    xx.append(pts[nr//2][0]) #abscissa of the middle point on the computed arc
    yy.append(pts[nr//2][1]) #ordinate of the same point
    x,y = zip(*pts)
    
    data.append(dict(type='scatter',
                     x=x, 
                     y=y, 
                     name='',
                     mode='lines', 
                     line=dict(width=nwidths[i], color='#6b8aca', shape='spline'),
                     hoverinfo='none'
                    )
                )
data.append(dict(type='scatter',
                 x=xx,
                 y=yy,
                 name='',
                 mode='markers',
                 marker=dict(size=0.5, color='#a0b6e8'),
                 text=tooltips,
                 hoverinfo='text'))
data.append(node_trace)
title = "(Hover on Tips of Arcs for Interaction Counts)"
layout = dict(
         title=title, 
         font=dict(size=10), 
         width=1500,
         height=600,
         showlegend=False,
         xaxis=dict(anchor='y',
                    showline=False,  
                    zeroline=False,
                    showgrid=False,
                    tickvals=list(range(len(labels))), 
                    ticktext=labels,
                    tickangle=50,
                    ),
         yaxis=dict(visible=False), 
         hovermode='closest',
         margin=dict(t=80, b=110, l=10, r=10),
         annotations=[dict(showarrow=False, 
                           text='',
                           xref='paper',     
                           yref='paper',     
                           x=0.05,  
                           y=-0.3,  
                           xanchor='left',   
                           yanchor='bottom',  
                           font=dict(size=11 ))
                                  ]
                 
           
    )
arc_fig = go.FigureWidget(data=data, layout=layout)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
 html.H2('Number of Different Locations Production Companies Filmed at in San Francisco'),
 html.Div([
 html.Div([
 html.H4('Select Timeframe'),
 dcc.Dropdown(
 id='timeframe_dropdown',
 options=[{'label': i, 'value': i} for i in timeframe],
 value = time_default
 ),
 ],
 style={'width': '48%', 'display': 'inline-block'}),
 dcc.Graph(id='heatmap', 
 figure = go.Figure({
 'data': [go.Heatmap(
 x=film_heat_default['Production Company'],
 y=film_heat_default['Release Year'],
 z=film_heat_default['Locations'],
 name = 'first legend group',
 hoverongaps = False,
 colorscale='Viridis')],
 'layout': go.Layout(
 xaxis = dict(title = 'Production Company'),
 yaxis = dict( title = 'Year')
 )})        
 )
 ]),
 html.H2('Collaborations Between Actors in San Francisco (Post 2000)'),     
 dcc.Graph(id='arc_diagram', 
 figure = arc_fig       
 ),
html.Div([
 html.Div([
 html.H4('Select Year'),  
dcc.Slider(
        id='year-slider',
        min= film_slider['Release Year'].min(),
        max=film_slider['Release Year'].max(),
        value=initial_year_value,
        marks={str(day): str(day) for day in film_slider['Release Year'].unique()},
        step=None
     )    
 ]),]),])


@app.callback(
    dash.dependencies.Output('heatmap','figure'),
    [dash.dependencies.Input('timeframe_dropdown', 'value')]
)
def update_graph(input_value):
    app.logger.info(input_value)
    heatmap_data = film_heat[(film_heat['Time Period'] == input_value)]
    #print(heatmap_data)
    #heatmap_data = pd.merge(data, heatmap,check, on=['weekday', 'hour'],how='outer').fillna(0)
    print (input_value)
    max = heatmap_data[heatmap_data['Locations']==heatmap_data['Locations'].max()]
    max = max.reset_index()

    figure = go.Figure({
     'data': [go.Heatmap(
     x=heatmap_data['Production Company'],
     y=heatmap_data['Release Year'],
     z=heatmap_data['Locations'],
     hoverongaps = False,
     colorscale='Viridis')],
     'layout': go.Layout(
     xaxis = dict(title = 'Production Company'),
     yaxis = dict( title = 'Year')
     )
        
     })
    figure.update_xaxes(
    tickangle=45,
    ticktext=heatmap_data['PC'].tolist(),
    tickvals=heatmap_data['Production Company'].tolist(),
)
    return figure


@app.callback(
    dash.dependencies.Output('arc_diagram','figure'),
    [dash.dependencies.Input('year-slider', 'value')]
)
def update_graph_2(input_value):
    app.logger.info(input_value)
    arc_data=film_final_int[(film_final_int['Release Year'] == input_value)]
    print(input_value)
    print(arc_data)
    
    

    film_json_string = arc_data.to_json(orient='records')
    film_json = json.loads(film_json_string)
    edges = [(item['Actor 1'], item['Actor 2'])  for item in film_json]
    interact_strength = [item['Links'] for item in film_json]
    keys = sorted(set(interact_strength)) 
    actors1 = arc_data[["Actor 1","Links"]]
    actors2 = arc_data[["Actor 2","Links"]]
    actors2 = actors2.rename(columns = {'Actor 2':'Actor 1'})
    actors = pd.concat([actors1, actors2])
    actors = actors.groupby(["Actor 1"]).sum().reset_index()
    node_data = []
    for index, rows in actors.iterrows():
        temp_list =[rows['Actor 1'], rows['Links']] 
        node_data.append(temp_list)
    values = [item[1] for item in node_data]
    L = len(set(arc_data['Actor 1'].tolist() + arc_data['Actor 2'].tolist()))
    labels = []
    labels = [list[0] for list in node_data]
    widths = [2+k*1 for k in range(25)]#+ [5+k*0.25 for k in range(8)]+[9+k*0.25 for k in range(7)]
    d = dict(zip(keys, widths))  
    nwidths = [d[val] for val in interact_strength] 
    data = []
    tooltips = [] #list of strings to be displayed when hovering the mouse over the middle of the circle arcs
    xx = []
    yy = []
    hover_text = [f'{labels[k]}, {values[k]} collaborations' for k in range(L)]
    node_trace = dict(type='scatter',
                      x=list(range(L)),
                      y=[0]*L,
                      mode='markers',
                      marker=dict(size=12, 
                                  color=values, 
                                  colorscale=pl_density,
                                  showscale=False,
                                  line=dict(color='rgb(50,50,50)', width=0.75)),
                      text=hover_text,
                      hoverinfo='text')
    X = list(range(L)) # node x-coordinates
    nr = 75 
    for i, (j, k) in enumerate(edges):
        if labels.index(j) < labels.index(k):
            tooltips.append('interactions(' + j + ', ' + k + ')=' + str(interact_strength[i]))
        else:
            tooltips.append('interactions(' + k + ', ' + j + ')=' + str(interact_strength[i]))
        b0 = [X[labels.index(j)], 0.0]
        b2 = [X[labels.index(k)], 0.0]
        b1 = get_b1(b0, b2)
        a = dim_plus_1([b0, b1, b2], [1, 0.5, 1])
        pts = Rational_Bezier_curve(a, nr)
        xx.append(pts[nr//2][0]) #abscissa of the middle point on the computed arc
        yy.append(pts[nr//2][1]) #ordinate of the same point
        x,y = zip(*pts)
        
        data.append(dict(type='scatter',
                         x=x, 
                         y=y, 
                         name='',
                         mode='lines', 
                         line=dict(width=nwidths[i], color='#6b8aca', shape='spline'),
                         hoverinfo='none'
                        )
                    )
    data.append(dict(type='scatter',
                     x=xx,
                     y=yy,
                     name='',
                     mode='markers',
                     marker=dict(size=0.5, color='#a0b6e8'),
                     text=tooltips,
                     hoverinfo='text'))
    data.append(node_trace)
    title = "(Hover on Tips of Arcs for Interaction Counts)"
    layout = dict(
             title=title, 
             font=dict(size=10), 
             width=1500,
             height=600,
             showlegend=False,
             xaxis=dict(anchor='y',
                        showline=False,  
                        zeroline=False,
                        showgrid=False,
                        tickvals=list(range(len(labels))), 
                        ticktext=labels,
                        tickangle=50,
                        ),
             yaxis=dict(visible=False), 
             hovermode='closest',
             margin=dict(t=80, b=110, l=10, r=10),
             annotations=[dict(showarrow=False, 
                               text='',
                               xref='paper',     
                               yref='paper',     
                               x=0.05,  
                               y=-0.3,  
                               xanchor='left',   
                               yanchor='bottom',  
                               font=dict(size=11 ))
                                      ]
                     
               
        )
    arc_fig = go.FigureWidget(data=data, layout=layout)
    return arc_fig

app.run_server(debug=False)

