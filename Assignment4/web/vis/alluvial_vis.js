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
        this.columns = ['sex', 'age', 'guardian', 'failures']

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

    init() {
        // clear the tag
        d3.select(this.html_root + " > *").remove()

        // create svg
        var svg = d3.select(this.html_root)
            .append('svg')
            .attr('width', this.width + this.margin.left + this.margin.right)
            .attr('height',  this.height + this.margin.top + this.margin.bottom)
            .attr('margin-top', '250px')

        var g = svg.append('g')
            .attr('transform', 'translate(' + this.margin.left + ',' + this.margin.top + ')')

        // create sankey skeleton
        var sankey = d3.sankey()
            .nodeWidth(15)
            .nodePadding(10)
            .extent([[1, 1], [this.width, this.height]])
        
        // create sankey layout
        sankey(this.graph)

        // create rectangles for the nodes
        svg.selectAll('.node')
            .data(this.graph.nodes)
            .enter().append('rect')
            .attr('class', 'node')
            .attr("fill", 'gray')
            .attr("x", d => d.x0)
            .attr("y", d => d.y0)
            .attr("width", d => { return d.x1 - d.x0})
            .attr("height", d => { return d.y1 - d.y0 })

        for(var i = 0; i < this.columns.length; i++)
        {
            var x_offset = i * (this.width / (this.columns.length - 1))

            svg.append('text')
            .text(this.columns[i])
            .attr('transform', 'translate(' + x_offset + ',' + 20 + ')')
            .attr('text-anchor', 'middle')
        }

        // create a curved area for links
        svg.selectAll('.link')
            .data(this.graph.links)
            .enter().append('path')
            .attr('class', 'link')
            .attr('d', d3.sankeyLinkHorizontal())
            .attr("stroke-width", function(d) { return Math.max(1, d.width); })
            .attr('stroke', "#010000")
        // // create a curved area for links
        // var link = g.append('g')
        //     .data(this.graph.links)
        //     .enter().append('path')
        //     .attr('class', 'link')
        //     .attr('d', d3.sankeyLinkHorizontal())
        //     .attr("stroke-width", function(d) { return Math.max(1, d.width); })
        //     .attr('stroke', "#010000")


        // // add the link titles
        // link.append("title")
        //     .text(function (d) {
        //         return d.source.name + " → " +
        //             d.target.name + "\n" + format(d.value);
        //     });

        // add in the nodes
        // var node = svg.append("g").selectAll(".node")
        //     .data(this.graph.nodes)
        //     .enter().append("g")
        //     .attr("class", "node")
        //     .attr("transform", function (d) {
        //         return "translate(" + d.x + "," + d.y + ")";
        //    })
            // .call(d3.behavior.drag()
            //     .origin(function (d) { return d; })
            //     .on("dragstart", function () {
            //         this.parentNode.appendChild(this);
            //     })
            //     .on("drag", dragmove));

        // add the rectangles for the nodes
        // node.append("rect")
        //     .attr("height", function (d) { return d.dy; })
        //     .attr("width", sankey.nodeWidth())
        //     .style("fill", function (d) {
        //         return d3.rgb(d.color)
        //         //return d.color = color(d.name.replace(/ .*/, ""));
        //     })
        //     .style("stroke", function (d) {
        //         return d3.rgb(d.color).darker(2);
        //     })
        //     .append("title")
            // .text(function (d) {
            //     return d.name + "\n" + format(d.value);
            // });

    }
}