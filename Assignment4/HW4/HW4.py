import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from preprocess_data import find_vector
from sklearn.decomposition import PCA
import numpy as np
from sklearn.cluster import KMeans

# 依据id合并两个表
df_movies = pd.read_csv('tmdb_5000_movies.csv')
df_credits = pd.read_csv('tmdb_5000_credits.csv')
df_credits = df_credits.rename(columns={'movie_id': 'id'})
df_movies = df_movies.merge(df_credits, on='id')

# 检查空缺值的比例，空缺率大于15%的列全部删除,剩下的空值删除所在行
miss_data_total = df_movies.isnull().sum().sort_values(ascending=False)
miss_data_per = (df_movies.isnull().sum() / df_movies.isnull().count()).sort_values(ascending=False)
miss_data = pd.concat([miss_data_total, miss_data_per], axis=1, keys=['Total', 'Percentage'])
df_movies = df_movies.drop((miss_data[miss_data['Percentage'] > 0.15]).index, axis=1)
df_movies = df_movies.dropna()

# 只保留电影上映的年份
df_movies['year'] = pd.to_datetime(df_movies['release_date']).apply(lambda x: int(x.date().year))

# 提取genres到genres_list
df_movies['genres'] = df_movies.genres.apply(json.loads)


def pipe_flatten_names(genres):
    return '|'.join([x['name'] for x in genres])


df_movies['genres'] = df_movies['genres'].apply(pipe_flatten_names)

genres_list = list()
for s in df_movies['genres'].str.split('|').values:
    genres_list = genres_list + s

genres_list = list(set(genres_list))
genres_list.remove('')
genres_list.sort()

# 按照genres新建列，如果该影片属于这个流派数值为1，否则为0
for genre in genres_list:
    df_movies.loc[df_movies['genres'].str.contains(genre), genre] = 1
    df_movies.loc[~df_movies['genres'].str.contains(genre), genre] = 0

# 统计每年的各个流派的数量,用一个新的表保存
year_list = df_movies['year'].unique()
year_list.sort()

df_genres_year = pd.DataFrame(columns=genres_list, index=year_list)
for year in year_list:
    df_genres_year.loc[year, 'year'] = year
    for genre in genres_list:
        df_genres_year.loc[year, genre] = df_movies[df_movies['year'] == year][genre].sum()

# 将打分分区间表示
df_movies.loc[(df_movies['vote_average'] >= 0) & (df_movies['vote_average'] <= 1), 'vote_interval'] = '0~1'
df_movies.loc[(df_movies['vote_average'] > 1) & (df_movies['vote_average'] <= 2), 'vote_interval'] = '1~2'
df_movies.loc[(df_movies['vote_average'] > 2) & (df_movies['vote_average'] <= 3), 'vote_interval'] = '2~3'
df_movies.loc[(df_movies['vote_average'] > 3) & (df_movies['vote_average'] <= 4), 'vote_interval'] = '3~4'
df_movies.loc[(df_movies['vote_average'] > 4) & (df_movies['vote_average'] <= 5), 'vote_interval'] = '4~5'
df_movies.loc[(df_movies['vote_average'] > 5) & (df_movies['vote_average'] <= 6), 'vote_interval'] = '5~6'
df_movies.loc[(df_movies['vote_average'] > 6) & (df_movies['vote_average'] <= 7), 'vote_interval'] = '6~7'
df_movies.loc[(df_movies['vote_average'] > 7) & (df_movies['vote_average'] <= 8), 'vote_interval'] = '7~8'
df_movies.loc[(df_movies['vote_average'] > 8) & (df_movies['vote_average'] <= 9), 'vote_interval'] = '8~9'
df_movies.loc[(df_movies['vote_average'] > 9) & (df_movies['vote_average'] <= 10), 'vote_interval'] = '9~10'


# 创建饼状图的data
def create_pie_date(genre):
    df_selected_genre = pd.DataFrame(columns=['interval'])
    df_selected_genre['interval'] = df_movies.loc[(df_movies[genre] == 1), 'vote_interval']
    vote_interval_list = df_selected_genre['interval'].unique()
    vote_interval_list.tolist()
    vote_interval_list.sort()
    sum_list = list()
    for i in vote_interval_list:
        df = df_selected_genre.loc[df_selected_genre['interval'] == i]
        a = df.shape[0]
        sum_list.append(a)
    result = pd.DataFrame(columns=['vote_index', 'sum'])
    result['vote_index'] = vote_interval_list
    result['sum'] = sum_list
    return result


def get_keywords(tmp_genre, tmp_year):
    # 首先拿到df_movie中的id，然后在原df中查找，返回
    tmp_df_movies = df_movies.loc[((df_movies[tmp_genre] != 0) & (df_movies['year'] == tmp_year))]['keywords']
    result = []
    for keyword_json in tmp_df_movies:
        tmp_result = []
        keyword_json = json.loads(keyword_json)
        for keyword in keyword_json:
            tmp_result.extend(keyword['name'].split())
        result.append(tmp_result)
    tmp_df_movies_name = df_movies.loc[((df_movies[tmp_genre] != 0) & (df_movies['year'] == tmp_year))][
        'original_title']
    names = []
    for name in tmp_df_movies_name:
        names.append(name)
    return result, names


def get_sen_embd(sentence_list):
    emd_list = np.array([])
    for sentence in sentence_list:
        if len(emd_list) == 0:
            emd_list = find_vector(sentence)
        else:
            tmp_vec = find_vector(sentence)
            if tmp_vec.shape != (0,):
                emd_list = np.concatenate((emd_list, find_vector(sentence)), axis=0)
            else:
                emd_list = np.concatenate((emd_list, np.zeros(shape=(1, 100))), axis=0)
    return emd_list


def get_coord(emd_list):
    emd_list = np.array(emd_list)
    pca = PCA(n_components=2)
    new_emd_list = pca.fit_transform(emd_list)
    return new_emd_list


# stream graph
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='stream-graph'),
    dcc.Slider(
        id='year-slider',
        min=df_genres_year['year'].min(),
        max=df_genres_year['year'].max(),
        value=df_genres_year['year'].max(),
        marks={str(year): str(year) for year in df_genres_year['year'].unique()},
        step=None
    ),
    dcc.Graph(id='scatter-graph'),
    dcc.Graph(id='pie-graph')
])


@app.callback(
    Output('stream-graph', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df_genres_year[df_genres_year.year <= selected_year]
    filtered_df['sum'] = 0
    traces = []
    for i in genres_list:
        traces.append(dict(
            fill='tonexty',
            x=filtered_df['year'],
            y=filtered_df[i] + filtered_df['sum'],
            text=i,
            type='scatter',
            name=i,
            line={'shape': 'spline', 'width': 0}
        ))
        filtered_df['sum'] += filtered_df[i]

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Year'},
            yaxis={'title': 'Sum'},
            margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            transition={'duration': 500},
            clickmode='event+select'
        )
    }


def display_scatter():
    def callback(*Datas):
        data=[]
        if (Datas[0] != None):
            points = Datas[0]['points'][0]
            year = points['x']
            sum = points['y']
            df = df_genres_year.loc[year]  # 寻找到clickdata的genre
            for genre in genres_list:
                sum -= df[genre]
                if sum == 0:
                    selected_genre = genre
                    break
            keywords, names = get_keywords(selected_genre, year)
            embedding_list = get_sen_embd(keywords)
            # print(embedding_list)
            coordinate_list = get_coord(embedding_list)
            # print(coordinate_list)
            coordinate_list.tolist()
            data=[go.Scatter(x=coordinate_list[:,0],y=coordinate_list[:,1],text=names
                  ,mode='markers',marker={'size':7,'opacity':0.5,'line':{'width':0.5,'color':'white'}})]

        return {
            'data':data,
            'layout': dict(
                xaxis={
                    'title': 'X',
                },
                yaxis={
                    'title': 'Y',
                    'type': 'linear'
                },
                title='Similarities of the movies based on their keywords',
                margin={'l': 40, 'b': 30, 't': 40, 'r': 0},
                height=450,
                hovermode='closest'
            )
        }

    return callback


# 点击stream graph里面的点会改变散点图
app.callback(
    Output('scatter-graph', 'figure'),
    [Input('stream-graph', 'clickData')]
)(display_scatter())



def display_pie():
    def callback(*Datas):
        data = []
        if (Datas[0] != None):
            points = Datas[0]['points'][0]
            year = points['x']
            sum = points['y']
            df = df_genres_year.loc[year]  # 寻找到clickdata的genre
            for genre in genres_list:
                sum -= df[genre]
                if sum == 0:
                    selected_genre = genre
                    break

            df = create_pie_date(selected_genre)
            data = [go.Pie(labels=df['vote_index'], values=df['sum'])]

        return {
            'data': data,
            'layout': dict(
                hovermode='closest',
                transition={'duration': 500},
                title='Movie rating distribution'
                # autosize=False,
            )
        }

    return callback


# #生成pie graph图
app.callback(
    Output('pie-graph', 'figure'),
    [Input('stream-graph', 'clickData')]
)(display_pie())



if __name__ == '__main__':
    app.run_server(debug=True)

