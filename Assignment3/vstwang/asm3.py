# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('/Users/Vincent/Google 云端硬盘/MS/Winter/ECS272 Info Visu/ECS272-Winter2020/Assignment3/datasets/Los_Angeles_International_Airport_-_Passenger_Traffic_By_Terminal.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='ECS272 Assignment 3'),
    html.H2(children='Shuotong Wang | 917809530'),

    html.Div([
        html.P(['The visualization consists of two views:',
               html.Br(), '1. A pie chart showing Domestic vs international Departures and Arrivals',
               html.Br(), '2. A Stream graph showing the number of passengers of different terminals vs time.'
               ])
    ]),

    # Checkboxes - Terminal Selection
    html.Label('Terminals'),
    dcc.Checklist(
        id='terminal_checkbox',
        options=[
            {'label': 'Imperial Terminal', 'value': 'Imperial Terminal'},
            {'label': 'Misc. Terminal', 'value': 'Misc. Terminal'},
            {'label': 'Terminal 1', 'value': 'Terminal 1'},
            {'label': 'Terminal 2', 'value': 'Terminal 2'},
            {'label': 'Terminal 3', 'value': 'Terminal 3'},
            {'label': 'Terminal 4', 'value': 'Terminal 4'},
            {'label': 'Terminal 5', 'value': 'Terminal 5'},
            {'label': 'Terminal 6', 'value': 'Terminal 6'},
            {'label': 'Terminal 7', 'value': 'Terminal 7'},
            {'label': 'Terminal 8', 'value': 'Terminal 8'},
            {'label': 'Tom Bradley International Terminal', 'value': 'Tom Bradley International Terminal'}
        ],
        value=['Terminal 1'],
        labelStyle={'display': 'inline-block'},
    ),

    # Year Range Slider
    html.Label('Date'),
    dcc.RangeSlider(
            id='year_slider',
            min=2006,
            max=2019,
            step=None,
            marks={i: 'Year {}'.format(i) if i == 2006 else str(i) for i in range(2006, 2020)},
            value=[2012, 2015],
    ),

    # Month Range Slider
    dcc.RangeSlider(
            id='month_slider',
            min=1,
            max=12,
            step=None,
            marks={i: 'Month {}'.format(i) if i == 1 else str(i) for i in range(1, 13)},
            value=[1, 13],
    ),

    # Simple Graph - Pie Charts, Proportion of Domestic and int'l, and Arrives & Departures
    html.Label('Arrivals and/or Departure'),
    dcc.Checklist(
        id='arrive_checkbox',
        options=[
            {'label': 'Arrival', 'value': 'Arrival'},
            {'label': 'Departure', 'value': 'Departure'}
        ],
        value=['Arrival'],
        labelStyle={'display': 'inline-block'},
    ),

    dcc.Graph(id='pie_chart',
              figure=go.Figure(
                  data=[go.Pie(labels=['Domestic', 'International'],
                               values=['4234', '1864'])],
                  layout=go.Layout(
                      title='Domestic vs Int\'l Passengers'))),

    dcc.Graph(id='stream_chart'),

    # html.Label('Stream Plot of LAX Passenger Arrivals & Departures'),
    # dcc.Graph(id='stream_chart',
    #           figure=go.Figure(
    #               data=[go.Scatter(x=[1, 2, 3, 4], y=[0, 2, 3, 5], fill='tozeroy')]
    #           )),
])


# Callbacks
@app.callback(
    [Output('pie_chart', 'figure'),
     Output('stream_chart', 'figure')],
    [Input('month_slider', 'value'),
     Input('year_slider', 'value'),
     Input('terminal_checkbox', 'value'),
     Input('arrive_checkbox', 'value')])
def pie_chart(selected_month, selected_year, selected_terminal, selected_arrival):

    if selected_month and selected_year and selected_terminal and selected_arrival:

        months = [x for x in range(selected_month[0], selected_month[-1] + 1)]
        years = [x for x in range(selected_year[0], selected_year[-1] + 1)]
        column_names = ['DataExtractDate', 'ReportPeriod', 'Terminal', 'Arrival_Departure', 'Domestic_International', 'Passenger_Count']

        # Filter date - year
        f_y_df = pd.DataFrame(columns=column_names)
        for year in years:
            f_y_df = f_y_df.append(df[df['ReportPeriod'].str.slice(start=6, stop=10) == (str(year))], ignore_index=True)

        # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #     print(f_y_df)

        # Filter date - month
        f_m_df = pd.DataFrame(columns=column_names)
        for month in months:
            month = str("%02d" % (month,))
            f_m_df = f_m_df.append(f_y_df[f_y_df['ReportPeriod'].str.slice(start=0, stop=2) == (str(month))], ignore_index=True)
        del f_y_df

        # Filter Terminal
        f_t_df = pd.DataFrame(columns=column_names)
        for t in selected_terminal:
            f_t_df = f_t_df.append(f_m_df[f_m_df['Terminal'].str.contains(t)], ignore_index=True)
        del f_m_df

        # Filter Arrival / Departure
        f_a_df = pd.DataFrame(columns=column_names)
        for s in selected_arrival:
            f_a_df = f_a_df.append(f_t_df[f_t_df['Arrival_Departure'].str.contains(s)], ignore_index=True)
        del f_t_df

        # Simple Visualization - Pie Chart Data
        dom_data = sum(f_a_df[f_a_df['Domestic_International'].str.contains('Domestic')]['Passenger_Count'])
        int_data = sum(f_a_df[f_a_df['Domestic_International'].str.contains('International')]['Passenger_Count'])

        # Advanced Visualization - Stream Chart
        # x value - time
        # y value - Passenger Count
        data = []
        term = []  # terminal name
        x_value = None
        for i, t in enumerate(selected_terminal):
            this_y = f_a_df[f_a_df['Terminal'].str.contains(t)]
            this_y = this_y.groupby(['ReportPeriod', 'Terminal'], as_index=False)['Passenger_Count'].sum()
            this_y['ReportPeriod'] = pd.to_datetime(this_y['ReportPeriod'], format='%m/%d/%Y %H:%M:%S %p')
            this_y = this_y.sort_values('ReportPeriod').reset_index(drop=True)
            this_y['ReportPeriod'] = this_y['ReportPeriod'].apply(lambda x: x.strftime("%m/%d/%Y"))
            x_value = list(dict.fromkeys(this_y['ReportPeriod']))

            data.append(this_y['Passenger_Count'].values)
            term.append(t)

        hover_data = data.copy()

        for i in range(1, len(data)):
            data[i] = [sum(x) for x in zip(data[i], data[i-1])]

        print(hover_data)

        graph_data = []
        for i in range(len(data)):
            this_data = {
                "id": t,
                "fill": "tonexty",
                "line": {
                    "shape": "spline",
                    "width": 0
                },
                "name": term[i],
                "type": "scatter",
                "x": x_value,
                "y": data[i],
                "hovertext": hover_data[i],
                "hoverinfo": 'text'
            }
            graph_data.append(this_data)

        return [{
                'data': [go.Pie(labels=['Domestic', 'International'],
                                values=[dom_data, int_data])],
                'layout': go.Layout(title='Pie Chart of Proportion of Domestic vs International Passengers'),
                },
                {
                'data': graph_data,
                'layout': dict(
                    title="Stream Plot of the Number of Arrivals and/or Departures in LAX",
                    xaxis={
                        "ticks": "outside",
                        "mirror": True,
                        "ticklen": 20,
                        "showgrid": False,
                        "showline": True,
                        "tickfont": {
                            "size": 11,
                        },
                        "tickwidth": 1,
                        "showticklabels": True
                    },
                    yaxis={
                        "ticks": "outside",
                        "title": "",
                        "mirror": True,
                        "ticklen": 5,
                        "showgrid": False,
                        "showline": True,
                        "tickfont": {
                            "size": 11,
                        },
                        "zeroline": True,
                        "tickwidth": 1,
                        "showticklabels": True
                    },

                )
                }]
    return None


if __name__ == '__main__':
    app.run_server(debug=False)
