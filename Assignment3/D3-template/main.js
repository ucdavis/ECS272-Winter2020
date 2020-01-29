//load the dataset from a CSV file
var map_visualization = null
var data = null

d3.csv('../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv')
    .then(csv => {
        data = csv

        var fdata = filterCSV(12)

        map_visualization = new MapVisualization(fdata);
        filterCSV()

    })

function onMapSelectionChanged(value) {
    d3.select("#time").text(value + ":00")
    var fdata = filterCSV(value)
    map_visualization.update(fdata)
}

function filterCSV(time) {
    return data.filter(d => {
        return d["Time"].startsWith(time)
    })
}
