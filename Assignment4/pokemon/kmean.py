import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objs as go
import json
import dash
import urllib.request
import bs4 as bs
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


pokemon = pd.read_csv('pokemon_alopez247.csv')
pkm_df = pokemon.replace(np.nan, 'NaN') # replace all nan to 'NaN'
features = list(pkm_df.columns)[2:] #x & y axis to be chosen to show
pkm_data = pkm_df.to_numpy()[:, 2:]
pkm_names = pkm_df.to_numpy()[:, 1]
pkm_names = np.reshape(pkm_names, (-1, 1))

# remove column of Total
features.remove('Total')
pkm_data = np.delete(pkm_data, 2, 1)
colors = {
    "Bug": "#A6B91A",
    "Dark": "#705746",
    "Dragon": "#6F35FC",
    "Electric": "#F7D02C",
    "Fairy": "#D685AD",
    "Fighting": "#C22E28",
    "Fire": "#EE8130",
    "Flying": "#A98FF3",
    "Ghost": "#735797",
    "Grass": "#7AC74C",
    "Ground": "#E2BF65",
    "Ice": "#96D9D6",
    "Normal": "#A8A77A",
    "Poison": "#A33EA1",
    "Psychic": "#F95587",
    "Rock": "#B6A136",
    "Steel": "#B7B7CE",
    "Water": "#6390F0",
}

feat_to_cat = ['Type_1', 'Type_2', 'isLegendary', 'Color', 'hasGender', 'Egg_Group_1', 'Egg_Group_2', 'hasMegaEvolution', 'Body_Style']
feat_index = [features.index(feat) for feat in feat_to_cat]
feat_dict = dict()
for col in feat_index:
    col_data = pkm_data[:, col]
    col_data_uniq = np.unique(col_data).tolist()
    if 'NaN' in col_data_uniq:
        col_data_uniq.remove('NaN')
    feat_dict[features[col]] = ['NaN'] + col_data_uniq

for col in feat_index:
    col_data = pkm_data[:, col]
    values = feat_dict[features[col]]
    for i in range(len(col_data)):
        val = values.index(col_data[i])
        col_data[i] = val

# eliminate 'NaN' in other columns
features_copy = [f for f in features]
for f in feat_to_cat:
    features_copy.remove(f)
for col in features_copy:
    col_data = pkm_data[:, features.index(col)]
    for i in range(len(col_data)):
        if col_data[i] == 'NaN':
            if col == 'Pr_Male':
                col_data[i] = 0.5
            else:
                col_data[i] = 0

#pkm_data = pkm_data.astype(np.float64)
pkm_df = pd.DataFrame(data=pkm_data, columns=features) # strip col of number & name and convert all to digits

# cluster
def k_cluster(k):
    global pkm_df
    clusters = k
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(pkm_df)
    cluster_column = np.asarray(kmeans.labels_)
    cluster_column = np.reshape(cluster_column, (-1, 1))

    return cluster_column

# PCA
def pCA():
    global pkm_df
    pca = PCA(3)
    pca.fit(pkm_df)
    pca_data_n = pca.transform(pkm_df)
    pca_data_n = np.append(pca_data_n, pkm_names, 1)

    return pca_data_n

def pCA_df(pca_data, cluster_column):
    global pkm_df,pkm_data
    pca_data_k = np.append(pca_data, cluster_column, 1)
    pca_df = pd.DataFrame(data=pca_data_k, columns=['0', '1', '2', 'n', 'c'])

    pkm_data_k = np.append(pkm_data, cluster_column, 1)
    pkm_df = pd.DataFrame(data=pkm_data_k, columns=features + ['c'])
    return pca_df

def create_figure(k):
    global pca_data, pca_df
    pca_df = pCA_df(pca_data, k_cluster(k))
    return px.scatter_3d(pca_df, x='0', y='1', z='2', color='c')

# selection from 3d plot
pca_data = pCA()
pca_df = pCA_df(pca_data, k_cluster(7))

pkm_selected = list()
f = create_figure(7)
last_k = 7

box_colors = ['#FF851B', '#FF4136', '#3D9970']
imagestyle = {"height":300,"background-color": "rgba(255, 255, 255, 0.9)","display":"none",'text-align':"center"}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
                html.Div([
                    html.Div([
                        'Choose K to cluster ',
                        dcc.Dropdown(
                            id='k_val',
                            options=[{'label': str(i+1), 'value': i+1} for i in range(10)],
                            value=7
                        ),
                    ],style={'width': '20%', 'display': 'inline-block'}),
                    dcc.Graph(id = '3d_scat', figure=f, style={
                        'height': 900,'opacity':'0.9'
                    }),
                    html.Div('Selected:'),
                    html.Div(id='selected_pkm',style={'display':'none'}),
                    html.Div(id='selected_names', children="[]"),
                    html.Div(id='selected_cluster', children="[]", style={
                        'display': 'none'
                    }),

                    html.Button('Clear Selection', id='clear')], style={'textAlign': 'center'}),
                    html.Div(id='imgs',children=[
                        html.Img(id='img1'),
                        html.Img(id='img2'),
                        html.Img(id='img3')
                    ]),

                    dcc.Graph(id = "stats",style={'float':'left','opacity':'0.9'}),
                    dcc.Graph(id = "box_plot",style={'float':'left','opacity':'0.9'})

])
def empty_plot(label_annotation):
    '''
    Returns an empty plot with a centered text.
    '''

    trace1 = go.Scatter(
        x=[],
        y=[]
    )

    data = [trace1]

    layout = go.Layout(
        showlegend=False,
        xaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        annotations=[
            dict(
                x=0,
                y=0,
                xref='x',
                yref='y',
                text=label_annotation,
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=0
            )
        ]
    )

    fig = go.Figure(data=data, layout=layout)
    # END
    return fig

def polar_pokemon_stats(pkmn_name):

    pkmn = pokemon[pokemon.Name == pkmn_name]
    plot = go.Scatterpolar(
        r=[
            pkmn['HP'].values[0],
            pkmn['Attack'].values[0],
            pkmn['Defense'].values[0],
            pkmn['Sp_Atk'].values[0],
            pkmn['Sp_Def'].values[0],
            pkmn['Speed'].values[0],
            pkmn['HP'].values[0]
        ],
        theta=[
            'HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed', 'HP'
        ],
        fill='toself',
        marker=dict(
            color=colors[pkmn['Type_1'].values[0]]
        ),
        name=pkmn['Name'].values[0]
    )

    return plot

def listToStr(list):
    if len(list) == 0:
        return "[]"
    else:
        ans = "["
        for i in list:
            ans  = ans + i + ","
        ans = ans[:-1]
        ans = ans + "]"
        return ans

def strToList(content):
    if content == "[]":
        return list()
    else:
        content = content[1:-1]
        return content.split(',')

@app.callback(Output('selected_pkm', 'children'),
            [Input('3d_scat', 'clickData'),
             Input('clear', 'n_clicks'),
             Input('k_val', 'value')],
            [State('selected_pkm', 'children')])
def select_point(clickData, clear_clicked, k, selected_points):
    global pca_data

    ctx = dash.callback_context
    ids = [c['prop_id'] for c in ctx.triggered]
    if selected_points:
        results = json.loads(selected_points)
    else:
        results = []

    if len(results) > 2:
        if 'clear.n_clicks' in ids:
            results = []
        # TO DO not sure what is this
        return json.dumps(results)
    else:
        if '3d_scat.clickData' in ids:
            if clickData:
                for p in clickData['points']:
                    if p not in results:
                        results.append(p)
        if 'clear.n_clicks' in ids:
            results = []
    return json.dumps(results)

@app.callback(Output('selected_names', 'children'),
            [Input('3d_scat', 'clickData'),
             Input('clear', 'n_clicks'),
             Input('k_val', 'value')],
            [State('selected_names', 'children')])
def select_point(clickData, clear_clicked, k, selected_names):
    global pca_data, last_k
    pca_df_n = pd.DataFrame(data=pca_data, columns=['0', '1', '2', 'n'])

    ctx = dash.callback_context
    ids = [c['prop_id'] for c in ctx.triggered]
    results = strToList(selected_names)

    if last_k != k:
        return "[]"
    elif len(results) > 2:
        if 'clear.n_clicks' in ids:
            results = []
        # TO DO not sure what is this
        return listToStr(results)
    else:
        if '3d_scat.clickData' in ids:
            if clickData:
                for p in clickData['points']:
                    px = p['x']
                    py = p['y']
                    pz = p['z']
                    tar = pca_df_n[pca_df_n['0'] == px]
                    tar = tar[tar['1'] == py]
                    tar = tar[tar['2'] == pz]
                    name = tar['n'].tolist()[0]
                    if name not in results:
                        results.append(name)
        if 'clear.n_clicks' in ids:
            results = []

        return listToStr(results)


@app.callback(Output('stats','figure'),
              [Input('3d_scat', 'clickData'),
               Input('clear', 'n_clicks'),
               Input('selected_names', 'children'),
               Input('k_val', 'value')],
              [State('stats','figure')])
def draw_stats(nclicks,clear,selected_names, k, selected_points):
    #print("draw stats called")
    global last_k
    names = strToList(selected_names)
    if len(names) == 0 or last_k != k:
        return empty_plot('No Pokemon selected yet')
    else:
        name_str = ",".join(names)
        #print(",".join(selected_names))
        layout = go.Layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 250]
                )
            ),
            showlegend=False,
            title="Stats of {}".format(name_str)
        )
        plot_pokelist = []
        for name in names:
            plot_pokelist.append(polar_pokemon_stats(name))

        pokemon_figure = go.Figure(data=plot_pokelist, layout=layout)
        return pokemon_figure


@app.callback(Output('3d_scat', 'figure'),
            [Input('clear', 'n_clicks'),
             Input('selected_pkm', 'children'),
             Input('k_val', 'value')])
def chart_3d(clear, selected_points, k):
    global f,last_k
    if last_k != k:
        f = create_figure(k)
        last_k = k
    '''
    ctx = dash.callback_context
    ids = [c['prop_id'] for c in ctx.triggered]
    selected_points = json.loads(selected_points) if selected_points else []
    #print(len(selected_points))
    if selected_points:
        color = ''
        if 'clear.n_clicks' in ids:

        else:
        f.add_trace(
            go.Scatter3d(
                mode='markers',
                x=[p['x'] for p in selected_points],
                y=[p['y'] for p in selected_points],
                z=[p['z'] for p in selected_points],
                marker=dict(
                    color='red',
                    size=5,
                    line=dict(
                        color='red',
                        width=2
                    )
                ),
                showlegend=False
            )
        )
    '''
    return f
@app.callback(Output('imgs','style'),
              [Input("3d_scat", "clickData"),
               Input('selected_names', 'children')])
def image_style(click,selected_names):
    selected_names = strToList(selected_names)
    if len(selected_names) != 0:
        if "display" in imagestyle:
            del imagestyle['display']
        return imagestyle
    else:
        imagestyle["display"] = "none"
        return imagestyle

@app.callback(Output('img1','src'),
              [Input("3d_scat","clickData"),
              Input('selected_names', 'children')])
def getimage_src(click,selected_names):
    selected_names = strToList(selected_names)
    if len(selected_names) > 0:
        sauce = urllib.request.urlopen("https://www.pokemon.com/us/pokedex/" + selected_names[0]).read()

        soup = bs.BeautifulSoup(sauce, "lxml")

        for image in soup.find_all("img", {"class": "active"}):
            url = image['src']
            break

        return url
    else:
        return ""
@app.callback(Output('img2','src'),
              [Input("3d_scat","clickData"),
              Input('selected_names', 'children')])
def getimage_src(click,selected_names):
    selected_names = strToList(selected_names)
    if len(selected_names) > 1 :
        sauce = urllib.request.urlopen("https://www.pokemon.com/us/pokedex/" + selected_names[1]).read()

        soup = bs.BeautifulSoup(sauce, "lxml")

        for image in soup.find_all("img", {"class": "active"}):
            url = image['src']
            break

        return url
    else:
        return ""
@app.callback(Output('img3','src'),
              [Input("3d_scat","clickData"),
              Input('selected_names', 'children')])
def getimage_src(click,selected_names):
    selected_names = strToList(selected_names)
    if len(selected_names) > 2:
        sauce = urllib.request.urlopen("https://www.pokemon.com/us/pokedex/" + selected_names[2]).read()

        soup = bs.BeautifulSoup(sauce, "lxml")

        for image in soup.find_all("img", {"class": "active"}):
            url = image['src']
            break

        return url
    else:
        return ""

@app.callback(Output('img1','style'),
              [Input("3d_scat","clickData"),
              Input('selected_names', 'children')])
def getimage(click,selected_names):
    selected_names = strToList(selected_names)
    if len(selected_names) == 0:
        return {'display':'none'}
    else:
        return {'display':"inline-block",'width':250,"height":250}
@app.callback(Output('img2','style'),
              [Input("3d_scat","clickData"),
              Input('selected_names', 'children')])
def getimage(click,selected_names):
    selected_names = strToList(selected_names)
    if len(selected_names) <= 1:
        return {'display':'none'}
    else:
        return {'display':"inline-block",'width':250,"height":250}
@app.callback(Output('img3','style'),
              [Input("3d_scat","clickData"),
              Input('selected_names', 'children')])

def getimage(click,selected_names):
    selected_names = strToList(selected_names)
    if len(selected_names) <=2:
        return {'display':'none'}
    else:
        return {'display':"inline-block",'width':250,"height":250}
@app.callback(Output('selected_cluster', 'children'),
            [Input('3d_scat', 'clickData'),
             Input('clear', 'n_clicks'),
             Input('k_val', 'value')],
            [State('selected_cluster', 'children')])
def select_point(clickData, clear_clicked, k, selected_cluster):
    global pca_df, last_k

    ctx = dash.callback_context
    ids = [c['prop_id'] for c in ctx.triggered]
    results = eval(selected_cluster)

    if last_k != k:
        return "[]"
    elif len(results) > 2:
        if 'clear.n_clicks' in ids:
            selected_cluster = "[]"
        return selected_cluster
    else:
        if '3d_scat.clickData' in ids:
            if clickData:
                for p in clickData['points']:
                    px = p['x']
                    py = p['y']
                    pz = p['z']
                    tar = pca_df[pca_df['0'] == px]
                    tar = tar[tar['1'] == py]
                    tar = tar[tar['2'] == pz]
                    cluster = tar['c'].tolist()[0]
                    if cluster not in results:
                        results.append(cluster)
        if 'clear.n_clicks' in ids:
            results = []

        ans = "["
        if len(results) > 0:
            for c in results:
                ans = ans + str(c) + ","
            ans = ans[:-1] + "]"
        else:
            ans = ans + "]"
        return ans

@app.callback(Output('box_plot','figure'),
              [Input('3d_scat', 'clickData'),
               Input('clear', 'n_clicks'),
               Input('selected_cluster', 'children'),
               Input('k_val', 'value')],
              [State('box_plot','figure')])
def draw_box(nclicks,clear,selected_cluster, k, selected_points):
    global pkm_df, box_colors, last_k

    clusters = eval(selected_cluster)
    print(clusters)
    if len(clusters) == 0 or last_k != k:
        return empty_plot("No pokemon selected yet")
    else:
        clusters_data = []
        for c in clusters:
            cluster = pkm_df[pkm_df['c'] == c]
            clusters_data.append(cluster)
        data = []
        index = 0
        for c_data in clusters_data:
            name = c_data['c'].tolist()[0]
            defense = c_data['Defense'].tolist()
            attack = c_data['Attack'].tolist()
            HP = c_data['HP'].tolist()
            sp_atk = c_data['Sp_Atk'].tolist()
            sp_def = c_data['Sp_Def'].tolist()
            speed = c_data['Speed'].tolist()
            count = len(defense)
            x = ['Defense' for i in range(count)] + ['Attack' for i in range(count)] + ['HP' for i in range(count)] + ['Sp_Atk' for i in range(count)] + ['Sp_Def' for i in range(count)] + ['Speed' for i in range(count)]
            y = defense + attack + HP + sp_atk + sp_def + speed
            trace = go.Box(
                y=y,
                x=x,
                name= name,
                marker=dict(
                    color=box_colors[index%3]
                )
            )
            data.append(trace)
            index += 1
        layout = go.Layout(
            yaxis=dict(
                title='Value',
                zeroline=False
            ),
            boxmode='group'
        )
        fig = go.Figure(data=data, layout=layout)
        return fig
if __name__ == '__main__':
    app.run_server(debug=True)