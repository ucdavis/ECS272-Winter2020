import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv('https://data.lacity.org/resource/g3qu-7q2u.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Add two columns to show the report year and report month
ReportYears = []
ReportMonths = []
print df.loc[0, 'reportperiod'][1:4]
for i in range(0, df.shape[0]):
    date = df.loc[i, 'reportperiod']
    ReportYears.append(int(date[0:4]))
    ReportMonths.append(int(date[5:7]))
df['ReportYear'] = ReportYears
df['ReportMonth'] = ReportMonths
report_years = df['ReportYear'].unique()
report_dates = df['reportperiod'].unique()

app.layout = html.Div([
    html.Div([

        # A visual interface widget of DropDown for users to choose the report year
        html.Div([
            dcc.Dropdown(
                id='report-year',
                options=[{'label': i, 'value': i} for i in report_years],
                value=report_years[0]
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        # A visual interface widget of RadioItem for users to choose Domestic/International flight
        html.Div([
            dcc.RadioItems(
                id='domestic-international',
                options=[{'label': i, 'value': i} for i in ['Domestic', 'International']],
                value='Domestic',
                labelStyle={'display': 'inline-block'}
            ),

            # A visual interface widget of RadioItem for users to choose Arrival/Departure flight
            dcc.RadioItems(
                id='arrival-departure',
                options=[{'label': i, 'value': i} for i in ['Arrival', 'Departure']],
                value='Arrival',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    # The first visualization view to show the Los Angeles International Airport - Passenger Traffic By Terminal
    dcc.Graph(id='first-view'),

    # A visual interface widget of Slider for users to choose the report month
    dcc.Slider(
        id='month--slider',
        min=df['ReportMonth'].min(),
        max=df['ReportMonth'].max(),
        value=df['ReportMonth'].min(),
        marks={str(month): str(month) for month in df['ReportMonth'].unique()},
        step=None
    ),

    html.Div([

            # A visual interface widget of DropDown for users to choose the report date
            dcc.Dropdown(
                id='ReportDate',
                options=[{'label': i, 'value': i} for i in report_dates],
                value=report_dates[0]
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

    # The second visualization view to show the Los Angeles International Airport - Passenger Traffic By
    #  Domestic/International, Arrival/Departure and Terminal
    dcc.Graph(id='second-view'),

])


@app.callback(
    Output('first-view', 'figure'),
    [Input('report-year', 'value'),
     Input('domestic-international', 'value'),
     Input('arrival-departure', 'value'),
     Input('month--slider', 'value')])
def update_figure(report_year_value, domestic_international_value, arrival_departure_value, month_value):
    filtered_df = df[df.ReportYear == report_year_value]
    filtered_df = filtered_df[filtered_df.domestic_international == domestic_international_value]
    filtered_df = filtered_df[filtered_df.arrival_departure == arrival_departure_value]
    filtered_df = filtered_df[filtered_df.ReportMonth == month_value]

    return {
        'data': [
            {'x': filtered_df['terminal'], 'y': filtered_df['passenger_count'],
             'type': 'bar', 'name': 'Passenger Count'}],
        'layout': {
            'title': 'Los Angeles International Airport - Passenger Traffic By Terminal'
        }
    }


# Define the labels used in the Sankey plot.
sankey_labels = ["Domestic", "International", "Arrival", "Departure"]
# Define the color of each label used in the Sankey plot.
colors = ["rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)", "rgba(44, 160, 44, 0.8)",
          "rgba(214, 39, 40, 0.8)", "rgba(148, 103, 189, 0.8)", "rgba(140, 86, 75, 0.8)",
          "rgba(227, 119, 194, 0.8)", "rgba(127, 127, 127, 0.8)", "rgba(188, 189, 34, 0.8)",
          "rgba(23, 190, 207, 0.8)", "rgba(31, 119, 180, 0.8)", "rgba(255, 127, 14, 0.8)",
          "rgba(44, 160, 44, 0.8)", "rgba(214, 39, 40, 0.8)", "rgba(148, 103, 189, 0.8)"]
terminals = df["terminal"].unique().tolist()
for terminal in terminals:
    sankey_labels.append(terminal)
print sankey_labels


@app.callback(
    Output('second-view', 'figure'),
    [Input('ReportDate', 'value')])
def update_graph(date_value):
    filtered_dff = df[df.reportperiod == date_value]
    # Define the links between the labels used in the Sankey plot.
    sankey_links = dict(source=[0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                        target=[2, 3, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
    sankey_links['value'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for j in range(0, filtered_dff.shape[0]):
        # Update the value of the related Sankey links.
        if filtered_dff.iloc[j, 4] == "Domestic":
            if filtered_dff.iloc[j, 3] == "Arrival":
                sankey_links['value'][0] += filtered_dff.iloc[j, 5]
                terminal_location = terminals.index(filtered_dff.iloc[j, 2])
                sankey_links['value'][terminal_location + 4] += filtered_dff.iloc[j, 5]
            else:
                sankey_links['value'][1] += filtered_dff.iloc[j, 5]
                terminal_location = terminals.index(filtered_dff.iloc[j, 2])
                sankey_links['value'][terminal_location + 15] += filtered_dff.iloc[j, 5]
        else:
            if filtered_dff.iloc[j, 3] == 'Arrival':
                sankey_links['value'][2] += filtered_dff.iloc[j, 5]
                terminal_location = terminals.index(filtered_dff.iloc[j, 2])
                sankey_links['value'][terminal_location + 4] += filtered_dff.iloc[j, 5]
            else:
                sankey_links['value'][3] += filtered_dff.iloc[j, 5]
                terminal_location = terminals.index(filtered_dff.iloc[j, 2])
                sankey_links['value'][terminal_location + 15] += filtered_dff.iloc[j, 5]
    fig = go.Figure(data=[go.Sankey(node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5),
                                              label=sankey_labels, color=colors), link=sankey_links)])
    fig.update_layout(
        hovermode='x',
        title_text="Los Angeles International Airport -"
                   " Passenger Traffic By Domestic/International, Arrival/Departure and Terminal",
        font=dict(size=12, color='Black'))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
