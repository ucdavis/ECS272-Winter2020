class MapVisualization {

    constructor(data) {
        this.data = data
    }

    draw() {
        // draw basic map
        var mymap = L.map('mapid').setView([37.775, -122.403], 10);    

        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox/streets-v11'
        }).addTo(mymap);

        this.data.forEach(element => {
            L.marker([element.latitude, element.longitude], 500).addTo(mymap);
        });
    }



    // L.marker([51.5, -0.09]).addTo(mymap)
    //   .bindPopup("<b>Hello world!</b><br />I am a popup.").openPopup();

    // L.circle([37.775420706711, -122.403404791479], 500, {
    //     color: 'red',
    //     fillColor: '#f03',
    //     fillOpacity: 0.5
    // }).addTo(mymap).bindPopup("I am a circle.");

    // L.polygon([
    //     [51.509, -0.08],
    //     [51.503, -0.06],
    //     [51.51, -0.047]
    // ]).addTo(mymap).bindPopup("I am a polygon.");


    // var popup = L.popup();

    // function onMapClick(e) {
    //     popup
    // .setLatLng(e.latlng)
    // .setContent("You clicked the map at " + e.latlng.toString())
    // .openOn(mymap);
}

// mymap.on('click', onMapClick);

// }

