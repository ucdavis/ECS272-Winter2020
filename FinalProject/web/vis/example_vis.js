class ExampleVis {
    constructor(data, html_root, dimensions) {
        this.data = data
        this.html_root = html_root

        this.width = dimensions.width
        this.height = dimensions.height
        this.margin = dimensions.margin

        this.init()
    }

    init() {
        var svg = d3.select(this.html_root)
            .append('svg')
            .attr('width', this.width + this.margin.left + this.margin.right)
            .attr('height', this.height + this.margin.top + this.margin.bottom)


        var view = svg.append('g')
             .attr('transform', 'translate(' + this.margin.left + ',' + this.margin.top + ')')

        view.append('text')
            .text('Here could be your vis.')
            .style('fill', colors.example_text_color)
    }
}
