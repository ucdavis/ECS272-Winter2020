import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

import plotly.express as px
from iso_alpha import ccode

import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('../datasets/globalterrorismdb_0718dist.csv', encoding="ISO-8859-1")

dropdown_options = [
    dict(
        label=country,
        value=country
    ) for country in sorted(df.country_txt.unique())
]
dropdown_options.append({
    'label': 'Global',
    'value': 'Global'
})

ccode = {v: k for k, v in ccode.items()}

app.layout = html.Div(
    [
        html.H1(
            children=['Assignment 3, Jiayu Liu']
        ),
        
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id='country_dropdown',
                            options=dropdown_options,
                            value='Global',
                            style=dict(
                                width='540px'
                            )
                        ),

                        dcc.RadioItems(
                            id='display_method',
                            options=[
                                {'label': 'line', 'value': 'line'},
                                {'label': 'bar', 'value': 'bar'},
                            ],
                            value='bar',
                            style=dict(
                                width='540px'
                            )
                        ),

                        dcc.Graph(
                            id='events_overtime',
                            style=dict(
                                width='540px'
                            )
                        ), 
                    ], 
                    style=dict(
                        width='540px'
                    )
                ),

                html.Div(
                    [
                        dcc.Dropdown(
                            id='year_selection',
                            options=sorted([dict(
                                label=year,
                                value=year
                            ) for year in df['iyear'].unique()], key=lambda x: x['value'], reverse=True),
                            value=df['iyear'].max(),
                            style=dict(
                                width='540px'
                            )
                        ),

                        dcc.Graph(
                            id='country_ratio',
                        ),
                    ],
                    style=dict(
                        width='540px',
                    )
                ),
            ],
            style=dict(
                textAlign='center',
                justifyContent='center',
                alignItems='center',
                display='flex'
            )
        ),

        html.Div(
            [
                dcc.Dropdown(
                    id='region_dropdown',
                    options=[{'label': region, 'value': region} for region in df.region_txt.unique()],
                    value='North America',
                ),

                dcc.Dropdown(
                    id='year_dropdown',
                    options=[{'label': year, 'value': year} for year in df.iyear.unique()],
                    value=df.iyear.unique().max(),
                ), 

                dcc.Graph(
                    id='sankey'
                )
            ],
            style=dict(
                width='1080px',
                margin='auto',
                borderColor='#FFFFFF'
            )
        ),
        
        html.Div(
            [
                dcc.Graph(
                    id='map',
                    style=dict(
                        width='1400px',
                        height='600px'
                    )
                ),
                dcc.Slider(
                    id='year-slider',
                    min=df['iyear'].min(),
                    max=df['iyear'].max(),
                    value=df['iyear'].max(),
                    marks={str(year): str(year) for year in df['iyear'].unique()},
                    step=None
                )
            ],
            style=dict(
                width='1400px',
                margin='auto'
            )
        )
    ],
    style=dict(
        width='1400px',
        textAlign='center',
        justifyContent='center',
        alignItems='center',
        margin='auto'
    )
)

@app.callback(
    Output('events_overtime', 'figure'),
    [
        Input('country_dropdown', 'value'),
        Input('display_method', 'value')
    ]
)
def update_overtime(country, dm):
    data = None
    layout = None
    years = df['iyear'].unique()
    if country == 'Global':
        # there's order problem in the dataset
        # link year with amount and sort them
        mapping = [(year, len(df[df.iyear == year])) for year in years]
        mapping.sort(key=lambda x: x[0])
        data = [
            dict(
                x=[e[0] for e in mapping],
                y=[e[1] for e in mapping],
                type=dm
            )
        ]
        layout = {
            'title': 'Global terrorism overtime'
        }
    else:
        mapping = [(year, len(df[(df.iyear == year) & (df.country_txt == country)])) for year in years]
        mapping.sort(key=lambda x: x[0])
        data = [
            dict(
                x=[e[0] for e in mapping],
                y=[e[1] for e in mapping],
                type=dm
            )
        ]
        layout = {
            'title': 'Terrorism in %s overtime' % country
        }
    return {
        'data': data,
        'layout': layout
    }

@app.callback(
    Output('country_ratio', 'figure'),
    [
        Input('year_selection', 'value')
    ]
)
def update_ratio(year):
    filtered_df = df[df.iyear == year]
    data = [
        dict(
            values=[len(filtered_df[filtered_df.country_txt == country]) for country in filtered_df.country_txt.unique()],
            type='pie',
            labels=filtered_df.country_txt.unique(),
            textinfo='none'
        )
    ]
    return {
        'data': data,
        'layout': dict(
            title='Ratio of each country in %s' % str(year)
        )
    }

@app.callback(
    Output('map', 'figure'),
    [
        Input('year-slider', 'value')
    ]
)
def update_map(year):
    filtered_df = df[df.iyear == year]
    locations = []
    events = []
    hover_name = []
    for country in filtered_df.country_txt.unique():
        if country in ccode:
            locations.append(ccode[country])
            events.append(len(filtered_df[filtered_df.country_txt == country]))
            hover_name.append(country)
    return px.choropleth(locations=locations, color=events, hover_name=hover_name, color_continuous_scale=px.colors.sequential.Plasma)

@app.callback(
    Output('sankey', 'figure'),
    [
        Input('region_dropdown', 'value'),
        Input('year_dropdown', 'value')
    ]
)
def update_sankey(region, year):
    filtered_df = df[(df.iyear == year) & (df.region_txt == region)]
    countries = filtered_df['country_txt'].unique()
    attack_type = filtered_df['attacktype1_txt'].unique()

    labels = [region] + list(countries) + list(attack_type)
    labels_mapping = {label: i for i, label in enumerate(labels)}

    region2country = [(
        labels_mapping[region],
        labels_mapping[country],
        len(filtered_df[filtered_df.country_txt == country])) for country in countries]
    
    country2attack = []
    for country in countries:
        new_df = filtered_df[filtered_df.country_txt == country]
        for attack in attack_type:
            country2attack.append((
                labels_mapping[country],
                labels_mapping[attack],
                len(new_df[new_df.attacktype1_txt == attack])
            ))

    link = region2country + country2attack
    return {
        'data': [
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color = "black", width = 0.5),
                    label=labels,
                    color='blue'
                ),
                link=dict(
                    source=[i[0] for i in link],
                    target=[i[1] for i in link],
                    value=[i[2] for i in link]
                )
            )
        ]
    }

if __name__ == '__main__':
    app.run_server(debug=True)