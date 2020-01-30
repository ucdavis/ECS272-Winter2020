class PieVisualization {

    constructor(data, no_crimes) {
        this.init(data, no_crimes)
    }

    // called upon initialize
    init(data, no_crimes) {
        var tdata = this.transform_data(data, no_crimes)
        this.draw(tdata)
    }

    // called upon slider change
    update(data, no_crimes) {
        var tdata = this.transform_data(data, no_crimes)
        d3.selectAll('#chart > *').remove()
        this.draw(tdata)
    }

    transform_data(csv, no_crimes) {

        var grouped_data = d3.nest()
            .key(d => { return d["Category"] })
            .rollup(v => {
                return {
                    count: v.length,
                }
            })
            .entries(csv)

        return grouped_data.map(d => {
            return {
                key: d.key,
                value: d.value.count
            }
        }).sort((a, b) => { return a.value > b.value}).slice(0,no_crimes)
    }

    draw(data) {
        const size = 500;
        const fourth = size / 4;
        const labelOffset = fourth * 1.4;
        const total = data.reduce((acc, cur) => acc + cur.value, 0);
        var width = 600;
        var height = 400;
        var margin = {left: 360, right: 20, top: 200, bottom: 60}


        const color = d3.scaleOrdinal()
            .domain(data.map(d => d.name))
            .range(d3.schemeCategory10)

        const chart = d3.select('#chart')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)

        const plotArea = chart.append('g')
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        const pie = d3.pie()
            .value(d => d.value)
            .sort(null);

        var arcs = pie(data)

        const arc = d3.arc()
            .innerRadius(0)
            .outerRadius(fourth);

        const arcLabel = d3.arc()
            .innerRadius(labelOffset)
            .outerRadius(labelOffset);

        plotArea.selectAll('path')
            .data(arcs)
            .enter()
            .append('path')
            .attr('fill', d => color(d.data.value))
            .attr('stroke', 'white')
            .attr('d', arc);

        const labels = plotArea.selectAll('text')
            .data(arcs)
            .enter()
            .append('text')
            .style('text-anchor', 'middle')
            .style('alignment-baseline', 'middle')
            .style('font-size', '10px')
            .style('font-family', 'Arial, Helvetica, sans-serif')
            .attr('transform', d => `translate(${arcLabel.centroid(d)})`)

        labels.append('tspan')
            .attr('y', '-0.6em')
            .attr('x', 0)
            .style('font-weight', 'bold')
            .style('font-family', 'Arial, Helvetica, sans-serif')
            .text(d => `${d.data.key}`);

        labels.append('tspan')
            .attr('y', '0.6em')
            .attr('x', 0)
            .text(d => `${d.data.value} (${Math.round(d.data.value / total * 100)}%)`);

    }

}