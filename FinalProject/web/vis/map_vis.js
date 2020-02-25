class MapVis {
    constructor(data, html_root, dimensions) {
        this.data = data
        this.html_root = html_root

        this.width = dimensions.width
        this.height = dimensions.height
        this.margin = dimensions.margin

        this.init()
    }

    init() {
        // var svg = d3.select(this.html_root)
        //     .append('svg')
        //     .attr('width', this.width + this.margin.left + this.margin.right)
        //     .attr('height', this.height + this.margin.top + this.margin.bottom)


        // var view = svg.append('g')
        //      .attr('transform', 'translate(' + this.margin.left + ',' + this.margin.top + ')')

        var map = L.map(this.html_root).setView([41.9028, 12.4964], 2)

        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: 'pk.eyJ1IjoibHVrYXNtYXhpbSIsImEiOiJjazcyYXVuZjQwMGNkM21wb2tobDl5cXVuIn0._VW3qQdxkxWyN2vj6vXOvA'
        }).addTo(map);
    }
}