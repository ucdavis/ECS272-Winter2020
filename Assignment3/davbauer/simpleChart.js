class SimpleChart {
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

    transformData(data) { 
        var nested = d3.nest()
            .key(d => d.Terminal)
            .rollup(v => {
                return d3.sum(v, d => d.Passenger_Count)
            })
            .entries(data)
        
        return nested.map(d => {
            return {
                key: d.key,
                value: +d.value,
            }
        }).sort((a, b) => d3.ascending(a.key, b.key));
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
        this.x = d3.scaleBand()
            .domain(this.data.map(d =>  d.key))
            .range([0, this.width])
            .padding(0.1)
            
        this.y = d3.scaleLinear()
            .domain([0, d3.max(this.data, d => d.value)])
            .range([this.height, 0])

        //axis
        this.xAxis = d3.axisBottom(this.x)
        this.yAxis = d3.axisLeft(this.y).ticks(6)
            
        // create a bar plot
        view.selectAll(".bar")
            .data(this.data)
            .enter()
            .append("rect")
            .attr("class", "bar")
            .attr("fill", "lightblue")
            .attr("x", d => { return this.x(d.key) })
            .attr("y", d => { return this.y(d.value) })
            .attr("width", this.x.bandwidth())
            .attr("height", d => { return this.height - this.y(d.value) })
    
    
        // x axis
        view.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + this.height + ")")
            .call(this.xAxis)
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(90)")
            .style("text-anchor", "start")
    
        // y axis
        view.append("g")
            .attr("class", "y axis")
            .call(this.yAxis)
            .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("x", - this.height / 5)
            .attr("y", - this.margin.left)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("No. Passengers")
    
    }

    updateChart(data) {
        console.log("Secondary Chart Entries: " + data.length)

        // Re-calculate data
        this.data = this.transformData(data)
        //this.init()
        

        // Update axis
        this.x.domain(this.data.map(d => d.key))
        this.y.domain([0, d3.max(this.data, d => d.value)])

        d3.select(this.html_root).select(".x.axis")
            .transition()
            .duration(500)
            .call(this.xAxis)
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(90)")
            .style("text-anchor", "start")
        d3.select(this.html_root).select(".y.axis")        
            .transition()
            .duration(500)
            .call(this.yAxis)


        // Update plot
        var bars = d3.select(this.html_root).select("g").selectAll(".bar")
        .data(this.data)


        bars
            .exit()
            .transition()
            .duration(500)
            .attr("y", this.y(0))
            .attr("height", this.height - this.y(0))
            .style('fill-opacity', 1e-6)
            .remove()
        bars
            .enter()
            .append("rect")
            .attr("class", "bar")
            .attr("fill", "lightblue")
            .attr("x", d => { return this.x(d.key) })
            .attr("width", this.x.bandwidth())
            .attr("y", this.y(0))
            .attr("height", this.height - this.y(0))


        bars = d3.select(this.html_root).select("g").selectAll(".bar")
            .data(this.data)
        
        bars
            .transition()
            .duration(500)
            .attr("x", d => { return this.x(d.key) })
            .attr("y", d => { return this.y(d.value) })
            .attr("width", this.x.bandwidth())
            .attr("height", d => { return this.height - this.y(d.value)}) 

    }
}