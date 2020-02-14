
import plotly.graph_objects as go
from selection_first_n import selection_first_n



def ParallelCoordinate(data, cate, feature_list, dict_features):
    n_features = 31
    selected_header = selection_first_n(data, feature_list, cate, n_features)


    dimensions = [go.parcats.Dimension(
                values = data[cate],
                categoryorder = 'array',
                categoryarray = sorted(data[cate].unique()),
                label = dict_features[cate])]

    for feature in selected_header:
        if data[feature].dtypes == 'object':
            dimensions.append(go.parcats.Dimension(
                values = data[feature],
                categoryorder = 'category ascending', label = dict_features[feature]))
        else:
            dimensions.append(go.parcats.Dimension(
                values = data[feature],
                categoryorder = 'array',
                categoryarray = sorted(data[feature].unique()),
                label = dict_features[feature]))

    color = data[cate]
    colorscale = ['rgb(255, 223, 61)','rgb(235, 168, 36)', 'rgb(194, 127, 0)', 'rgb(153, 86, 0)', 'rgb(113, 46, 0)']

    fig = go.Figure(
        data = [go.Parcats(dimensions = dimensions,
                            line = {'color': color, 'colorscale': colorscale, 'showscale': False},
                            labelfont={'size': 14, 'family': 'Courier New, monospace', 'color':'rgba(245, 240, 214, 1)'},
                            tickfont={'size': 14, 'family': 'Courier New, monospace', 'color':'rgba(245, 240, 214, 1)'}
                           )]
    )


    fig.update_layout(
        autosize = False,
        width = n_features * 220,
        height = 800,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    return fig
