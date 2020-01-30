class ComplexChart {
    constructor(data, html_root, dimensions) {
        this.keys = null
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
        this.colors = null

        this.init()
    }

    transformData(data) {
        this.keys = d3.set(data, d => {
            return d.Terminal
        }).values()

        var nested = d3.nest()
        .key(d => { return new Date(d.ReportPeriod) })
        .rollup(v => { 
            var result = {}
            this.keys.forEach(key => {
                result[key] = d3.sum(v, d => { 
                    return d.Terminal == key ? parseInt(d.Passenger_Count) : 0 
                })
            })
            return result
        })
        .entries(data)

        return nested.map(d => {
            d.value.date = new Date(d.key)
            return d.value
        })
    }

    init() {
        // Clear the tag
        d3.select(this.html_root + " > *").remove()

        // Add new items
        var svg = d3.select(this.html_root)
        .append('svg')
            .attr('width', this.width + this.margin.left + this.margin.right)
            .attr('height', this.height + this.margin.top + this.margin.bottom) 

        var view = svg.append("g")
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")
    
    
        //scale functions
        this.x = d3.scaleTime()
            .domain([d3.min(this.data, d => d.date), d3.max(this.data, d => d.date)])
            .range([0, this.width])
            
        this.y = d3.scaleLinear()
            .range([this.height, 0])

        // axis
        this.xAxis = d3.axisBottom(this.x).ticks(6)
        this.yAxis = d3.axisLeft(this.y).ticks(6)

        // plot function and colors
        this.plot_function = d3.area()
            .x(d => { return this.x(d.data.date) })
            .y0(d => { return this.y(d[0]) })
            .y1(d => { return this.y(d[1]) })

        this.colors = d3.scaleOrdinal()
        .domain(this.keys)
        .range(d3.schemeSet2)

        // stream graph
        var stack = d3.stack()
            .offset(d3.stackOffsetSilhouette)
            .keys(this.keys)
            (this.data)

        var ymin = d3.min(stack.map(d => {
            return d3.min(d.map(v => {
                return d3.min(v)
            }))
        }))
        var ymax = d3.max(stack.map(d => {
            return d3.max(d.map(v => {
                return d3.max(v)
            }))
        }))
        this.y.domain([ymin*1.1, ymax*1.1])

        // create the streamgraph
        var self = this;
        view.selectAll(".layer")
            .data(stack)
            .enter()
            .append("path")
            .attr("class", "plot")
            .style("fill", d => { return this.colors(d.key); })
            .attr("d", this.plot_function)
            .on("mouseover", function(d) { self.onMouseOver(self, this, d) })
            .on("mousemove", (d, i) => this.onMouseMove(d, i))
            .on("mouseleave", (d) => this.onMouseLeave(d))
    
        // x axis
        view.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + this.height + ")")
            .call(this.xAxis)
            .append("text")
            .attr("fill", "#000")
            .attr("x", this.width / 2)
            .attr('y', this.margin.bottom / 2)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("Time")
    
        // y axis
        view.append("g")
            .attr("class", "y axis")
            .call(this.yAxis)
            .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("x", - this.height / 2.5 )
            .attr("y", - this.margin.left)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("Passengers per Terminal")

        // terminal hover text
        view.append("text")
            .attr("class", "tooltip")
            .attr("x", 20)
            .attr("y", 20)
            .style("opacity", 0)
            .style("font-size", 17)
    }

    onMouseOver(self, el, d) {
        d3.select(self.html_root).selectAll(".tooltip")
            .style("opacity", 1)
        d3.select(self.html_root).selectAll(".plot")
            .style("opacity", 0.5)
        d3.select(el)
            .style("stroke", "black")
            .style("opacity", 1)
    }

    onMouseMove(d, i) {
        d3.selectAll(this.html_root).selectAll(".tooltip").text(this.keys[i])
    }

    onMouseLeave(d) {
        d3.selectAll(this.html_root).selectAll(".tooltip")
            .style("opacity", 0)
        d3.selectAll(this.html_root).selectAll(".plot")
            .style("opacity", 1)
            .style("stroke", "none")
    }

    updateChart(data) {
        console.log("Primary Chart Entries: " + data.length)

        // Re-calculate data
        this.data = this.transformData(data)
        var stack = d3.stack()
            .offset(d3.stackOffsetSilhouette)
            .keys(this.keys)
            (this.data)


        // Update axis
        this.x.domain([d3.min(this.data, d => d.date), d3.max(this.data, d => d.date)])
        var ymin = d3.min(stack.map(d => {
            return d3.min(d.map(v => {
                return d3.min(v)
            }))
        }))
        var ymax = d3.max(stack.map(d => {
            return d3.max(d.map(v => {
                return d3.max(v)
            }))
        }))
        this.y.domain([ymin*1.1, ymax*1.1])


        // Update chart
        var layers = d3.select(this.html_root).selectAll("path")
        .data(stack)


        layers
            .exit()
            .transition()
            .duration(500)
            .remove();

        layers
            .enter()
            .append("path")
            .attr("class", "plot")
            .style("fill", d => { return this.colors(d.key); })
            .attr("d", this.plot_function)
            .on("mouseover", function(d) { self.onMouseOver(self, this, d) })
            .on("mousemove", (d, i) => this.onMouseMove(d, i))
            .on("mouseleave", (d) => this.onMouseLeave(d))

        layers
            .transition()
            .duration(500)
            .style("fill", d => { return this.colors(d.key); })
            .attr("d", this.plot_function)


        // Call axis
        d3.select(this.html_root).select(".x.axis")
            .transition()
            .duration(500)
            .call(this.xAxis)
        d3.select(this.html_root).select(".y.axis")        
            .transition()
            .duration(500)
            .call(this.yAxis)

        
    }
}