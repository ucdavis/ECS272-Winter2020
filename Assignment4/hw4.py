import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import urllib.request as req
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
from factor_analyzer import FactorAnalyzer
from sklearn.preprocessing import LabelEncoder  

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

file_responses = open('responses.csv')
file_columns=open('columns.csv')

data0 = pd.read_csv(file_columns)
categories=['Music']*19+['Movie']*12+['Hobbies']*32+['Phobias']*10+['Health habits']*3+['Personality views & opinions']*57+['Spending habits']*7+['Demographics']*10
data0['category']=categories

df = data0[data0['category']!='Demographics']

data = pd.read_csv(file_responses)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

currenttype = 'Music'

questions= data0['short'].tolist()
cata = data0['category'].tolist()
types=['Music','Movie','Hobbies','Phobias','Health habits','Personality views & opinions'
       ,'Spending habits']
indexs={'Music':[0,19],'Movie':[19,31],'Hobbies':[31,63],'Phobias':[63,73],
        'Health habits':[73,76],'Personality views & opinions':[76,133],'Spending habits':[133,140]}


#fa
factors_num={'Music':5,'Movie':4,'Hobbies':6,'Phobias':10,
        'Health habits':3,'Personality views & opinions':5,'Spending habits':7}

fa=FactorAnalyzer(factors_num[currenttype], rotation="varimax")

def fa_preprocess(current_type, count):
    data_type=data.iloc[:, indexs[current_type][0]: indexs[current_type][1]]
    data_type=data_type.dropna()
    data_type = data_type.apply(LabelEncoder().fit_transform)

    fa = FactorAnalyzer(count, rotation="varimax")
    x_fa=fa.fit_transform(data_type)        
    df_type=pd.DataFrame(x_fa)       

    return df_type
#fa END

#heatmap
def hp_preprocess(current_type, count):
    data_type=data.iloc[:, indexs[current_type][0]: indexs[current_type][1]]
    data_type=data_type.dropna()
    data_type = data_type.apply(LabelEncoder().fit_transform)

    fa = FactorAnalyzer(count, rotation="varimax")
    x_fa=fa.fit_transform(data_type) 
    return pd.DataFrame(np.abs(fa.loadings_))
#


df['total']='total'
fig = px.treemap(df,path=['total','category','short'],maxdepth=2)


app.layout = html.Div(children=[
    html.H1('ECS272 Assignment 4'),
    html.Div([
        html.H5('Treemap of Questions')
    ]),
    dcc.Graph(id='treemap',figure=fig,clickData={'points': [{'label': 'Music'}]}),
    html.Br(),
    html.H5('Percentage of Every Answer in Every Question'),
    dcc.Graph(id='barmap'),
    html.Br(),
    html.Div([
        html.H5('Factor analysis and dimension reduction', style={
        'textAlign': 'center'
    })
    ]),
    dcc.Dropdown(id='number0'
        #options=[{'label':i,'value':i} for i in range (2,13)],
        #value = factors_num[currenttype]
                 ),
    dcc.Graph(id='fa'),
    # html.Div([
    #     html.P(id='description')
    # ]),
    html.Br(),
    html.H5('Heatmap of every question and every dimension'),
    dcc.Graph(id='heatmap'),
    html.Div(id='intermediate-value', style={'display': 'none'})
    ],style={'textAlign': 'center'}
    )


@app.callback(
    dash.dependencies.Output('number0', 'options'),
    [dash.dependencies.Input('treemap','clickData')]
    )
def updatechoice(clickData):
    global currenttype
    if clickData:
        if clickData['points'][0]['label'] in types:
            currenttype = clickData['points'][0]['label']
    data2 = data0[data0['category']==currenttype]
    questions0= data2['short'].tolist()
    mm=len(questions0)
    if mm >=12:
        nn=[{'label':i,'value':i} for i in range (2,13)]
    else:
        nn=[{'label':i,'value':i} for i in range (2,mm+1)]
    
    return nn



@app.callback(
    dash.dependencies.Output('number0', 'value'),
    [dash.dependencies.Input('treemap','clickData')]
    )
def updatechoice(clickData):
    global currenttype
    if clickData:
        if clickData['points'][0]['label'] in types:
            currenttype = clickData['points'][0]['label']
    value = factors_num[currenttype]
    
    return value




@app.callback(
    dash.dependencies.Output('barmap', 'figure'),
    [dash.dependencies.Input('treemap','clickData')]
    )
def updatetreemap(clickData):
    global currenttype
    if clickData:
        if clickData['points'][0]['label'] in types:
            currenttype = clickData['points'][0]['label']
    index=indexs[currenttype]
    start=index[0]
    end=index[1]
    print(currenttype)
    print(index)
    
    
    data1 = data.iloc[:, start:end].dropna()
    melted = pd.melt(data1)
    twoway=pd.crosstab(melted['variable'], melted['value'])
    percentage=twoway.divide(twoway.sum(axis=1),axis=0)
    #print(percentage)
    #print(type(percentage))

    data2 = data0[data0['category']==currenttype]
    questions0= data2['short'].tolist()

    mmm = percentage.T.to_dict('list')
    nnn = list(percentage)
    ww=[]
    num = len(nnn)
    for i in range (num):
        ww.append([])
        for qs in questions0:
            ww[-1].append(mmm[qs][i])
    if currenttype == 'Personality views & opinions':
        fig9 = go.Figure(
            data=[go.Bar(name='{}'.format(nnn[0]),x=questions0,y=ww[0]),
                  go.Bar(name='{}'.format(nnn[1]),x=questions0,y=ww[1]),
                  go.Bar(name='{}'.format(nnn[2]),x=questions0,y=ww[2]),
                  go.Bar(name='{}'.format(nnn[3]),x=questions0,y=ww[3]),
                  go.Bar(name='{}'.format(nnn[4]),x=questions0,y=ww[4]),
                  go.Bar(name='{}'.format(nnn[5]),x=questions0,y=ww[5]),
                  go.Bar(name='{}'.format(nnn[6]),x=questions0,y=ww[6]),
                  go.Bar(name='{}'.format(nnn[7]),x=questions0,y=ww[7]),
                  go.Bar(name='{}'.format(nnn[8]),x=questions0,y=ww[8]),
                  go.Bar(name='{}'.format(nnn[9]),x=questions0,y=ww[9]),
                  go.Bar(name='{}'.format(nnn[10]),x=questions0,y=ww[10]),
                  go.Bar(name='{}'.format(nnn[11]),x=questions0,y=ww[11]),
                  go.Bar(name='{}'.format(nnn[12]),x=questions0,y=ww[12]),
                  go.Bar(name='{}'.format(nnn[13]),x=questions0,y=ww[13]),
                  go.Bar(name='{}'.format(nnn[14]),x=questions0,y=ww[14]),
                  go.Bar(name='{}'.format(nnn[15]),x=questions0,y=ww[15])
                  ])
    elif currenttype =='Health habits':
        fig9 = go.Figure(
            data=[go.Bar(name='{}'.format(nnn[0]),x=questions0,y=ww[0]),
                  go.Bar(name='{}'.format(nnn[1]),x=questions0,y=ww[1]),
                  go.Bar(name='{}'.format(nnn[2]),x=questions0,y=ww[2]),
                  go.Bar(name='{}'.format(nnn[3]),x=questions0,y=ww[3]),
                  go.Bar(name='{}'.format(nnn[4]),x=questions0,y=ww[4]),
                  go.Bar(name='{}'.format(nnn[5]),x=questions0,y=ww[5]),
                  go.Bar(name='{}'.format(nnn[6]),x=questions0,y=ww[6]),
                  go.Bar(name='{}'.format(nnn[7]),x=questions0,y=ww[7]),
                  go.Bar(name='{}'.format(nnn[8]),x=questions0,y=ww[8]),
                  go.Bar(name='{}'.format(nnn[9]),x=questions0,y=ww[9]),
                  go.Bar(name='{}'.format(nnn[10]),x=questions0,y=ww[10]),
                  go.Bar(name='{}'.format(nnn[11]),x=questions0,y=ww[11])
                  ])
    else:
        fig9 = go.Figure(
            data=[go.Bar(name='{}'.format(nnn[0]),x=questions0,y=ww[0]),
                  go.Bar(name='{}'.format(nnn[1]),x=questions0,y=ww[1]),
                  go.Bar(name='{}'.format(nnn[2]),x=questions0,y=ww[2]),
                  go.Bar(name='{}'.format(nnn[3]),x=questions0,y=ww[3]),
                  go.Bar(name='{}'.format(nnn[4]),x=questions0,y=ww[4])
                  ])
    fig9.update_layout(barmode='stack')
    return fig9
    


@app.callback(
    dash.dependencies.Output('fa', 'figure'),
    [dash.dependencies.Input('treemap', 'clickData'),
     dash.dependencies.Input('number0', 'value')
     ]
    )
def update_fa_figure(clickData, number0):        
    global currenttype
    if clickData:
        if clickData['points'][0]['label'] in types:
            currenttype = clickData['points'][0]['label']
        #fa graph
    if(currenttype in types):
        df_type=fa_preprocess(currenttype, number0)
        columns=np.arange(0, number0)
        dimensions=[]
        for col in columns:
            dimensions.append("Column"+str(col))
        df_type.columns=dimensions
        fig= px.parallel_coordinates(df_type, dimensions=dimensions, color_continuous_scale=px.colors.diverging.Tealrose,
                              color_continuous_midpoint=2)
            
    return fig    

@app.callback(
    dash.dependencies.Output('heatmap', 'figure'),
    [dash.dependencies.Input('treemap', 'clickData'),
     dash.dependencies.Input('number0', 'value')
     ]
    )
def update_heatmap(clickData, number0):
    global currenttype
    if clickData:
        if clickData['points'][0]['label'] in types:
            currenttype=clickData['points'][0]['label']
        #heatmap
    if(currenttype in types):
        df_cm=hp_preprocess(currenttype, number0)
        fig=go.Figure(data=go.Heatmap(
                z=df_cm,
                y=data0['short'].iloc[indexs[currenttype][0]:indexs[currenttype][1]]
            ))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

