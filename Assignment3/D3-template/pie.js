class PieVisualization {

    constructor(csv) {
        this.init(csv)
    }

    // called upon initialize
    init(csv) {
        var tcsv = this.transform_data(csv)
        this.draw(tcsv)
    }

    transform_data(csv) {

        var grouped_data = d3.nest()
            .key(d => { return d["Category"] })
            .rollup(v => {
                return {
                    count: v.length,
                }
            })
            .entries(csv)

        return grouped_data
    }

    draw(tcsv) {
        const width = 600;
        const height = 400;
        const radius = Math.min(width, height) / 2;
        const margin = { left: 60, right: 20, top: 20, bottom: 60 }

        const color = d3.scaleOrdinal(d3.schemeCategory10);

        const svg = d3.select('#container')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${width / 2}, ${height / 2})`);

        const pie = d3.pie()
            .value(d => d.count)
            .sort(null);

        const arc = d3.arc()
            .innerRadius(0)
            .outerRadius(radius);
 

        var arcs = svg.selectAll("g.slice")
            .data(pie)
            .enter()
            .append("svg:g")
            .attr("class", "slice")

        arcs.append("svg:path")
            .attr("fill", (d, i) => { return color(i); })
            .attr("d", arc)

    }

}