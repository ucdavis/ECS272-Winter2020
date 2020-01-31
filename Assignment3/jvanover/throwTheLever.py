import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import subprocess


# load raw data
try:
    with open('__dataSet', 'rb') as f:
        df = pickle.load(f)
except:
    subprocess.call(['unzip', 'dataSet.zip'])
    with open('__dataSet', 'rb') as f:
        df = pickle.load(f) 

# rename columns for prettier labels:
df.rename(columns={'nkill': 'Deaths',
                    'country' : 'Country Code',
                    'country_txt' : 'Country',
                    'city' : 'City',
                    'attacktype1_txt' : 'Attack Type',
                    'targtype1_txt' : 'Target Type',
                    'success' : 'Successful'
                }, inplace=True
)

# clean data of NaNs
df['Deaths'].fillna(0, inplace=True)
df['summary'].fillna("", inplace=True)

# replace Successful 0 and 1 with No and Yes
df['Successful'] = df['Successful'].replace("0", "No")
df['Successful'] = df['Successful'].replace("1", "Yes")

# cast columns of interest into desired data type
df['iyear'] = df['iyear'].astype('int32')
df['latitude'] = df['latitude'].astype('float64')
df['longitude'] = df['longitude'].astype('float64')
df['Deaths'] = df['Deaths'].astype('int32')
df['marker_size'] = df['Deaths'] + 1

# replace country names with modern equivalents
df['Country'] = df['Country'].to_frame().replace("East Germany (GDR)", "Germany")
df['Country'] = df['Country'].to_frame().replace("West Germany (FRG)", "Germany")
df['Country'] = df['Country'].to_frame().replace("South Vietnam", "Vietnam")
df['Country'] = df['Country'].to_frame().replace("Soviet Union", "Russia")
df['Country'] = df['Country'].to_frame().replace("People's Republic of the Congo", "Democratic Republic of the Congo")
df['Country'] = df['Country'].to_frame().replace("Yugoslavia", "Serbia")
df['Country'] = df['Country'].to_frame().replace("Serbia-Montenegro", "Serbia")

# load pre-processed aggregated data set, or generate it
try:
    with open("__dataSetAggregate", 'rb') as f:
        df_aggregate = pickle.load(f)
except:
    df_aggregate_list = []

    import country_converter as coco
    for year in df['iyear'].unique():
        for country in df['country_txt'].unique():
            temp = df[(df.country_txt==country) & (df.iyear==year)]
            if not temp.empty:
                df_aggregate_list.append({'iyear': year,
                                        'Country' : country,
                                        'country_code': coco.convert(names=[country], to='ISO3', not_found=None),
                                        'Attacks' : len(temp)})

    # create dataframe of aggregated data
    df_aggregate = pd.DataFrame(data=df_aggregate_list, columns=['iyear', 'Country', 'country_code', 'Attacks'])

    # remove NaNs
    df_aggregate.dropna(inplace=True)

    # save dataFrame
    with open("__dataSetAggregate", 'wb') as f:
        pickle.dump(df_aggregate, f)


def renderVisualization():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    styles = {
        'pre': {
            'border': 'thin lightgrey solid',
            'font-size' : 'large',
            'width' : '80%'
        },
    }

    app.layout = html.Div([
        html.Div(html.H1("Terror Over the Years")),

        html.Div(html.H4("explore by selecting year on the slider, a country from the world map, or a specific attack from the focused map")),

        html.Div([
            html.Div([
                dcc.Graph(id='map-with-slider',)
            ], className="six columns"),

            html.Div([
                dcc.Graph(id='focus-map')
            ], className="six columns"),
        ], className="row"),

        dcc.Slider(
            id='year-slider',
            min=df['iyear'].min(),
            max=df['iyear'].max(),
            value=2002,
            marks={str(year): str(year) for year in df['iyear'].unique()},
            step=None
        ),

        html.Div([
            html.Div([
                dcc.Graph(id='parallel-diagram')
            ], className="six columns"),

            html.Div([
                html.H3("Summary Details (if available)"),
                html.P(id='summary-info', style=styles['pre'])
            ], className="six columns")
        ], className="row")
    ])

    # callback to update the overall choropleth world map
    @app.callback(
        Output('map-with-slider', 'figure'),
        [Input('year-slider', 'value')])
    def update_figure(selected_year):
        return px.choropleth(df_aggregate[df_aggregate.iyear == selected_year],
                                locations="country_code",
                                color="Attacks",
                                hover_name="Country",
                                hover_data=['Attacks'],
                                projection="natural earth",
                            )

    # callback to update the summary info box
    @app.callback(
        Output('summary-info', 'children'),
        [Input('focus-map', 'clickData')]
    )
    def update_summary(click_data):

        if click_data:
            eventid = click_data["points"][0]["customdata"][-1]
        else:
            return "Select a country in the world map on the top left to view it in more detail above. Select individual points from above to see a summary of the attack here. Select a year to observe with the slider."

        row = df[df.eventid == eventid]

        if row['summary'].iloc[0] == "":
            return "No summary for the attack in {}, {} on {}/{}/{}. Try another selection.".format(row['City'].iloc[0], row['Country'].iloc[0], row['imonth'].iloc[0], row['iday'].iloc[0], row['iyear'].iloc[0])
        else:
            return "{}, {} on {}".format(row['City'].iloc[0], row['Country'].iloc[0], row['summary'].iloc[0])


    # callback to update the local country map and Sankey diagram
    @app.callback(
        [Output('focus-map', 'figure'),
        Output('parallel-diagram', 'figure')],
        [Input('year-slider', 'value'),
        Input('map-with-slider', 'clickData')])
    def update_map(selected_year, click_data):

        # get click data or set to default
        if click_data:
            selected_country = click_data["points"][0]["hovertext"]
        else:
            selected_country = "United States"

        df_selected = df[(df.Country == selected_country) & (df.iyear == selected_year)]

        # set zoom level
        if df_selected.empty:
            zoom_region = "world"
        else:
            zoom_region = df_selected.iloc[0]['region_txt']

            if zoom_region == "Central America & Carribbean" or zoom_region == "North America":
                zoom_region = "north america"
            elif zoom_region == "South America":
                zoom_region = "south america"
            elif zoom_region == "Australasia & Oceania":
                zoom_region = "world"
            elif "europe" in zoom_region.lower():
                if selected_country == "Russia":
                    zoom_region = "world"
                else:
                    zoom_region = "europe"
            elif zoom_region == "Middle East & North Africa":
                if selected_country in ['Egypt', 'Algeria', 'Morocco', 'Western Sahara', 'Tunisia', 'Libya']:
                    zoom_region = "africa"
                elif selected_country in ['Jordan', 'Lebanon', 'Turkey', 'Iran', 'South Yemen', 'Israel', 'Kuwait', 'West Bank and Gaza Strip', 'North Yemen', 'Syria', 'United Arab Emirates', 'Iraq','Saudi Arabia', 'Bahrain','Qatar', 'Yemen']:
                    zoom_region = "asia"
                else:
                    zoom_region = "world"
            elif "asia" in zoom_region.lower():
                zoom_region = "asia"
            elif "africa" in zoom_region.lower():
                zoom_region = "africa"
            else:
                zoom_region = 'world'

        return px.scatter_geo(df_selected,
                                lat='latitude',
                                lon='longitude',
                                color='Deaths',
                                hover_name='Country',
                                hover_data=['City', 'Deaths', 'eventid'],
                                size='marker_size',
                                projection='equirectangular',
                                color_continuous_scale="redor",
                                scope = zoom_region
                                ), px.parallel_categories(df_selected, 
                                                            dimensions=['Successful', 'Attack Type','Target Type'],
                                                            title={
                                                                'text' : "Terrorist attacks in {} in the year {}".format(selected_country, selected_year),
                                                                'y': 0.9,
                                                                'x' : 0.5,
                                                                'xanchor' : 'center',
                                                                'yanchor' : 'top'
                                                            }
                                                        )

    app.run_server(debug=True)

if __name__ == '__main__':
    renderVisualization()