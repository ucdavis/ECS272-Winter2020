class AlluvialVis {
    constructor(data, html_root, dimensions) {
        this.graph = this.transformData(data)
        this.html_root = html_root

        this.width = dimensions.width
        this.height = dimensions.height
        this.margin = dimensions.margin

        this.x = null
        this.y = null
        this.xAxis = null
        this.yAxis = null
        this.plot_function = null

        this.init()
    }

    transformData(data) {
        var graph = {'nodes': [], 'links': []}

        var n_rows = data.length
        var columns = ['sex', 'age', 'guardian', 'failures']

        var nodes = []
        var links = []

        var col_nodes = {}

        for (const element of columns) {
            col_nodes[element] = d3.set(data, d => d[element]).values()
            nodes.push.apply(nodes, d3.set(data, d => d[element]).values())
        }
        graph.nodes = nodes


        for (var i = 0; i < columns.length - 1; i++) {

            var items = []
            for (const val1 of col_nodes[columns[i]]) {
                items = data.filter(d => {
                    return d[columns[i]] == val1
                })

                for (const val2 of col_nodes[columns[i+1]]) {
                    var val = items.filter(d => {
                        return d[columns[i+1]] == val2
                    }).length

                    links.push({
                        source: val1,
                        target: val2,
                        value: val / n_rows
                    })
                }
            }
        }
        graph.links = links

        return graph
    }

    init() {
        // Clear the tag
        d3.select(this.html_root + " > *").remove()

        var svg = d3.select(this.html_root)
        .append('svg')
            .attr('width', this.width + this.margin.left + this.margin.right)
            .attr('height', this.height + this.margin.top + this.margin.bottom)

        var view = svg.append('g')
            .attr('transform', 'translate(' + this.margin.left + ',' + this.margin.top + ')')

        var sankey = d3.sankey()
            .nodeWidth(36)
            .nodePadding(10)
            .size([this.width, this.height])

        var path = sankey.link()

        //sankey
        //    .nodes(this.graph.nodes)
        //    .links(this.graph.links)
        //    .layout(32)

        
    }
}