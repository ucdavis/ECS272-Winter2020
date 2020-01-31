import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, datetime, base64


df = pd.read_csv(os.path.join('..', 'datasets', 'Police_Department_Incidents_-_Previous_Year__2016_.csv'))
# Create geomap
geo_map = px.scatter_mapbox(df, lat="Y", lon="X", hover_name="Time", hover_data=["Category", "Descript", "Resolution"],
                        color="Category", height=300, zoom = 11)
geo_map.update_layout(mapbox_style="carto-positron", width = 1500,
	height = 600, margin={"r":0,"t":0,"l":0,"b":0}, geo_scope='usa')
#Create parralell sets

def get_color(row):
	corresponding_colors = {"ARSON": "red", "LARCENY/THEFT": 'peru', "MISSING PERSON": "lime", "OTHER OFFENSES": 'purple', "TRESPASS": "orange", "SUSPICIOUS OCC": "lightyellow", "FRAUD": 'royalblue', "VEHICLE THEFT": 'maroon',
	"ASSAULT": 'pink', "NON-CRIMINAL": 'gold', "SECONDARY CODES": 'olivedrab', "DRUG/NARCOTIC": 'orangered', "RECOVERED VEHICLE": 'honeydew', "WARRANTS": 'fuchsia', 'SEX OFFENSES, NON FORCIBLE': 'aquamarine', 'TREA': 'darkslategray',
	"ROBBERY": 'mediumturquoise', "VANDALISM": 'plum', "PROSTITUTION": 'mediumorchid', "KIDNAPPING": 'grey', 'BURGLARY': 'firebrick', 'STOLEN PROPERTY': 'chocolate', 'WEAPON LAWS': 'powderblue', 'PORNOGRAPHY/OBSCENE MAT': 'tomato',
	'FORGERY/COUNTERFEITING': 'navy', 'LIQUOR LAWS': 'brown', 'SEX OFFENSES, FORCIBLE': 'peachpuff', 'LOITERING': 'linen', 'DISORDERLY CONDUCT': 'chartreuse', 'DRUNKENNESS': 'forestgreen', 'BRIBERY': 'mintcream',
	'EMBEZZLEMENT': 'yellow', 'EXTORTION': 'rosybrown', 'BAD CHECKS': 'palegoldenrod', 'FAMILY OFFENSES': 'papayawhip', 'RUNAWAY': 'orchid', 'DRIVING UNDER THE INFLUENCE': 'coral', 'GAMBLING': 'green', 'SUICIDE': 'aliceblue'}
	return corresponding_colors[row['Category']]

def get_time_of_day(row):
	hour = int(str(row['Time']).split(':')[0])
	if hour < 6:
		return 'Dawn'
	if hour < 12:
		return 'Morning'
	if hour < 18:
		return 'Afternoon'
	return 'Evening'

df['color'] = df.apply(lambda row: get_color(row), axis=1)
df['Time of Day'] = df.apply(lambda row: get_time_of_day(row), axis=1)
paralell_coordinates = px.parallel_categories(df, color='color', dimensions=['DayOfWeek', 'PdDistrict', 'Time of Day'])

# Key image
img_width = 1600
img_height = 900
scale_factor = 0.5

key = go.Figure()

key.add_trace(
	go.Scatter(
		x=[0, img_width * scale_factor],
		y=[0, img_height * scale_factor],
		mode="markers",
		marker_opacity=0
	)
)

key.add_layout_image(
	go.layout.Image(
		x=0,
		sizex=img_width * scale_factor,
		y=img_height * scale_factor,
		sizey=img_height * scale_factor,
		xref="x",
		yref="y",
		opacity=1.0,
		layer="below",
		sizing="stretch",
		source="https://i.imgur.com/RDHaF6V.png")
	)

key.update_xaxes(
	visible=False,
	range=[0, img_width * scale_factor]
)

key.update_yaxes(
	visible=False,
	range=[0, img_height * scale_factor],
	# the scaleanchor attribute ensures that the aspect ratio stays constant
	scaleanchor="x"
)

key.update_layout(
	width=img_width * scale_factor,
	height=img_height * scale_factor,
	margin={"l": 0, "r": 0, "t": 0, "b": 0},
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
	# Header
	html.H3('San Fransisco Crime'),
	# Add geo-map to app
	dcc.Graph(
		id='geo_map',
		figure=geo_map
	),
	# Time of day slider
	html.Label('Time of Day:'),
	dcc.Slider(
		id='time_slider',
		min=0,
		max=23,
		step=1,
		value=12),
	# Add paralell coordinates graph to app
	dcc.Graph(
		id='paralell_coordinates',
		figure=paralell_coordinates
	),
	#Crime checklist
	dcc.Checklist(
		id='crime_category',
		options=[
		{'label': 'Assault', 'value': 'ASSAULT'},
		{'label': 'Arson', 'value': 'ARSON'},
		{'label': 'Bad Checks', 'value': 'BAD CHECKS'},
		{'label': 'Bribery', 'value': 'BRIBERY'},
		{'label': 'Disorderly Conduct', 'value': 'DISORDERLY CONDUCT'},
		{'label': 'DUI', 'value': 'DRIVING UNDER THE INFLUENCE'},
		{'label': 'Drugs', 'value': 'DRUGS/NARCOTIC'},
		{'label': 'Drunkenness', 'value': 'DRUNKENNESS'},
		{'label': 'Embezzlement', 'value': 'EMBEZZLEMENT'},
		{'label': 'Extortion', 'value': 'EXTORTION'},
		{'label': 'Family Offenses', 'value': 'FAMILY OFFENSES'},
		{'label': 'Forgery', 'value': 'FORGERY/COUNTERFEITTING'},
		{'label': 'Fraud', 'value': 'FRAUD'},
		{'label': 'Gambling', 'value': 'GAMBLING'},
		{'label': 'Kidnapping', 'value': 'KIDNAPPING'},
		{'label': 'Larency/Theft', 'value': 'LARCENY/THEFT'},
		{'label': 'Liquor Laws', 'value': 'LIQUOR LAWS'},
		{'label': 'Loitering', 'value': 'LOITERING'},
		{'label': 'Missing Person', 'value': 'MISSING PERSON'},
		{'label': 'Non-Criminal', 'value': 'NON-CRIMINAL'},
		{'label': 'Other Offenses', 'value': 'OTHER OFFENSES'},
		{'label': 'Pornography', 'value': 'PORNOGRAPHY/OBSCENE MAT'},
		{'label': 'Prostitution', 'value': 'PROSTITUTION'},
		{'label': 'Recovered Vehicle', 'value': 'RECOVERED VEHICLE'},
		{'label': 'Robbery', 'value': 'ROBBERY'},
		{'label': 'Runaway', 'value': 'RUNAWAY'},
		{'label': 'Secondary Codes', 'value': 'SECONDARY CODES'},
		{'label': 'Sex Offenses; Forcible', 'value': 'SEX OFFENSES, FORCIBLE'},
		{'label': 'Sex Offenses; Non-Forcible', 'value': 'SEX OFFENSES, NON FORCIBLE'},
		{'label': 'Stolen Property', 'value': 'STOLEN PROPERTY'},
		{'label': 'Suicide', 'value': 'SUICIDE'},
		{'label': 'Suspicious', 'value': 'SUSPICIOUS OCC'},
		{'label': 'Trea', 'value': 'TREA'},
		{'label': 'Tresspassing', 'value': 'TRESSPASS'},
		{'label': 'Vandalism', 'value': 'VANDALISM'},
		{'label': 'Vehicle Theft', 'value': 'VEHICLE THEFT'},
		{'label': 'Warrants', 'value': 'WARRANTS'},
		{'label': 'Weapon Laws', 'value': 'WEAPON LAWS'}],
		value = ['DRUNKENNESS'],
		labelStyle={'display': 'inline-block'}
		),
	
	dcc.Graph(
		figure = key)

	])

@app.callback(
    dash.dependencies.Output('geo_map', 'figure'),
    [dash.dependencies.Input('time_slider', 'value')])
def update_geomap(value):
	# New dataframe to make the map out of
	df = pd.read_csv(os.path.join('..', 'datasets', 'Police_Department_Incidents_-_Previous_Year__2016_.csv'))
	time_list = get_time_list(str(value))
	df = df[df.Time.isin(time_list)]
	fig = px.scatter_mapbox(df, lat="Y", lon="X", hover_name="Time", hover_data=["Category", "Descript", "Resolution"],
                        color="Category", height=300, zoom = 11)
	fig.update_layout(mapbox_style="carto-positron", width = 1500,
		height = 600, margin={"r":0,"t":0,"l":0,"b":0}, geo_scope='usa')
	return fig

@app.callback(
    dash.dependencies.Output('paralell_coordinates', 'figure'),
    [dash.dependencies.Input('crime_category', 'value')])
def update_parralel(value):
	# New dataframe to make the map out of
	df = pd.read_csv(os.path.join('..', 'datasets', 'Police_Department_Incidents_-_Previous_Year__2016_.csv'))
	df['color'] = df.apply(lambda row: get_color(row), axis=1)
	df['Time of Day'] = df.apply(lambda row: get_time_of_day(row), axis=1)
	df = df[df.Category.isin(value)]
	fig = px.parallel_categories(df, color='color', dimensions=['DayOfWeek', 'PdDistrict', 'Time of Day'])
	fig.update_layout(showlegend=True)
	return fig

# Return a list of strings such that the elements in 
def get_time_list(hour):
	l = []
	if int(hour) < 10:
		hour = '0' + hour
	for i in range(60):
		s = str(i)
		if i < 10:
			s = '0' + s
		s = hour + ':' + s
		l.append(s)
	return l

if __name__ == '__main__':
    app.run_server(debug=True)