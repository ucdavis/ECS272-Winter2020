import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
import numpy as np

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
names_file = './young-people-survey/columns.csv'
responses_file = './young-people-survey/responses.csv'
name_data = pd.read_csv(names_file)
response_data = pd.read_csv(responses_file)
# remove rows with na
response_data = response_data.dropna()
names = name_data['short']
enjoy_music = names[0]
music_cols = names[1:19]
enjoy_movie = names[19]
movie_cols = names[20:31]
hobbies_cols = names[31:63]
phobia_cols = names[63:73]
health_cols = names[73:76]
personality_cols = names[76:133]
spending_cols = names[133:140]
demographic_cols = names[140:150]

app.layout = html.Div([
    html.H1("Education Level Distribution(Grew up in village/town)", style={"textAlign": "center"}),
    html.Div([
        html.H6("Select maximum age of interest", style={"textAlign": "center"}),
        dcc.Slider(
            id='age_slider',
            min=response_data['Age'].min(),
            max=response_data['Age'].max(),
            value=response_data['Age'].max(),
            marks={
                '15': {'label': '15'},
                '16': {'label': '16'},
                '17': {'label': '17'},
                '18': {'label': '18'},
                '19': {'label': '19'},
                '20': {'label': '20'},
                '21': {'label': '21'},
                '22': {'label': '22'},
                '23': {'label': '23'},
                '24': {'label': '24'},
                '25': {'label': '25'},
                '26': {'label': '26'},
                '27': {'label': '27'},
                '28': {'label': '28'},
                '29': {'label': '29'},
                '30': {'label': '30'}
            },
            step=None,
        )
    ]),
    html.H5("Hover over bar to see Principle Component Analysis of village/town and the sankey graph of "
            "village/town", style=({"textAlign": "center"})),
    dcc.Graph(id='education_bar'),
    html.Div([
        html.Div([
            html.H5('Principal Component Analysis: Select Question of Interest', style=({"textAlign": "center"})),
            dcc.Dropdown(
                id='pca_dropdown',
                options=[
                    {'label': 'Movie Preference and its relation to preference for outdoor activity', 'value': 'movie'},
                    {'label': 'Age and its relation to spending habits', 'value': 'age'},
                    # {'label': 'Music Preference and its relation to', 'value': 'music'},
                    {'label': 'Phobia and its relation to Hypochondria', 'value': 'phobia'}
                ],
                value='phobia',
                style=({"textAlign": "center"})
            ),
            dcc.Graph(id='pca_scatter')
        ], className="six columns"),
        html.Div([
            html.H5('Sankey graph', style=({"textAlign": "center"})),
            dcc.Graph(id='sankey')
        ], className="six columns")
    ], className="row")
])


@app.callback(
    Output('education_bar', 'figure'),
    [Input('age_slider', 'value')]
)
def update_education_bar(input_age):
    filtereddata = response_data[response_data.Age <= input_age]
    possible_education = filtereddata.Education.unique()
    # group by education level then count village/town
    count = filtereddata.groupby(['Education', 'Village - town']).size().unstack()
    # print(count)
    village = count['village']
    town = count['city']
    trace1 = go.Bar(x=possible_education, y=village, name='village')
    trace2 = go.Bar(x=possible_education, y=town, name='town')
    return {
        'data': [trace1, trace2],
        'layout': go.Layout(title=f'Education Level distribution(village/town)',
                            colorway=["#EF963B", "#EF533B"],
                            hovermode="closest",
                            clickmode='event',
                            xaxis={'title': "Education", 'titlefont': {'color': 'black', 'size': 14},
                                   'tickfont': {'size': 9, 'color': 'black'}},
                            yaxis={'title': "Total count", 'titlefont': {'color': 'black', 'size': 14, },
                                   'tickfont': {'color': 'black'}})
    }


@app.callback(
    Output('pca_scatter', 'figure'),
    [Input('pca_dropdown', 'value'),
     Input('education_bar', 'hoverData')]
)
def update_pca_scatter(question_of_interest, hoverData):
    # select data according to question of interest
    if question_of_interest == 'age':
        data_of_interest = spending_cols
        target = 'Age'
        possible_result = response_data.Age.unique()
    elif question_of_interest == 'movie':
        data_of_interest = movie_cols
        target = 'Countryside, outdoors'
        possible_result = [0, 1, 2, 3, 4, 5]
    else:
        data_of_interest = phobia_cols
        target = 'Hypochondria'
        possible_result = [0, 1, 2, 3, 4, 5]
    # print(question_of_interest)
    # perform pca analysis based on question of interest
    # 2 component pca analysis
    result = hoverData['points'][0]['curveNumber']
    if result == 0:
        location = 'village'
    else:
        location = 'city'

    filtered_df = response_data.dropna(subset=['Village - town'])
    filtered_df = filtered_df[filtered_df['Village - town'] == location]
    filtered_df = filtered_df.dropna(subset=data_of_interest)
    filtered_df = filtered_df.dropna(subset=[target])
    # print(filtered_df)
    pca = PCA(n_components=2)
    # Separating out the features
    x = filtered_df.loc[:, data_of_interest].values
    # print(x)
    y = filtered_df[target]
    # print(y)
    x = StandardScaler().fit_transform(x)
    principalComponents = pca.fit_transform(x)
    # print(principalComponents)
    principalDf = pd.DataFrame(data=principalComponents
                               , columns=['principal_component_1', 'principal_component_2'])
    finalDf = pd.concat([principalDf, filtered_df[[target]]], axis=1)
    finalDf = finalDf.dropna()
    # print(finalDf)
    return {
        'data': [dict(
            x=finalDf[finalDf[target] == i]['principal_component_1'],
            y=finalDf[finalDf[target] == i]['principal_component_2'],
            text=finalDf[target],
            mode='markers',
            opacity=0.7,
            color=finalDf[finalDf[target] == i][target],
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'},
                'color': finalDf[target],
            },
            name=i
        ) for i in possible_result],
        #帮我看看怎么让图右边的12345换成他们对应的颜色 你把鼠标挪到点上 能看到12345该有什么颜色
        'layout': go.Layout(title=f'Principal Component Analysis of Question of Interest) for ' + location,
                            hovermode="closest",
                            xaxis={'title': "Principal Component 1", 'titlefont': {'color': 'black', 'size': 14},
                                   'tickfont': {'size': 9, 'color': 'black'}},
                            yaxis={'title': "Principal Component 2", 'titlefont': {'color': 'black', 'size': 14, },
                                   'tickfont': {'color': 'black'}})
    }

#sankey
# @app.callback(
#     Output('sankey','figure'),
#     [Input('education_bar', 'hoverData')]
# )
# def update_sankey(hoverData):
#     #select village or city rows from response_data
#     #response_data['Village - town'] = "village" or "city"
#     result = hoverData['points'][0]['curveNumber']
#     if result == 0:
#         location = 'village'
#     else:
#         location = 'city'
#
#     filtered_df = response_data.dropna(subset=['Village - town'])
#     #随便画个sankey图吧 挑几页
#

if __name__ == '__main__':
    app.run_server(debug=True, port=8800)
