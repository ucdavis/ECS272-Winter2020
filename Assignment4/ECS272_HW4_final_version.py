# ECS 272 HW3 2020 Winter Quarter
# Hang Su and Xuerui Li

# Import packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

'''K-means clustering preparation'''


# size = 30  ##取值范围

##计算欧式距离
def distEuclid(x, y):
    return np.sqrt(np.sum((x - y) ** 2))


## 初始化簇中心点 一开始随机从样本中选择k个 当做各类簇的中心
def initCentroid(data, k):
    #    num, dim = data.shape
    centpoint = np.zeros((k, 3))
    l = [x for x in range(721)]
    np.random.shuffle(l)
    for i in range(k):
        index = int(l[i])
        centpoint[i] = data[index]
    return centpoint


##进行KMeans分类
def KMeans(data, k):
    ##样本个数
    num = np.shape(data)[0]

    ##记录各样本 簇信息 0:属于哪个簇 1:距离该簇中心点距离
    cluster = np.zeros((num, 2))
    cluster[:, 0] = -1

    ##记录是否有样本改变簇分类
    change = True
    ##初始化各簇中心点
    cp = initCentroid(data, k)

    while change:
        change = False

        ##遍历每一个样本
        for i in range(num):
            minDist = 100
            minIndex = -1

            ##计算该样本距离每一个簇中心点的距离 找到距离最近的中心点
            for j in range(k):
                dis = distEuclid(cp[j], data[i])
                if dis < minDist:
                    minDist = dis
                    minIndex = j

            ##如果找到的簇中心点非当前簇 则改变该样本的簇分类
            if cluster[i, 0] != minIndex:
                change = True
                cluster[i, :] = minIndex, minDist

        ## 根据样本重新分类  计算新的簇中心点
        for j in range(k):
            pointincluster = data[[x for x in range(num) if cluster[x, 0] == j]]
            cp[j] = np.mean(pointincluster, axis=0)

    print("finish!")
    return cp, cluster


##展示结果  各类簇使用不同的颜色  中心点使用X表示
def Show(data, k, cp, cluster):
    color = ['r', 'g', 'b', 'c', 'y', 'm', 'k']
    ax = plt.subplot(111, projection='3d')
    for i in range(721):
        mark = int(cluster[i, 0])
        ax.scatter(data[i, 0], data[i, 1], data[i, 2], c=color[mark])

    for i in range(k):
        ax.scatter(cp[i, 0], cp[i, 1], cp[i, 2], c=color[i], marker='x')

    plt.show()


# Import data
df = pd.read_csv('pokemon_dataset_revised.csv')

# Process and prepare data for future plot (k-means and parallel coordinates)
data = np.zeros((721, 3))


def get_max_value(martix):
    res_list = []
    for j in range(721):
        one_list = []
        for i in range(2):
            one_list.append(int(martix[j][i]))
        res_list.append(str(max(one_list)))
    return res_list


martix = np.zeros((721, 2))
martix[:, 0] = df['Attack']
martix[:, 1] = df['Sp_Atk']
data[:, 0] = get_max_value(martix)
data[:, 1] = np.multiply(np.array(df['HP']), np.array(df['Defense']), np.array(df['Sp_Def'])) / 100
data[:, 2] = df['Speed']

df['Backup1'] = data[:, 0]
df['Backup2'] = data[:, 1]
df['Backup3'] = data[:, 2]

# cp, cluster = KMeans(data, k)
#
# df['Backup4'] = cluster[:, 0]
#
df['Backup5'] = np.trunc(df['Backup1'] / 10)
df['Backup6'] = np.trunc(df['Backup2'] / 10)
df['Backup7'] = np.trunc(df['Backup3'] / 10)

cp, cluster4 = KMeans(data, 4)
df['Backup11'] = cluster4[:, 0]

cp, cluster5 = KMeans(data, 5)
df['Backup12'] = cluster5[:, 0]

cp, cluster6 = KMeans(data, 6)
df['Backup13'] = cluster6[:, 0]

cp, cluster7 = KMeans(data, 7)
df['Backup14'] = cluster7[:, 0]

cp, cluster8 = KMeans(data, 8)
df['Backup15'] = cluster8[:, 0]

'''preparation for parallel coordinates'''
color_dict = {}
count = 0
for i in df['Generation']:
    color_dict[i] = count
    count += 5
color_code = []
for i in df['Generation']:
    color_code.append(color_dict[i])
df['Generation'] = color_code

week_dict = {}
count = 0
for i in df['Backup5'].unique():
    week_dict[i] = count
    count += 5
week_code = []
for i in df['Backup5']:
    week_code.append(week_dict[i])
df['Backup5'] = week_code

pd_dict = {}
count = 0
for i in df['Backup6'].unique():
    pd_dict[i] = count
    count += 5
pd_code = []
for i in df['Backup6']:
    pd_code.append(pd_dict[i])
df['Backup6'] = pd_code
# print(df['Backup6'].min())
res_dict = {}
count = 0
for i in df['Backup7'].unique():
    res_dict[i] = count
    count += 5
res_code = []
for i in df['Backup7']:
    res_code.append(res_dict[i])
df['Backup7'] = res_code
# print(df['Backup7'])
catch_dict = {}
count = 0
for i in df['Catch_Rate'].unique():
    catch_dict[i] = count
    count += 5
catch_code = []
for i in df['Catch_Rate']:
    catch_code.append(catch_dict[i])
df['Backup8'] = catch_code
# print(df['Catch_Rate'].max())
usage_dict = {}
count = 0
for i in df['Usage'].unique():
    usage_dict[i] = count
    count += 5
usage_code = []
for i in df['Usage']:
    usage_code.append(usage_dict[i])
df['Usage'] = usage_code

# Options for first two dropdown menu
available_indicators_overview = ['Total_mean', 'Number']
available_indicators_detail = ['Catch_Rate', 'Height_m', 'Weight_kg', 'HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def',
                               'Speed']

app.layout = html.Div([
    html.Div([
        html.Div(children=[
            html.Img(
                src='https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3%A9mon_logo.svg/1920px-International_Pok%C3%A9mon_logo.svg.png',
                style={
                    'height': '10%',
                    'width': '10%',
                    'text-align': 'right',
                    'padding-top': '0px',
                    'padding-left': '5%',
                    'float': 'left'

                },
            ), ]),
        html.Div(children=[
            html.Img(
                src='https://upload.wikimedia.org/wikipedia/en/a/a6/Pok%C3%A9mon_Pikachu_art.png',
                style={
                    'height': '10%',
                    'width': '10%',
                    'text-align': 'right',
                    'padding-top': '0px',
                    'padding-left': '5%',
                    'float': 'right'

                },
            ), ]),
        html.Div(children='ECS 272 HW4: Pokemon dataset visualization',
                 style={'text-align': 'center',
                        'color': 'black',
                        'font-family': 'FreeMono, monospace',
                        'font-size': '50px',
                        'width': '75%',
                        'padding-top': '100px',
                        'margin': 'auto',
                        'padding-bottom': '20px',
                        }),
        html.Div(children='Group member: Xuerui Li & Hang Su',
                 style={'text-align': 'center',
                        'color': 'black',
                        'font-family': 'FreeMono, monospace',
                        'font-size': '20px',
                        'width': '60%',
                        'padding-top': '100px',
                        'margin': 'auto',
                        'padding-bottom': '50px',
                        }),
        html.Div(children='1. Overview and detailed view',
                 style={  # 'text-align': 'center',
                     'color': 'black',
                     'font-family': 'FreeMono, monospace',
                     'font-size': '30px',
                     'width': '30%',
                     'padding-top': '100px',
                     'margin-left': '10%',
                     'margin-right': '50%',
                     'padding-bottom': '50px',
                 }),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Markdown('''
                ###### Overview parameters
                '''),
                    dcc.Dropdown(
                        id='choose_overview',
                        options=[{'label': i, 'value': i} for i in available_indicators_overview],
                        value='Total_mean'
                    )
                ],
                    style={'width': '20%', 'display': 'inline-block', 'font-family': 'FreeMono, monospace', }
                ),

                html.Div([
                    dcc.Markdown('''
                ###### Detailed parameters
                '''),
                    dcc.Dropdown(
                        id='choose_detail',
                        options=[{'label': i, 'value': i} for i in available_indicators_detail],
                        value='Catch_Rate'
                    )
                ],
                    style={'width': '20%', 'float': 'right', 'display': 'inline-block',
                           'font-family': 'FreeMono, monospace'}
                ),
            ], style={'borderBottom': 'thin lightgrey solid',
                      'backgroundColor': 'rgb(250, 250, 250)',
                      'padding': '10px 5px'}),

            html.Div([
                dcc.Graph(
                    id='overview',
                    hoverData={'points': [{'customdata': 'Grass'}]}
                )
            ],
                style={'width': '60%', 'display': 'inline-block', 'margin': 'auto'}
            ),

            html.Div([
                dcc.Graph(id='detail')
            ],
                style={'width': '40%', 'display': 'inline-block', 'margin': 'auto'}),
        ], style={'width': '80%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}, ),
        html.Div(children='2. K-means clustering view',
                 style={  # 'text-align': 'center',
                     'color': 'black',
                     'font-family': 'FreeMono, monospace',
                     'font-size': '30px',
                     'width': '30%',
                     'padding-top': '100px',
                     'margin-left': '10%',
                     'margin-right': '50%',
                     'padding-bottom': '50px',
                 }),
        html.Div([
            html.Div([
                dcc.Graph(id='graph-with-slider'),
            ]),
            html.Div([
                dcc.Markdown('''
                ###### Value of K:
                '''),
            ], style={'width': '20%', 'margin-left': 'auto', 'margin-right': 'auto',
                      'font-family': 'FreeMono, monospace',
                      }),
            html.Div([
                dcc.Slider(
                    id='year-slider',
                    min=4,
                    max=8,
                    value=6,  # df['year'].min(),
                    marks={str(i): str(i) for i in range(4, 9)},
                    step=None
                )
            ], style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),

        ], style={'width': '80%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto',
                  'margin-bottom': 'auto', 'font-family': 'FreeMono, monospace'}

        )

    ]),
    html.Div(children='3. Parallel coordinates view',
             style={  # 'text-align': 'center',
                 'color': 'black',
                 'font-family': 'FreeMono, monospace',
                 'font-size': '30px',
                 'width': '30%',
                 'padding-top': '100px',
                 'margin-left': '10%',
                 'margin-right': '50%',
                 'padding-bottom': '50px',
             }),
    html.Div([
        html.Div([
            dcc.Markdown('''
                ###### Theme
                '''),
            dcc.Dropdown(
                id='parallel-color-change',
                options=[
                    {'label': 'Earth Colorscale', 'value': 'Earth'},
                    {'label': 'Picnic Colorscale', 'value': 'Picnic'},
                    {'label': 'Blackbody Colorscale', 'value': 'Blackbody'},
                    {'label': 'Electric Colorscale', 'value': 'electric'}
                ],
                value='electric'
            ),

        ], style={'width': '20%', 'margin-left': '10%', 'borderBottom': 'thin lightgrey solid',
                  'backgroundColor': 'rgb(250, 250, 250)',
                  'padding': '10px 5px', 'font-family': 'FreeMono, monospace'}),
        html.Div([
            dcc.Graph(id='parallel-coordinate'),
        ], style={'width': '80%', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}, ),

    ]),
    html.Div(children=[
        html.Img(
            src='https://upload.wikimedia.org/wikipedia/en/a/a5/Pok%C3%A9mon_Charmander_art.png',
            style={
                'height': '10%',
                'width': '10%',
                'text-align': 'right',
                'padding-top': '0px',
                'padding-left': '5%',
                'float': 'left'

            },
        ), ]),
    html.Div(children=[
        html.Img(
            src='https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png',
            style={
                'height': '10%',
                'width': '10%',
                'text-align': 'right',
                'padding-top': '0px',
                'padding-left': '5%',
                'float': 'right'

            },
        ), ]),
])


# Define overview figure
@app.callback(
    Output('overview', 'figure'),
    [Input('choose_overview', 'value')])
def update_figure(choose_overview):
    kind = df['Type_1'].unique()
    N = []
    M = []
    S = []
    for t in kind:
        dff = df[df['Type_1'] == t]
        row = dff.shape[0]
        N.append(row)
        average = dff['Total'].mean()
        s = dff['Total'].sum()
        M.append(average)
        S.append(s)
    # ['Total_mean', 'Total_sum', 'Number']
    data_overview = {'Total_mean': M, 'Total_sum': S, 'Number': N}
    df_overview = pd.DataFrame(data_overview)

    return {
        'data': [{'x': kind, 'y': df_overview[choose_overview], 'type': 'bar',
                  'customdata': kind, 'name': choose_overview}],
        'layout': dict(
            # xaxis={'type': 'linear', 'title': 'Total'},
            yaxis={'title': choose_overview},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            # legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


def create_sub(x1, y1, ylabel, text, ty):
    return {
        'data': [dict(
            x=x1,
            y=y1,
            text=text,
            # customdata=kind,
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.7,
                'color': 'rgb(234, 220, 39)',
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={'type': 'linear', 'title': 'Total', 'font-family': 'FreeMono, monospace'},
            yaxis={'title': ylabel},
            title=ty,
            # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            # legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


@app.callback(
    Output('detail', 'figure'),
    [Input('overview', 'hoverData'),
     Input('choose_detail', 'value')])
def update_hover_data(hoverData, choose_detail):
    pokemon_type = hoverData['points'][0]['customdata']
    df_type = df[df['Type_1'] == pokemon_type]
    x = df_type['Total']
    y = df_type[choose_detail]
    title = choose_detail
    text1 = df_type['Name']
    text2 = pokemon_type

    return create_sub(x, y, title, text1, text2)


# Define k-means return figure
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    if selected_year == 4:
        df['Backup20'] = df['Backup11']
    elif selected_year == 5:
        df['Backup20'] = df['Backup12']
    elif selected_year == 6:
        df['Backup20'] = df['Backup13']
    elif selected_year == 7:
        df['Backup20'] = df['Backup14']
    else:
        df['Backup20'] = df['Backup15']

    filtered_df = df
    traces = []
    for kk in df.Backup20.unique():
        df_by_continent = filtered_df
        traces.append(dict(
            x=df[df['Backup20'] == kk]['Backup1'],
            y=df[df['Backup20'] == kk]['Backup2'],
            text=df[df['Backup20'] == kk]['Name'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=kk
        )
        )

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Attack',
                   'range': [0, 200]},
            yaxis={'title': 'Defense', 'range': [0, 200]},
            height=800,
            # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition={'duration': 500},
        )
    }


# define parallel coordinates
@app.callback(
    Output('parallel-coordinate', 'figure'),
    [Input('parallel-color-change', 'value')])
def update_parallel_figure(selected_color):
    week_text = [i for i in week_dict]
    week_vals = [week_dict[i] for i in week_text]
    week_text.sort()

    pd_text = [i for i in pd_dict]
    pd_vals = [pd_dict[i] for i in pd_text]
    pd_text.sort()

    res_text = [i for i in res_dict]
    res_vals = [res_dict[i] for i in res_text]
    res_text.sort()

    color_text = [i for i in color_dict]
    color_vals = [color_dict[i] for i in color_text]
    color_text.sort()

    catch_text = [i for i in catch_dict]
    catch_vals = [catch_dict[i] for i in catch_text]
    catch_text.sort()

    usage_text = [i for i in usage_dict]
    usage_vals = [usage_dict[i] for i in usage_text]
    usage_text.sort(reverse=True)
    # print(catch_vals)
    # print(catch_text)

    fig = go.Figure(
        data=go.Parcoords(
            line=dict(
                color=df['Generation'],
                colorscale=selected_color,
                showscale=True,
                cmin=min(color_code),
                cmax=max(color_code),
                colorbar=dict(
                    tickvals=color_vals,
                    ticktext=color_text
                )
            ),
            dimensions=list([
                dict(
                    range=[df['Backup5'].min(), df['Backup5'].max()],
                    tickvals=week_vals,
                    ticktext=week_text,
                    label='Calculated Attack', values=df['Backup5']
                ),
                dict(
                    range=[df['Backup6'].min(), df['Backup6'].max()],
                    tickvals=pd_vals,
                    ticktext=pd_text,
                    label='Calculated Defense', values=df['Backup6']
                ),
                dict(
                    range=[df['Backup7'].min(), df['Backup7'].max()],
                    tickvals=res_vals,
                    ticktext=res_text,
                    label='Speed', values=df['Backup7']
                ),
                dict(
                    range=[df['Backup8'].min(), df['Backup8'].max()],
                    tickvals=catch_vals,
                    ticktext=catch_text,
                    label='Catch Rate', values=df['Backup8']
                ),
                dict(
                    range=[1, df['Usage'].max()],
                    tickvals=usage_vals,
                    ticktext=usage_text,
                    label='Usage Ranking', values=df['Usage']
                )])
        )
    )

    fig.update_layout(
        autosize=False,
        # width=n_features * 220,
        height=800,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
