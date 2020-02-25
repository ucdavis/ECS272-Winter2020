from typing import List, Callable, Tuple

import plotly.graph_objects as go

from data_constants import feat_colors


def make_sankey(
    df,
    columns: List[str],
    should_highlight_node: Callable[[str, str], bool] = None
):
    node_maps = {}
    node_labels, node_colors = [], []
    link_srcs, link_tgts, link_vals, link_colors = [], [], [], []

    def make_label_for_val(kind, v):
        return v


    def make_node_for(field, val):
        if (field, val) not in node_maps:
            node_maps[(field, val)] = len(node_maps)
            label = make_label_for_val(field, val)
            node_labels.append(label)
            if should_highlight_node is None or not should_highlight_node(field, val):
                node_colors.append("grey")
            else:
                node_colors.append(feat_colors[field][val])

    # Make the leftmost nodes
    leftmost = df[columns[-1]].unique().tolist()
    for s in leftmost:
        make_node_for(columns[-1], s)

    def add_links(source_field, tgt_field):
        src_vals = df[source_field].unique()
        for src_val in src_vals:
            make_node_for(source_field, src_val)
            matches_src = (df[source_field] == src_val)
            for tgt_val in df[tgt_field].unique():
                make_node_for(tgt_field, tgt_val)
                num_in_link = len(df[matches_src & (df[tgt_field] == tgt_val)])
                if num_in_link > 0:
                    link_srcs.append(node_maps[(source_field, src_val)])
                    link_tgts.append(node_maps[(tgt_field, tgt_val)])
                    link_vals.append(num_in_link)
                    highlight_link = should_highlight_node is not None and \
                                     should_highlight_node(source_field, src_val) and \
                                     should_highlight_node(tgt_field, tgt_val)
                    link_colors.append("#555" if not highlight_link else "#000")

    for i in range(len(columns) - 1):
        add_links(columns[i], columns[i+1])

    return go.Sankey(
        node=dict(
            label=node_labels,
            color=node_colors
        ),
        link=dict(
            source=link_srcs,
            target=link_tgts,
            value=link_vals,
            #color="grey"
        )
    )
