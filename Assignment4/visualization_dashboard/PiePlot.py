import plotly.express as px
def PiePlot(data, hoverData, feature, cate, dict_features):
    print(hoverData)
    gp = data.groupby([feature, cate])
    name = hoverData['points'][0]['x']
    new_gp = gp.size().reset_index(name='counts')
    new_gp = new_gp.loc[new_gp[feature] == name]
    new_gp = new_gp.sort_values(by = [cate])
    print(new_gp)
    colorscale = ['rgb(255, 223, 61)','rgb(235, 168, 36)', 'rgb(194, 127, 0)', 'rgb(153, 86, 0)', 'rgb(113, 46, 0)']
    fig = px.pie(new_gp, values = 'counts', names = cate, color = cate, color_discrete_sequence=colorscale)
    fig.update_layout(
                      title = 'Components of \'' + str(name) + '\' in \'' + dict_features[feature] + '\':',
                      font = {'size': 14, 'family': 'Courier New, monospace', 'color':'rgba(245, 240, 214, 1)'},
                      hovermode='closest',
                      showlegend=False
                      )
    fig.update_layout(
        autosize = False,
        width = 800,
        height = 500,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    return fig
