import plotly.graph_objects as go
import plotly.express as px

def BarPlot(data, cate, feature, dict_features):
    gp = data.groupby([feature, cate])
    new_gp = gp.size().reset_index(name='counts')
    colorscale = ['rgb(255, 223, 61)','rgb(235, 168, 36)', 'rgb(194, 127, 0)', 'rgb(153, 86, 0)', 'rgb(113, 46, 0)']

    fig = px.bar(new_gp, x = feature, y = 'counts', color = cate, color_continuous_scale=colorscale)
    fig.update_layout(
                      xaxis_title = dict_features[feature],
                      yaxis_title = 'Number of students',
                      font = {'size': 14, 'family': 'Courier New, monospace', 'color':'rgba(245, 240, 214, 1)'},
                      hovermode='closest'
                      )

    fig.update_layout(coloraxis_colorbar=dict(
        title=dict_features[cate],
        dtick=1
    ))

    fig.update_layout(
        autosize = False,
        width = 800,
        height = 500,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    return fig