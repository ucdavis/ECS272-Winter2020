var map_visualization = null
var data = null
var no_crimes = 5
var time_value = 17

d3.csv('../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv')
    .then(csv => {
        data = csv

        var fdata = filterCSV(this.time_value)

        map_visualization = new MapVisualization(fdata);
        pie_visualization = new PieVisualization(fdata, no_crimes);
    })

function onMapSelectionChanged(value) {
    this.time_value = value
    d3.select("#time").text("Crimes commited at " + value + ":00")

    var padded_value = pad(this.time_value, 2)
    var fdata = filterCSV(padded_value)

    map_visualization.update(fdata)
    pie_visualization.update(fdata, this.no_crimes)
}

function onSelectChanged(value) {
    this.no_crimes = value
    var padded_value = pad(this.time_value, 2)
    var fdata = filterCSV(padded_value)

    pie_visualization.update(fdata, this.no_crimes)
}

function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}

function filterCSV(time) {
    return data.filter(d => {
        return d["Time"].startsWith(time)
    })
}
