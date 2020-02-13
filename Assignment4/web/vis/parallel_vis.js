class ParallelVis {
    constructor(data, html_root, dimensions) {
        this.columns = ['sex', 'age', 'health', 'Walc', 'Dalc', 'studytime', 'failures']

        this.data = this.transformData(data)
        this.html_root = html_root

        this.width = dimensions.width
        this.height = dimensions.height
        this.margin = dimensions.margin

        this.x = null
        this.y = null
        this.xAxis = null
        this.yAxis = null
        this.plot_function = null

        //this.init()
        this.plot()
    }

    transformData(data) {
        return data

        var graph = { 'nodes': [], 'links': [] }

        var n_rows = data.length
        //this.columns = ['sex', 'age', 'health', 'Walc', 'Dalc', 'studytime', 'failures']
        //this.columns = ['sex', 'failures', 'health']

        var nodes = []
        var links = []

        var col_nodes = {}

        var node_count = 0

        for (const element of this.columns) {
            col_nodes[element] = []
            var unique_values = d3.set(data, d => d[element]).values()

            for(const val of unique_values) {
                nodes.push({
                    node: node_count,
                    name: val
                })
                col_nodes[element].push({
                    node: node_count++,
                    name: val
                })
            }
        }
        graph.nodes = nodes


        for (var i = 0; i < this.columns.length - 1; i++) {

            var items = []
            for (const val1 of col_nodes[this.columns[i]]) {
                items = data.filter(d => {
                    return d[this.columns[i]] == val1.name
                })

                for (const val2 of col_nodes[this.columns[i+1]]) {
                    var val = items.filter(d => {
                        return d[this.columns[i+1]] == val2.name
                    }).length

                    links.push({
                        source: val1.node,
                        target: val2.node,
                        value: val / n_rows
                    })
                }
            }
        }
        graph.links = links

        return graph
    }

    plot() {
        this.dimensions = d3.keys(this.data[0]).filter(d => { return d == 'age' || d == 'Dalc' })
        this.dimensions = this.columns

        this.y = {}

        for(var name of this.dimensions) {
            this.y[name] = d3.scaleBand()
                .domain(this.data.map(d => d[name]))
                .range([this.height, 0])
        }

        this.x = d3.scalePoint()
            .range([0, this.width])
            .domain(this.dimensions)

        var svg = d3.select("#parallel-vis-container")
            .append("svg")
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom)

        var view = svg.append("g")
              .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

        view.selectAll('.myPath')
            .data(this.data)
            .enter().append('path')
            .attr('class', 'myPath')
            .attr('d', (d) => { return this.path(d) })
            .style("fill", "none")
            .style("stroke", "#69b3a2")
            .style("opacity", 0.1)


        var self = this

        view.selectAll(".myAxis")
            // For each dimension of the dataset I add a 'g' element:
            .data(this.dimensions).enter()
            .append("g")
            .attr('class', 'myAxis')
            .attr("transform", (d) => { return "translate(" + this.x(d) + ", 0)"; })
            .each(function(d) { d3.select(this).call(d3.axisLeft().scale(self.y[d])) })
            // And I build the axis with the call function
            //.each(function(d) { d3.select(this).call(d3.axisLeft().scale(y[d])); })
            // Add axis title
            .append("text")
            .style("text-anchor", "middle")
            .attr("y", -9)
            .text(function(d) { return d; })
            .style("fill", "black")
    

    }

    path(d) {
        return d3.line()(this.dimensions.map((p) => { 
            return [this.x(p), this.y[p](d[p])]; 
        }));
    }

    init() {
        // clear the tag
        d3.select(this.html_root + " > *").remove()

        var colors = {
            'M' : '#0087DC',
            'F' : '#FFC0CB',
            '0' : '#46CB18',
            'Yes': '#BA0000'
        }

        // create svg
        var svg = d3.select(this.html_root)
            .append('svg')
            .attr('width', this.width + this.margin.left + this.margin.right)
            .attr('height',  this.height + this.margin.top + this.margin.bottom)

        var view = svg.append('g')
            .attr('transform', 'translate(' + this.margin.left + ',' + this.margin.top + ')')



        // create category labels


        for(var i = 0; i < this.columns.length; i++)
        {
            var x_offset = i * (this.width / (this.columns.length - 1)) + this.margin.left
            var y_offset = this.margin.top - 15

            svg.append('text')
            .text(this.toUpperCase(this.columns[i]))
            .attr('transform', 'translate(' + x_offset + ',' + y_offset + ')')
            .attr('text-anchor', 'middle')

        }
    }

    handleMouseOver(d, i){
        d3.select(this)
            .attr('fill', '#000')
    }

    toUpperCase(string) {
        return string.charAt(0).toUpperCase() + string.slice(1)
    }
}