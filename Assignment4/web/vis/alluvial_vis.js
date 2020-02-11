class AlluvialVis {
    constructor(data, html_root, dimensions) {
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

        this.init()
    }

    transformData() {

    }

    init() {

    }
}