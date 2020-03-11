
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from data_preprocessing import *
from sklearn import preprocessing
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns

import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objects import *

from data_preprocessing import *
import matplotlib.pyplot as plt




def ScatterPlot(data, method, alc, x_column, y_column):
    header = data.columns
    #n_max = 8
    #n_feature = 2
    X_header = header[0:26].append(header[28:len(header)])

    # X_selected = select_first_n(data_revised, X_header, y_header[0], n_max)

    X = data[X_header]
    # print(data.shape)

    X_encoded = encode(X)
    X_scaled = StandardScaler().fit_transform(X_encoded)

    data_TSNE = TSNE(n_components=2).fit_transform(X_scaled)
    TSNE_x = data_TSNE[:, 0]
    TSNE_y = data_TSNE[:, 1]

    data_PCA = PCA(n_components=2).fit_transform(X_scaled)
    PCA_x = data_PCA[:, 0]
    PCA_y = data_PCA[:, 1]

    data = data.assign(TSNE_x=TSNE_x)
    data = data.assign(TSNE_y=TSNE_y)
    data = data.assign(PCA_x=PCA_x)
    data = data.assign(PCA_y=PCA_y)



    colorscale = ['rgb(255, 223, 61)', 'rgb(235, 168, 36)', 'rgb(194, 127, 0)', 'rgb(153, 86, 0)', 'rgb(113, 46, 0)']

    if method == 'T-SNE':
        x_label = 'TSNE_x'
        y_label = 'TSNE_y'
    elif method == 'PCA':
        x_label = 'PCA_x'
        y_label = 'PCA_y'
    else:
        x_label = x_column
        y_label = y_column

    traces = []
    alc_list = data[alc].unique().tolist()
    alc_list.sort()

    for i in alc_list:
        data_by_alc = data[data[alc] == i]
        traces.append(dict(
                x=data_by_alc[x_label],
                y=data_by_alc[y_label],
                #text=data_by_alc['continent'],
                mode='markers',
                opacity=0.5,
                marker={
                    'size': 15,
                    #'line': {'width': 0.5, 'color': 'white'},
                    'color': colorscale[i-1]
                },
                name=i))

    return [{
        'data': traces,
        'layout': dict(
            xaxis={'title': x_label, 'autorange': True},
            yaxis={'title': y_label,  'autorange': True},
            font={'size': 14, 'family': 'Courier New, monospace', 'color': 'rgba(245, 240, 214, 1)'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            autosize=False,
            width=900,
            height=500,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)'
        )
    }]