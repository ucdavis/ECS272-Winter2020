function OnScatterVisSelectionChanged(value) {
    scatter_vis.color_by = value

    //scatter_vis.update(null)
    scatter_vis.init()
}