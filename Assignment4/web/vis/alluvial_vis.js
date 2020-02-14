class AlluvialVis {
    constructor(data, html_root, dimensions) {
        this.columns = ['sex', 'age', 'romantic', 'Walc', 'Dalc', 'health', 'failures']

        this.data = data
        this.graph = null
        this.html_root = html_root

        this.width = dimensions.width
        this.height = dimensions.height
        this.margin = dimensions.margin

        this.x = null
        this.y = null
        this.xAxis = null
        this.yAxis = null
        this.plot_function = null

        this.index_cat_ref = []

        this.init()
    }

    transformData(data) {
        var graph = { 'nodes': [], 'links': [] }

        var n_rows = data.length
        //this.columns = ['Walc', 'sex', 'health']
        //this.columns = ['sex', 'failures', 'health']

        var nodes = []
        var links = []

        var col_nodes = {}

        var node_count = 0

        for (const element of this.columns) {
            col_nodes[element] = []
            var unique_values = d3.set(data, d => d[element]).values().sort((a, b) => {
                return parseInt(a) > parseInt(b)
            })

            for (const val of unique_values) {
                nodes.push({
                    node: node_count,
                    name: val
                })
                this.index_cat_ref[node_count] = element
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

                for (const val2 of col_nodes[this.columns[i + 1]]) {
                    var val = items.filter(d => {
                        return d[this.columns[i + 1]] == val2.name
                    }).length

                    links.push({
                        source: val1.node,
                        target: val2.node,
                        value: val / n_rows,
                    })
                }
            }
        }
        graph.links = links

        return graph
    }

    init() {
        var self = this
        this.graph = this.transformData(this.data)

        // clear the tag
        d3.select(this.html_root + " > *").remove()

        var colors = {
            'sex_M': '#0087DC',
            'sex_F': '#FFC0CB',
            '0': '#46CB18',
            'romantic_yes': '#BA0000',
            'romantic_no': '#C2C5CC',
            'Walc_1': '#dbf22c',
            'Walc_2': '#a1dab4',
            'Walc_3': '#41b6c4',
            'Walc_4': '#2c7fb8',
            'Walc_5': '#253494',
            'Dalc_1': '#dbf22c',
            'Dalc_2': '#a1dab4',
            'Dalc_3': '#41b6c4',
            'Dalc_4': '#2c7fb8',
            'Dalc_5': '#253494',
            'health_1': '#54c9e5',
            'health_2': '#95d3cf',
            'health_3': '#d9cfc0',
            'health_4': '#f27119',
            'health_5': '#fb5108',
            'failures_1': '#54c9e5',
            'failures_2': '#95d3cf',
            'failures_3': '#d9cfc0',
            'failures_4': '#f27119',
        }

        // create svg
        var svg = d3.select(this.html_root)
            .append('svg')
            .attr('width', this.width + this.margin.left + this.margin.right)
            .attr('height', this.height + this.margin.top + this.margin.bottom)

        var view = svg.append('g')
            .attr('transform', 'translate(' + this.margin.left + ',' + this.margin.top + ')')

        // create sankey skeleton
        var sankey = d3.sankey()
            .nodeWidth(15)
            .nodePadding(10)
            .iterations(0) // makes stuff order!
            .extent([[1, 1], [this.width, this.height]])

        // create sankey layout
        sankey(this.graph)




        // create category labels
        for (var i = 0; i < this.columns.length; i++) {
            var x_offset = i * (this.width / (this.columns.length - 1)) + this.margin.left
            var y_offset = this.margin.top - 15

            svg.append('text')
                .text(this.toUpperCase(this.columns[i]))
                .attr('transform', 'translate(' + x_offset + ',' + y_offset + ')')
                .attr('text-anchor', 'middle')
        }

        // create a curved area for links
        view.selectAll('.link')
            .data(this.graph.links)
            .enter().append('path')
            .attr('class', d => { return 'link source-' + d.source.layer + '-' + d.source.name + ' target-' + d.source.layer + '-' + d.target.name })
            .attr('d', d3.sankeyLinkHorizontal())
            .attr("stroke-width", d => { return Math.max(1, d.width); })
            .attr('stroke', d => {
                return colors[this.index_cat_ref[d.source.node] + '_' + d.source.name] || '#000'
            })

                   // create rectangles for the nodes
        view.selectAll('.node')
        .data(this.graph.nodes)
        .enter().append('rect')
        .attr('class', 'node')
        .attr("fill", 'gray')
        .attr("x", d => d.x0)
        .attr("y", d => d.y0)
        .attr("width", d => { return d.x1 - d.x0 })
        .attr("height", d => { return d.y1 - d.y0 })
        .on('mouseover', this.handleMouseOver)
        .on('mouseout', this.handleMouseOut)
        .on('click', function(d) {
            self.handleMouseClick.call(this, d, self)
        })

        // create labels next to teh nodes
        view.selectAll('.node-label')
            .data(this.graph.nodes)
            .enter().append('text')
            .attr('class', 'node-label')
            .attr('text-anchor', 'end')
            .attr("x", d => d.x0 - 15)
            .attr("y", d => d.y0 + (d.y1 - d.y0) / 2)
            .text(d => this.toUpperCase(d.name))
    }

    handleMouseOver(d) {
        d3.selectAll('.source-' + d.layer + '-' + d.name)
            .classed('hovered', true)

        d3.selectAll('.target-' + (d.layer - 1) + '-' + d.name)
            .classed('hovered', true)
    }

    handleMouseOut(d) {
        d3.selectAll('.source-' + d.layer + '-' + d.name)
            .classed('hovered', false)

        d3.selectAll('.target-' + (d.layer - 1) + '-' + d.name)
            .classed('hovered', false)
    }

    handleMouseClick(d, self) {
        var state = !d3.select(this).classed("selected")
        d3.selectAll('.node')
            .classed("selected", false)
        d3.selectAll('.link')
            .classed('selected', false)

        d3.select(this)
            .classed("selected", state)

        d3.selectAll('.source-' + d.layer + '-' + d.name)
            .classed('selected', state)

        d3.selectAll('.target-' + (d.layer - 1) + '-' + d.name)
            .classed('selected', state)

        self.sendFilteredData(d, state)
    }

    sendFilteredData(d, selected){
        var filtered_data
        var column


        if (selected) {
            column = this.index_cat_ref[d.node]
            filtered_data = this.data.filter(j => {
                return j[column] == d.name
            })
        } else {
            column = null
            filtered_data = this.data
        }

        eventbus.emit('alluvial_vis_changed', filtered_data, column)
    }

    toUpperCase(string) {
        return string.charAt(0).toUpperCase() + string.slice(1)
    }
}
