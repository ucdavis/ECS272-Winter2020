import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA


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
responses_file = 'responses.csv'
response_data = pd.read_csv(responses_file)
names = response_data.columns

# remove rows with na
response_data = response_data.dropna()
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

# select variables with correlation >= 0.3 for the selected question of interest
corr = response_data.corr()
target_snake = abs(corr["Snakes"])
relevant_snake = target_snake[target_snake >= 0.3].index
target_shopping = abs(corr["Shopping"])
relevant_shopping = target_shopping[target_shopping >= 0.3].index
target_math = abs(corr["Mathematics"])
relevant_math = target_math[target_math >= 0.3].index
target_sport = abs(corr["Active sport"])
relevant_sport = target_sport[target_sport >= 0.3].index
target_rock = abs(corr["Rock"])
relevant_rock = target_rock[target_rock >= 0.3].index

possible_education = ['currently a primary school pupil', 'primary school', 'secondary school', 'college/bachelor '
                                                                                                'degree',
                      'masters degree', 'doctorate degree']

app.layout = html.Div([
    html.H1("Education Level Distribution(Grew up in village/town)", style={"textAlign": "center"}),
    html.Div([
        html.H6("Select maximum age of interest", style={"textAlign": "center"}),
        dcc.Slider(
            id='age_slider',
            min=response_data['Age'].min()+2,
            max=response_data['Age'].max(),
            value=response_data['Age'].max(),
            marks={
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
    html.H3("Hover over bar to see Principle Component Analysis of village/town and the sankey graph of "
            "village/town", style=({"textAlign": "center"})),
    dcc.Graph(id='education_bar', hoverData={'points': [{'curveNumber': 1}]}),
    html.Div([
        html.Div([
            html.H3('Principal Component Analysis: Select Question of Interest', style=({"textAlign": "center"})),
            dcc.Dropdown(
                id='pca_dropdown',
                options=[
                    {'label': 'Explore variables relates to Rock Music', 'value': 'rock'},
                    {'label': 'Explore variables relates to Active Sport', 'value': 'sport'},
                    {'label': 'Explore variables relates to Shopping', 'value': 'shopping'},
                    {'label': 'Explore variables relates to Mathematics', 'value': 'math'},
                    {'label': 'Determine the level of fear towards Snakes through other phobias', 'value': 'snakes'}
                ],
                value='snakes',
                style=({"textAlign": "center"})
            ),
            html.H5('Select the number of principal components desired:', style=({"textAlign": "center"})),
            dcc.RadioItems(
                id='pca_radio',
                options=[{'label': i, 'value': i} for i in [2, 3]],
                value=3,
                labelStyle={'display': 'inline-block'},
                style=({"textAlign": "center"})
            ),
            dcc.Graph(id='pca_scatter')
        ], className="six columns"),
        html.Div([
            html.H3('Sankey graph: How demographic affect people\'s view toward movie / music',
                    style=({"textAlign": "center"})),
            dcc.Dropdown(
                id='sankey_dropdown',
                options=[
                    {'label': 'Music', 'value': 'music'},
                    {'label': 'Movie', 'value': 'movie'},
                ],
                value='music',
                style=({"textAlign": "center"})
            ),
            dcc.Graph(id='sankey')
        ], className="six columns")
    ], className="row")
])


@app.callback(
    dash.dependencies.Output('education_bar', 'figure'),
    [dash.dependencies.Input('age_slider', 'value')]
)
def update_education_bar(input_age):
    filtereddata = response_data[response_data.Age <= input_age]
    # group by education level then count village/town
    count = filtereddata.groupby(['Education', 'Village - town']).size().unstack()
    # print(count)
    village = count['village']
    town = count['city']
    trace1 = go.Bar(x=possible_education, y=village, name='village')
    trace2 = go.Bar(x=possible_education, y=town, name='town')
    return {
        'data': [trace1, trace2],
        'layout': go.Layout(title='Education Level distribution(village/town)',
                            colorway=["#EF963B", "#EF533B"],
                            hovermode="closest",
                            clickmode='event',
                            xaxis={'title': "Education", 'titlefont': {'color': 'black', 'size': 14},
                                   'tickfont': {'size': 9, 'color': 'black'}},
                            yaxis={'title': "Total count", 'titlefont': {'color': 'black', 'size': 14, },
                                   'tickfont': {'color': 'black'}})
    }


@app.callback(
    dash.dependencies.Output('pca_scatter', 'figure'),
    [dash.dependencies.Input('pca_dropdown', 'value'),
     dash.dependencies.Input('education_bar', 'hoverData'),
     dash.dependencies.Input('pca_radio', 'value'),
     dash.dependencies.Input('age_slider','value')]
)
def update_pca_scatter(question_of_interest, hoverData, comp_num, ageValue):
    # select data according to question of interest
    if question_of_interest == 'shopping':
        data_of_interest = relevant_shopping
        target = 'Shopping'
        possible_result = [0, 1, 2, 3, 4, 5]
    elif question_of_interest == 'math':
        data_of_interest = relevant_math
        target = 'Mathematics'
        possible_result = [0, 1, 2, 3, 4, 5]
    elif question_of_interest == 'sport':
        data_of_interest = relevant_sport
        target = 'Active sport'
        possible_result = [0, 1, 2, 3, 4, 5]
    elif question_of_interest == 'rock':
        data_of_interest = relevant_rock
        target = 'Rock'
        possible_result = [0, 1, 2, 3, 4, 5]
    else:
        data_of_interest = relevant_snake
        target = 'Snakes'
        possible_result = [0, 1, 2, 3, 4, 5]
    # print(question_of_interest)
    # perform pca analysis based on question of interest
    # 2 component pca analysis
    #print("yes")
    #print(type(hoverData))
    #print(hoverData)
    result = hoverData['points'][0]['curveNumber']
    if result == 0:
        location = 'village'
    else:
        location = 'city'

    filtered_df = response_data.dropna(subset=['Village - town'])
    filtered_df = filtered_df[filtered_df['Village - town'] == location]
    filtered_df = filtered_df[filtered_df['Age'] <= ageValue]
    filtered_df = filtered_df.dropna(subset=data_of_interest)
    filtered_df = filtered_df.dropna(subset=[target])
    # print(filtered_df)
    pca = PCA(n_components=comp_num)
    # Separating out the features
    x = filtered_df.loc[:, data_of_interest].values
    # print(x)
    y = filtered_df[target]
    # print(y)
    x = StandardScaler().fit_transform(x)
    principalComponents = pca.fit_transform(x)
    # print(principalComponents)
    # print(finalDf)
    # 2 comp
    if comp_num == 2:
        principalDf = pd.DataFrame(data=principalComponents
                                   , columns=['principal_component_1', 'principal_component_2'])
        finalDf = pd.concat([principalDf, filtered_df[[target]]], axis=1)
        finalDf = finalDf.dropna()
        return {
            'data': [dict(
                x=finalDf[finalDf[target] == i]['principal_component_1'],
                y=finalDf[finalDf[target] == i]['principal_component_2'],
                # text=finalDf[target],
                text=finalDf[finalDf[target] == i][target],
                mode='markers',
                opacity=0.7,
                # color=finalDf[finalDf[target] == i][target],
                marker={
                    'size': 10,
                    'line': {'width': 0.5, 'color': 'white'}
                    # 'color': finalDf[target],
                },
                name=i
            ) for i in possible_result],
            'layout': go.Layout(title=location,
                                height=500,
                                hovermode="closest",
                                xaxis={'title': "Principal Component 1", 'titlefont': {'color': 'black', 'size': 14},
                                       'tickfont': {'size': 9, 'color': 'black'}},
                                yaxis={'title': "Principal Component 2", 'titlefont': {'color': 'black', 'size': 14, },
                                       'tickfont': {'color': 'black'}})
        }
    # 3 comp
    else:
        principalDf = pd.DataFrame(data=principalComponents
                                   ,
                                   columns=['principal_component_1', 'principal_component_2', 'principal_component_3'])
        finalDf = pd.concat([principalDf, filtered_df[[target]]], axis=1)
        finalDf = finalDf.dropna()
        #print(finalDf)
        trace = [go.Scatter3d(
            x=finalDf['principal_component_1'], y=finalDf['principal_component_2'], z=finalDf['principal_component_3'],
            mode='markers',
            text=finalDf[target],
            marker={'size': 8, 'color': finalDf[target], 'colorscale': 'Brwnyl', 'opacity': 0.8,
                    "showscale": True,
                    "colorbar": {"thickness": 15, "len": 0.5, "x": 0.8, "y": 0.6, }, })]
        return {
            'data': trace,
            "layout": go.Layout(
                height=600, title=f"3 Component analysis of question of interest ",
                # paper_bgcolor="#f3f3f3",
                scene={"aspectmode": "cube",
                       "xaxis": {"title": f"Principal Component 1", 'titlefont': {'color': 'black', 'size': 14},
                                 'tickfont': {'size': 9, 'color': 'black'}},
                       "yaxis": {"title": f"Principal Component 2", 'titlefont': {'color': 'black', 'size': 14},
                                 'tickfont': {'size': 9, 'color': 'black'}},
                       "zaxis": {"title": f"Principal Component 3", 'titlefont': {'color': 'black', 'size': 14},
                                 'tickfont': {'size': 9, 'color': 'black'}}})
        }

# Sankey
# Define the labels used in the Sankey plot.
sankey_labels = list()
sankey_labels.append('male')
sankey_labels.append('famale')
sankey_labels.append('village')
sankey_labels.append('town')
sankey_labels.append('Age 10 - 20')
sankey_labels.append('Age 20 - 30')
education_levels = response_data["Education"].unique().tolist()
for education_level in education_levels:
    sankey_labels.append(education_level)
for i in range(1, 6):
    sankey_labels.append(i)
#print(sankey_labels)
colors = ["rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)", "rgba(44, 160, 44, 0.8)",
          "rgba(214, 39, 40, 0.8)", "rgba(148, 103, 189, 0.8)", "rgba(140, 86, 75, 0.8)",
          "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)", "rgba(188, 189, 34, 0.8)",
          "rgba(23, 190, 207, 0.8)", "rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)",
          "rgba(127, 127, 127, 0.8)", "rgba(188, 189, 34, 0.8)", "rgba(23, 190, 207, 0.8)",
          "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)"]

@app.callback(
    dash.dependencies.Output('sankey', 'figure'),
    [dash.dependencies.Input('sankey_dropdown', 'value')]
)
def update_graph(dropdown_value):
    # Define the links between the labels used in the Sankey plot.
    sankey_links = dict(source=[0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6,
                                7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11],
                        target=[2, 3, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 10, 11, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                                12, 13, 14, 15, 16, 12, 13, 14, 15, 16, 12, 13, 14, 15, 16, 12, 13, 14, 15, 16,
                                12, 13, 14, 15, 16])
    sankey_links['value'] = [0] * 50

    for j in range(0, response_data.shape[0]):
        # Update the value of the related Sankey links.
        if response_data.iloc[j, 144] == 'male':
            if response_data.iloc[j, 148] == 'village':
                sankey_links['value'][0] += 1
                if response_data.iloc[j, 140] <= 20:
                    sankey_links['value'][4] += 1
                    education_location = education_levels.index(response_data.iloc[j, 146])
                    sankey_links['value'][education_location + 8] += 1
                    if dropdown_value == 'music':
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 0]) - 1] += 1
                    else:
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 19]) - 1] += 1
                else:
                    sankey_links['value'][5] += 1
                    education_location = education_levels.index(response_data.iloc[j, 146])
                    sankey_links['value'][education_location + 14] += 1
                    if dropdown_value == 'music':
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 0]) - 1] += 1
                    else:
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 19]) - 1] += 1
            else:
                sankey_links['value'][1] += 1
                if response_data.iloc[j, 140] <= 20:
                    sankey_links['value'][6] += 1
                    education_location = education_levels.index(response_data.iloc[j, 146])
                    sankey_links['value'][education_location + 8] += 1
                    if dropdown_value == 'music':
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 0]) - 1] += 1
                    else:
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 19]) - 1] += 1
                else:
                    sankey_links['value'][7] += 1
                    education_location = education_levels.index(response_data.iloc[j, 146])
                    sankey_links['value'][education_location + 14] += 1
                    if dropdown_value == 'music':
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 0]) - 1] += 1
                    else:
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 19]) - 1] += 1
        else:
            if response_data.iloc[j, 148] == 'village':
                sankey_links['value'][2] += 1
                if response_data.iloc[j, 140] <= 20:
                    sankey_links['value'][4] += 1
                    education_location = education_levels.index(response_data.iloc[j, 146])
                    sankey_links['value'][education_location + 8] += 1
                    if dropdown_value == 'music':
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 0]) - 1] += 1
                    else:
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 19]) - 1] += 1
                else:
                    sankey_links['value'][5] += 1
                    education_location = education_levels.index(response_data.iloc[j, 146])
                    sankey_links['value'][education_location + 14] += 1
                    if dropdown_value == 'music':
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 0]) - 1] += 1
                    else:
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 19]) - 1] += 1
            else:
                sankey_links['value'][3] += 1
                if response_data.iloc[j, 140] <= 20:
                    sankey_links['value'][6] += 1
                    education_location = education_levels.index(response_data.iloc[j, 146])
                    sankey_links['value'][education_location + 8] += 1
                    if dropdown_value == 'music':
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 0]) - 1] += 1
                    else:
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 19]) - 1] += 1
                else:
                    sankey_links['value'][7] += 1
                    education_location = education_levels.index(response_data.iloc[j, 146])
                    sankey_links['value'][education_location + 14] += 1
                    if dropdown_value == 'music':
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 0]) - 1] += 1
                    else:
                        sankey_links['value'][20 + education_location * 5 + int(response_data.iloc[j, 19]) - 1] += 1

    fig = go.Figure(data=[go.Sankey(node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5),
                                              label=sankey_labels, color=colors), link=sankey_links)])
    fig.update_layout(
        hovermode='x')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8800)
