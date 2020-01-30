class MapVisualization {

    constructor(csv) {
        this.sampling = 10000

        this.init(csv)
    }

    // called upon initialize
    init(csv){
        var array = this.transform_data(csv)
        this.draw(array)
    }

    // called upon slider change
    update(csv){
        var array = this.transform_data(csv)
        this.mymap.removeLayer(this.heatlayer)
        this.heatlayer = L.heatLayer(array, { radius: 20, max: 10 })
        this.heatlayer.addTo(this.mymap)
    }

    // transforms csv into array accessible by heatmap 
    transform_data(csv) {
        var data = csv.map(row => {
            return {
                latitude: Number(row['X']),
                longitude: Number(row['Y']),
            }
        })

        // sample by rounding coords
        data.forEach(element => {
            element.latitude = Math.round(element.latitude * this.sampling) / this.sampling
            element.longitude = Math.round(element.longitude * this.sampling) / this.sampling
        });

        // group coords
        var grouped_data = d3.nest()
            .key(d => { return d.longitude + '#' + d.latitude })
            .rollup(v => { return { 
                count: v.length,
             } })
            .entries(data)

        // turn into array
        var grouped_data_array = []
        grouped_data.forEach(element => {
            grouped_data_array.push(
                [parseFloat(element["key"].split("#", 1)[0]), parseFloat(element["key"].split("#", 2)[1]), element["value"]["count"]]
            )
        });

        return grouped_data_array
    }

    // draws the map with overlayed heatmap
    draw(array) {
        // draw map
        this.mymap = L.map('mapid').setView([37.775, -122.403], 11);

        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox/streets-v11'
        }).addTo(this.mymap);

        // add heatmap layer
        this.heatlayer = L.heatLayer(array, { radius: 20, max: 10})
        this.heatlayer.addTo(this.mymap);
    }
}
