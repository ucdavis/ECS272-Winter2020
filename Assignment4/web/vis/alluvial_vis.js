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
        var graph = { 'nodes': [], 'links': [] }

        var n_rows = data.length
        var columns = ['sex', 'age', 'guardian', 'failures']

        var nodes = []
        var links = []

        var col_nodes = {}

        // for (const element of columns) {
        //     col_nodes[element] = d3.set(data, d => d[element]).values()
        //     var unique_values = d3.set(data, d => d[element]).values()

        //     nodes.push({
        //         node: unique_values
        //     })
        // }
        // graph.nodes = nodes


        // for (var i = 0; i < columns.length - 1; i++) {

        //     var items = []
        //     for (const val1 of col_nodes[columns[i]]) {
        //         items = data.filter(d => {
        //             return d[columns[i]] == val1
        //         })

        //         for (const val2 of col_nodes[columns[i+1]]) {
        //             var val = items.filter(d => {
        //                 return d[columns[i+1]] == val2
        //             }).length

        //             links.push({
        //                 source: val1,
        //                 target: val2,
        //                 value: val / n_rows
        //             })
        //         }
        //     }
        // }
        // graph.links = links

        data = {
            "nodes": [
                {
                    "node": 0,
                    "name": "Africa"
                },
                {
                    "node": 1,
                    "name": "America"
                },
                {
                    "node": 2,
                    "name": "Europe"
                }
            ],
            "links": [
                {
                    "source": 0,
                    "target": 2,
                    "value": 1
                },
                {
                    "source": 1,
                    "target": 2,
                    "value": 2
                },
                {
                    "source": 0,
                    "target": 1,
                    "value": 1
                }
            ]
        }

        graph.links = data.links
        graph.nodes = data.nodes

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

        sankey
            .nodes(this.graph.nodes)
            .links(this.graph.links)
            .layout(32)

        // add in the links
        var link = svg.append("g").selectAll(".link")
            .data(this.graph.links)
            .enter().append("path")
            .attr("class", "link")
            .attr("d", path)
            .style("stroke-width", function (d) { return Math.max(1, d.dy); })
            .sort(function (a, b) { return b.dy - a.dy; });

        // // add the link titles
        // link.append("title")
        //     .text(function (d) {
        //         return d.source.name + " → " +
        //             d.target.name + "\n" + format(d.value);
        //     });

        // add in the nodes
        var node = svg.append("g").selectAll(".node")
            .data(this.graph.nodes)
            .enter().append("g")
            .attr("class", "node")
            .attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            })
            // .call(d3.behavior.drag()
            //     .origin(function (d) { return d; })
            //     .on("dragstart", function () {
            //         this.parentNode.appendChild(this);
            //     })
            //     .on("drag", dragmove));

        // add the rectangles for the nodes
        node.append("rect")
            .attr("height", function (d) { return d.dy; })
            .attr("width", sankey.nodeWidth())
            .style("fill", function (d) {
                return d.color = color(d.name.replace(/ .*/, ""));
            })
            .style("stroke", function (d) {
                return d3.rgb(d.color).darker(2);
            })
            .append("title")
            .text(function (d) {
                return d.name + "\n" + format(d.value);
            });

    }
}