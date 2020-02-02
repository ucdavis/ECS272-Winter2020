# Get this figure: fig = py.get_figure("https://plot.ly/~ep8/12/")
# Get this figure's data: data = py.get_figure("https://plot.ly/~ep8/12/").get_data()
# Add data to this figure: py.plot(Data([Scatter(x=[1, 2], y=[2, 3])]), filename ="plot from API (1)", fileopt="extend")
# Get y data of first trace: y1 = py.get_figure("https://plot.ly/~ep8/12/").get_data()[0]["y"]

# Get figure documentation: https://plot.ly/python/get-requests/
# Add data documentation: https://plot.ly/python/file-options/

# If you're using unicode in your file, you may need to specify the encoding.
# You can reproduce this figure in Python with the following code!

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import chart_studio.plotly as py
from plotly.graph_objs import *
py.sign_in('xtzou', 'Ff1sRZNG4Kto0ySvGkhU')
trace1 = {
  "fill": "tonexty", 
  "line": {
    "color": "#cdcdd8", 
    "shape": "spline", 
    "width": 0
  }, 
  "name": "", 
  "type": "scatter", 
  "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
  "y": [0.0, -1.145, -1.155, -1.4224999999999999, -1.2959999999999998, -1.369, -1.1315, -1.3175000000000001, -1.203, -1.1099999999999999, -1.5165, -1.008, -1.005], 
  "fillcolor": "#cdcdd8"
}
trace2 = {
  "fill": "tonexty", 
  "line": {
    "color": "#0202ef", 
    "shape": "spline", 
    "width": 0
  }, 
  "name": "", 
  "type": "scatter", 
  "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
  "y": [0.0, -0.891, -0.885, -1.1885, -1.0709999999999997, -1.108, -0.8345, -1.0205000000000002, -0.9500000000000001, -0.9129999999999998, -1.2834999999999999, -0.8109999999999999, -0.833], 
  "fillcolor": "#0202ef"
}
trace3 = {
  "fill": "tonexty", 
  "line": {
    "color": "#8f8ff7", 
    "shape": "spline", 
    "width": 0
  }, 
  "name": "", 
  "type": "scatter", 
  "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
  "y": [0.0, -0.637, -0.63, -0.9364999999999999, -0.8329999999999997, -0.8720000000000001, -0.5455000000000001, -0.8065000000000002, -0.7030000000000001, -0.6549999999999998, -1.0044999999999997, -0.5569999999999999, -0.5249999999999999], 
  "fillcolor": "#8f8ff7"
}
trace4 = {
  "fill": "tonexty", 
  "line": {
    "color": "#f7960e", 
    "shape": "spline", 
    "width": 0
  }, 
  "name": "", 
  "type": "scatter", 
  "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
  "y": [0.0, -0.42700000000000005, -0.401, -0.7234999999999999, -0.5689999999999997, -0.6120000000000001, -0.3035000000000001, -0.5775000000000002, -0.4640000000000001, -0.4219999999999998, -0.7714999999999997, -0.38199999999999995, -0.30299999999999994], 
  "fillcolor": "#f7960e"
}
trace5 = {
  "fill": "tonexty", 
  "line": {
    "color": "#f2c382", 
    "shape": "spline", 
    "width": 0
  }, 
  "name": "", 
  "type": "scatter", 
  "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
  "y": [0.0, -0.21700000000000005, -0.17, -0.5195, -0.3119999999999997, -0.3490000000000001, -0.06150000000000011, -0.36750000000000027, -0.2290000000000001, -0.1629999999999998, -0.4924999999999997, -0.15499999999999994, -0.009999999999999953], 
  "fillcolor": "#f2c382"
}
trace6 = {
  "fill": "tonexty", 
  "line": {
    "color": "#f21602", 
    "shape": "spline", 
    "width": 0
  }, 
  "name": "", 
  "type": "scatter", 
  "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
  "y": [0.0, 0.020999999999999935, 0.064, -0.14449999999999996, -0.023999999999999744, -0.0500000000000001, 0.1574999999999999, -0.028500000000000247, 0.020999999999999908, 0.033000000000000196, -0.1774999999999997, 0.01600000000000007, 0.14400000000000004], 
  "fillcolor": "#f21602"
}
trace7 = {
  "fill": "tonexty", 
  "line": {
    "color": "#edbdb8", 
    "shape": "spline", 
    "width": 0
  }, 
  "name": "", 
  "type": "scatter", 
  "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
  "y": [0.0, 0.2769999999999999, 0.319, 0.28250000000000003, 0.29900000000000027, 0.2879999999999999, 0.39249999999999985, 0.35649999999999976, 0.29399999999999993, 0.2430000000000002, 0.16850000000000026, 0.19300000000000006, 0.31100000000000005], 
  "fillcolor": "#edbdb8"
}
trace8 = {
  "fill": "tonexty", 
  "line": {
    "color": "#25b8f7", 
    "shape": "spline", 
    "width": 0
  }, 
  "name": "", 
  "type": "scatter", 
  "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
  "y": [0.0, 0.4509999999999999, 0.581, 0.6905, 0.6200000000000003, 0.5839999999999999, 0.6214999999999998, 0.6344999999999998, 0.567, 0.43800000000000017, 0.5755000000000002, 0.3640000000000001, 0.45600000000000007], 
  "fillcolor": "#25b8f7"
}
trace9 = {
  "fill": "tonexty", 
  "line": {
    "color": "#b7e4f7", 
    "shape": "spline", 
    "width": 0
  }, 
  "name": "CBS", 
  "type": "scatter", 
  "x": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
  "y": [0.0, 0.6249999999999999, 0.871, 1.1675, 0.9850000000000003, 0.9219999999999999, 0.8674999999999998, 0.9404999999999999, 0.867, 0.6450000000000001, 1.0445000000000002, 0.5410000000000001, 0.6080000000000001], 
  "fillcolor": "#b7e4f7"
}
data = Data([trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9])
layout = {
  "title": "Streamgraph with minimized wiggle <a href='http://leebyron.com/streamgraph/stackedgraphs_byron_wattenberg.pdf'> [1]</a>", 
  "width": 900, 
  "xaxis": {
    "ticks": "outside", 
    "mirror": True, 
    "ticklen": 5, 
    "showgrid": False, 
    "showline": True, 
    "tickfont": {
      "size": 11, 
      "color": "rgb(107, 107, 107)"
    }, 
    "tickwidth": 1, 
    "showticklabels": True
  }, 
  "yaxis": {
    "ticks": "outside", 
    "title": "", 
    "mirror": True, 
    "ticklen": 5, 
    "showgrid": False, 
    "showline": True, 
    "tickfont": {
      "size": 11, 
      "color": "rgb(107, 107, 107)"
    }, 
    "zeroline": True, 
    "tickwidth": 1, 
    "showticklabels": True
  }, 
  "height": 460, 
  "margin": {
    "b": 60, 
    "l": 60, 
    "r": 60, 
    "t": 80
  }, 
  "autosize": False, 
  "hovermode": "x", 
  "showlegend": False, 
  "annotations": [
    {
      "x": 0, 
      "y": -0.13, 
      "font": {"size": 12}, 
      "text": "Brier Score data", 
      "xref": "paper", 
      "yref": "paper", 
      "xanchor": "left", 
      "yanchor": "bottom", 
      "showarrow": False
    }
  ]
}
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)