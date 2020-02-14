import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Set up type color for Sankey diagram
def type_to_color(type):
    switcher = {
        'Bug': 'lightGreen',
        'Fire': 'Red',
        'Normal': 'Grey',
        'Ground': 'Brown',
        'Water': 'aqua',
        'Electric': 'Yellow',
        'Dark': 'Black',
        'Ice': 'lightskyblue',
        'Rock': 'Brown',
        'Fighting': 'Darkred',
        'Flying': 'skyblue',
        'Poison': 'Purple',
        'Psychic': 'Peru',
        'Dragon': 'tan',
        'Steel': 'silver',
        'Grass': 'Green',
        'Fairy': 'Pink',
        'Ghost': 'deeppink'
    }
    return switcher.get(type)

# Set up dashboard style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# read the pokemon dataset
pkm = pd.read_csv('./pokemon_alopez247.csv')
pokedex = pkm[['HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed']]

cat_list = []
count = 0

gen_dict = {}
for i in pkm['Generation'].unique():
    gen_dict[i] = count
    cat_list.append("Gen-" + str(i))
    #num_dict[count] = i
    count += 1

color_dict = {}
for i in pkm['Color'].unique():
    color_dict[i] = count
    cat_list.append(i)
    #num_dict[count] = i
    count += 1

type1_dict = {}
for i in pkm['Type_1'].unique():
    type1_dict[i] = count
    cat_list.append(i + " Type")
    #num_dict[count] = i
    count += 1

egg1_dict = {}
for i in pkm['Egg_Group_1'].unique():
    egg1_dict[i] = count
    cat_list.append(i + " Egg Group")
    #num_dict[count] = i
    count += 1

#Group by Generation and Color
gen_color = pkm.groupby(['Generation', 'Color']).agg({'Name': 'count'}).reset_index()
#print(gen_color.head(20))

#Group by Color and type1
color_type1 = pkm.groupby(['Color', 'Type_1']).agg({'Name': 'count'}).reset_index()

#Group by type1 and egg1
type1_egg1 = pkm.groupby(['Type_1', 'Egg_Group_1']).agg({'Name': 'count'}).reset_index()

sources = []
targets = []
values = []
flow_color = []

for index, row in gen_color.iterrows():
    sources.append(gen_dict[row['Generation']])
    targets.append(color_dict[row['Color']])
    values.append(row['Name'])
    if row['Color'] == 'White':
        flow_color.append('Silver')
    else:
        flow_color.append(row['Color'])
    #flow_color.append('brown')
    
for index, row in color_type1.iterrows():
    sources.append(color_dict[row['Color']])
    targets.append(type1_dict[row['Type_1']])
    values.append(row['Name'])
    if row['Color'] == 'White':
        flow_color.append('Silver')
    else:
        flow_color.append(row['Color'])
    #flow_color.append('brown')

for index, row in type1_egg1.iterrows():
    sources.append(type1_dict[row['Type_1']])
    targets.append(egg1_dict[row['Egg_Group_1']])
    values.append(row['Name'])
    flow_color.append(type_to_color(row['Type_1']))
    #flow_color.append('brown')

# PCA Dimensionality reduction
pca = PCA(n_components=2)
fit = pca.fit_transform(pokedex)
fit1 = pd.DataFrame(fit, columns=['c1', 'c2'])

color_list = ['steelblue', 'black', 'yellow', 'seagreen', 'cyan', 'darkblue', 'darkseagreen', \
    'lightcoral', 'red', 'lightblue', 'hotpink', 'gray', 'darkviolet', 'deeppink', 'darkred', \
        'darksalmon', 'darkgreen', 'darkgoldenrod', 'orange', 'purple']

# Dashboard layout
app.layout = html.Div([
    # Scatter plot for K-means clustering
    html.Div([
        html.H1(
            children='K-Means Clustering For Pokemon Dataset',
            style={'textAlign': 'center'}
        ),
        dcc.Graph(
            id='kmeans_with_k',
            clickData={'points': [{'customdata': '0'}]}
        ),
        # Dropdown Widget
        dcc.Dropdown(
            id='k_selection',
            options=[
                {'label': 'k = 1', 'value': 1},
                {'label': 'k = 2', 'value': 2},
                {'label': 'k = 4', 'value': 4},
                {'label': 'k = 5', 'value': 5},
                {'label': 'k = 6', 'value': 6},
                {'label': 'k = 7', 'value': 7},
                {'label': 'k = 9', 'value': 9},
                {'label': 'k = 10', 'value': 10},
                {'label': 'k = 11', 'value': 11},
                {'label': 'k = 12', 'value': 12},
                {'label': 'k = 15', 'value': 15},
                {'label': 'k = 18', 'value': 18},
                {'label': 'k = 20', 'value': 20}
            ],
            value=1
        )
    ]),
    # Type distribution bar chart for selected group
    html.Div([
        html.H1(
            children='Type Distribution of Selected Cluster',
            style={'textAlign': 'center'}
        ),
        dcc.Graph(id='type_bar_chart')
    ]),
    # Generation distribution bar chart for selected group
    html.Div([
        html.H1(
            children='Generation Distribution of Selected Cluster',
            style={'textAlign': 'center'}
        ),
        dcc.Graph(id='generation_bar_chart')
    ]),
    # Sankey Diagram
    html.Div([
        html.H1(
            children='Sankey Diagram for Pokemon Dataset',
            style={'textAlign': 'center'}
        ),
        dcc.Graph(
            id='snakey_diagram',
            figure=go.Figure(data=[go.Sankey(
                valueformat = ".0f",
                valuesuffix = " pokemon",
                # Define nodes
                node = dict(
                    pad = 15,
                    thickness = 15,
                    #line = dict(color = "black", width = 0.5),
                    label =  cat_list,
                    color =  'darkcyan'
                ),
                # Add links
                link = dict(
                    source =  sources,
                    target =  targets,
                    value =  values,
                    color =  flow_color
                    #label =  data['data'][0]['link']['label']
                ))])
        ),
    ])
])

# update the k-means graph
@app.callback(
    Output('kmeans_with_k', 'figure'),
    [Input('k_selection', 'value')]
)
def update_kmeans_graph(k):
    pkm_km = KMeans(n_clusters=k, random_state=0).fit_predict(fit1)
    pkm['c1'] = fit1['c1']
    pkm['c2'] = fit1['c2']
    gpname = 'Group' + str(k)
    pkm[gpname] = pkm_km

    traces = []
    for i in pkm[gpname].unique():
        pkm_cluster = pkm[pkm[gpname] == i]
        pkm_not_legn = pkm_cluster[pkm_cluster['isLegendary'] == False]
        pkm_legn = pkm_cluster[pkm_cluster['isLegendary'] == True]
        traces.append(dict(
            x=pkm_not_legn['c1'],
            y=pkm_not_legn['c2'],
            text=pkm_not_legn['Name'],
            customdata=pkm_not_legn[gpname],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 10,
                'line': {'width': 0.5, 'color': 'white'},
                'symbol': 'circle',
                'color':color_list[i]
            },
            name = 'group ' + str(i) + ' not legendary'
        ))
        traces.append(dict(
            x=pkm_legn['c1'],
            y=pkm_legn['c2'],
            text=pkm_legn['Name'],
            customdata=pkm_legn[gpname],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 10,
                'line': {'width': 0.5, 'color': 'white'},
                'symbol': 'star',
                'color':color_list[i]
            },
            name = 'group ' + str(i) + ' legendary'
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'range':[-100, 150]},
            yaxis={'range': [-100, 200]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
            clickmode='event+select'
        )
    }

# update the type bar chart
@app.callback(
    Output('type_bar_chart', 'figure'),
    [Input('kmeans_with_k', 'clickData'), Input('k_selection', 'value')]
)
def update_type_chart(clickData, k):
    group_number = clickData['points'][0]['customdata']
    if(group_number == '0'): selected_pkm = pkm
    else: selected_pkm = pkm[pkm['Group' + str(k)] == group_number]
 
    type_list = pkm['Type_1'].unique()
    type_count = selected_pkm['Type_1'].value_counts()
    count_list = []
    for t in type_list:
        try: count_list.append(type_count[t])
        except: count_list.append(0)

    return {
        'data': [
            {'x': type_list, 'y': count_list, 'type': 'bar'}
        ],
        'layout': dict(
            height=225,
            margin={'l': 20, 'b': 30, 'r': 10, 't': 10},
        )
    }

# update the generation bar chart
@app.callback(
    Output('generation_bar_chart', 'figure'),
    [Input('kmeans_with_k', 'clickData'), Input('k_selection', 'value')]
)
def update_generation_chart(clickData, k):
    group_number = clickData['points'][0]['customdata']
    if(group_number == '0'): selected_pkm = pkm
    else: selected_pkm = pkm[pkm['Group' + str(k)] == group_number]

    gen_list = pkm['Generation'].unique()
    gen_count = selected_pkm['Generation'].value_counts()
    count_list = []
    for t in gen_list:
        try: count_list.append(gen_count[t])
        except: count_list.append(0)

    return {
        'data': [
            {'x': gen_list, 'y': count_list, 'type': 'bar'}
        ],
        'layout': dict(
            height=225,
            margin={'l': 20, 'b': 30, 'r': 10, 't': 10},
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)