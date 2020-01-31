# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

print("Loading Data")
df = pd.read_csv("../datasets/globalterrorismdb_0718dist.csv", encoding="ISO-8859-1")


def get_bar_data(selected_regions=None):
    filtered_df = df
    if selected_regions is not None:
        filtered_df = filtered_df[filtered_df['region_txt'].isin(selected_regions)]
    by_year = filtered_df['iyear']
    year_counts = by_year.value_counts()
    return [
        {"x": year_counts.index.tolist(), "y": year_counts.values.tolist(), 'type': 'bar'}
    ]


def build_region_dropdown():
    regions = df['region_txt'].unique()
    region_dicts = [
        {'label': region, 'value': region}
        for region in regions.tolist()
    ]
    return dcc.Dropdown(
        options=region_dicts,
        value=regions.tolist(),
        multi=True,
        id="region-dropdown",
    )


def build_year_select():
    min_year, max_year = min(df['iyear']), max(df['iyear'])
    return html.Div(
        dcc.RangeSlider(
            id='range-slider',
            min=min_year,
            max=max_year,
            value=[min_year, max_year],
            marks={
                year: {"label": f"{year}"}
                for year in range(min_year, max_year+1, 5)
            }
        ),
        style={"margin": "20px"}
    )


def get_sankey_data(year_range=None):
    node_maps = {}
    node_labels = []
    link_srcs, link_tgts, link_vals = [], [], []

    filtered_df = df

    if year_range:
        start_year, end_year = year_range
        years = filtered_df['iyear']
        filtered_df = filtered_df[(years >= start_year) & (years <= end_year)]

    def make_label_for_val(kind, v):
        if kind == "success":
            return f'Successful' if v == 1 else "Not Successful"
        else:
            return v

    success_vals = filtered_df['success'].unique().tolist()
    for s in success_vals:
        l = make_label_for_val("success", s)
        node_maps[l] = len(node_maps)
        node_labels.append(l)


    def add_links(source_field, tgt_field):
        src_vals = filtered_df[source_field].unique()
        for src_val in src_vals:
            src_label = make_label_for_val(source_field, src_val)
            if source_field not in node_maps:
                node_maps[src_label] = len(node_maps)
                node_labels.append(src_label)
            matches_src = (filtered_df[source_field] == src_val)
            for tgt_val in filtered_df[tgt_field].unique():
                tgt_label = make_label_for_val(tgt_field, tgt_val)
                num_in_link = len(filtered_df[matches_src & (filtered_df[tgt_field] == tgt_val)])
                if num_in_link > 0:
                    link_srcs.append(node_maps[src_label])
                    link_tgts.append(node_maps[tgt_label])
                    link_vals.append(num_in_link)

    add_links("attacktype1_txt", "success")
    add_links("region_txt", "attacktype1_txt")

    return [go.Sankey(
        node=dict(
            label=node_labels,
            color="blue"
        ),
        link=dict(
            source=link_srcs,
            target=link_tgts,
            value=link_vals
        )
    )]



app.layout = html.Div(children=[
    html.H1(children='Vis Assignment 3. David Gros'),
    html.H2(children='Data from Global Terrorism Dataset'),
    html.H3("'Basic Visualization'. Barplot of events by year"),
    html.Label("Regions"),
    build_region_dropdown(),
    dcc.Graph(
        id='bar-graph'
    ),
    html.Hr(),
    html.H3("'Advanced Visualization'. Sankey of successful events"),
    html.Label("Year"),
    build_year_select(),
    html.Br(),
    dcc.Graph(
        id='sankey-graph'
    ),
])


@app.callback(
    Output('bar-graph', 'figure'),
    [Input('region-dropdown', 'value')])
def update_bar_chart(selected_regions):
    return {
        'data': get_bar_data(selected_regions),
        'layout': {
            'title': 'Number of events',
            'xaxis': {
                "title": "Year"
            },
            'yaxis': {
                "title": "Number of Terrorist Events",
                "range": (0, 20_000)
            }
        }
    }


@app.callback(
    Output('sankey-graph', 'figure'),
    [Input('range-slider', 'value')])
def update_bar_sankey(selected_years):
    return {
        'data': get_sankey_data(selected_years),
    }


if __name__ == '__main__':
    app.run_server(debug=True)
