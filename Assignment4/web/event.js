function OnScatterVisSelectionChanged(value) {
    scatter_vis.color_by = value

    scatter_vis.update(null)
    //scatter_vis.init()
}

function OnSanKeyVisSelectionChanged(value, id) {
    var selects = document.getElementsByClassName('sankey-select');

    var columns = []
    for(const select of selects) {
        if (select.value === "none")
            continue

        if (columns.indexOf(select.value) >= 0) {
            this.value = 'none'
            return
        }
        columns.push(select.value)
    }

    alluvial_vis.columns = columns
    alluvial_vis.init()
}