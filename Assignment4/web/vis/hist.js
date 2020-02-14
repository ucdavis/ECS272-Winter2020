class Histogram {
    constructor(data, html_root, dimensions, setting){

        eventbus.on('scatter_vis_changed', (filtered_data, ...args) => {
          this.updateLinking(args[0], filtered_data)
      })

        this.setting = setting
        this.isHist = true
        //raw data
        this.data = data
        this.h_data = null

        this.html_root = html_root

        this.width = dimensions.width
        this.height = dimensions.height
        this.margin = dimensions.margin

        this.x = null
        this.y = null
        this.xAxis = null
        this.yAxis = null
        this.plot_function = null

        this.mouseover = null
        this.mousemove = null
        this.mouseleave = null
        //somehow just cannot make tooltip here.

        this.init()
    }

    transformData(data, key, isHist) {
      if(data == null){
        return
      }

      if(isHist){
        var hist = d3.histogram()
          .domain([this.setting.x_domain.min, this.setting.x_domain.max])
          .thresholds([...Array(this.setting.x_ticks+1).keys()]);

        var temp = hist(data.map(d => d[key]).map(d => { return +d }) ).map(d => {
          return{
            x0: d.x0,
            x1: d.x1,
            value: d.length
          }
        })

        return temp
      } else {
        var nested = d3.nest()
        .key(d => d[key])
        .rollup(v => v.length)
        .entries(data)

        return nested.map(d => {
            return {
                key: d.key,
                value: +d.value,
            }
        }).sort((a, b) => d3.ascending(a.key, b.key))
      }
    }

    init(){
        // Clear the tag
        d3.select(this.html_root + " > *").remove()

        // Add new items
        var svg = d3.select(this.html_root)
        .append('svg')
            .attr('width', this.width + this.margin.left + this.margin.right)
            .attr('height', this.height + this.margin.top + this.margin.bottom)

        var view = svg.append("g")
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")

        var tooltip = d3.select("#hist-vis")
            .append("div")
              .style("opacity", 0)
              .attr("class", "tooltip")
              .style("padding", "5px")
              .style("width", "100px")
              .style("height", "15px")
              .style("font-anchor", "mid")

        this.mouseover = function(d){
          tooltip.html("<span style='color: black'>" + d.value + " students </span>")
            .style("left", (d3.mouse(this)[0]+10) + "px")
            .style("top", (d3.mouse(this)[1]) + "px")

          d3.select(this)
            .style("stroke", "gray")
            .style("fill-opacity", 1)

          tooltip
            .transition()
            .duration(200)
              .style("opacity", 1)
        }

        this.mousemove = function(d){
          tooltip
            .style("left", (d3.mouse(this)[0]+10) + "px")
            .style("top", (d3.mouse(this)[1]) + "px")
        }

        this.mouseleave = function(d){
          tooltip
            .transition()
            .duration(200)
              .style("opacity", 0)

          d3.select(this)
            .style("stroke", "none")
            .style("fill-opacity", 0.6)
        }

        var data_p = this.transformData(this.data, this.setting.key, this.isHist)

        //scale functions
        this.x = d3.scaleLinear()
          .domain([this.setting.x_domain.min, this.setting.x_domain.max])
          .range([0,this.width]);

        this.y = d3.scaleLinear()
          .domain([0, d3.max(data_p, function(d){ return d.value; })])
          .range([this.height, 0]);

        //axis
        this.xAxis = d3.axisBottom(this.x)
        this.yAxis = d3.axisLeft(this.y)

        //create the bar rectangles for histogram
        this.drawBars(view, data_p, "base", "gray")

        //x axis
        view.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + this.height + ")")
          .call(this.xAxis)
          .append("text")
            .attr("id", "x_title")
            .attr("fill", "#000")
            .attr("x", this.width / 2 )
            .attr("y", 60)
            .attr("text-anchor", "mid")
            .text(this.setting.x_axis)

        //y axis
        view.append("g")
          .attr("class", "y axis")
          .call(this.yAxis)
          .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("x", -this.height / 2)
            .attr("y", -60)
            .attr("text-anchor", "mid")
            .text("# of Students")


    }

    drawBars(view, data, bar_class, color){
      view.selectAll("." + bar_class)
        .data(data)
        .enter()
        .append("rect")
          .attr("class", bar_class)
          .attr("fill", color)
          .style("fill-opacity", 0.6)
          .attr("x", d => { return this.x(d.x0) })
          .attr("y", d => { return this.y(d.value) })
          .attr("width", d => { return this.x(d.x1) - this.x(d.x0) })
          .attr("height", d => { return this.height - this.y(d.value) })
        .on("mouseover", this.mouseover)
        .on("mousemove", this.mousemove)
        .on("mouseleave", this.mouseleave)
    }

    updateLinking(data, h_data){ //raw data
      this.data = data
      this.h_data = h_data
      this.update(this.setting, this.isHist)
    }

    updateDropdown(setting, isHist){ //not raw data
      this.update(setting, isHist)
    }

    update(setting, isHist){
      console.log("start update: ", setting.x_axis)
      this.setting = setting
      this.isHist = isHist

      //re-transform the data
      this.updateAxis()

      d3.select(this.html_root).select(".x.axis")
        .transition()
        .duration(1000)
        .call(this.xAxis)
        .select("#x_title")
          .text(this.setting.x_axis)
        .selectAll("text")


      d3.select(this.html_root).select(".y.axis")
        .transition()
        .duration(500)
        .call(this.yAxis)

      var data_p = this.transformData(this.data, this.setting.key, this.isHist)
      var h_data_p = this.transformData(this.h_data, this.setting.key, this.isHist)
      // update the rectangles
      var base_bars = d3.select(this.html_root).select("g").selectAll(".base").data(data_p)
      var highlight_bars = null
      if(h_data_p) highlight_bars = d3.select(this.html_root).select("g").selectAll(".highlight").data(h_data_p)

      // var tooltip = d3.select(".vis-container")
      //     .append("div")
      //       .style("opacity", 0)
      //       .attr("class", "tooltip")
      //       .style("background-color", "black")
      //       .style("border-radius", "2px")
      //       .style("padding", "5px")
      //       .style("width", "100px")
      //       .style("height", "15px")
      //       .attr("font-anchor", "mid")

      if(isHist){
        this.updateBars_Hist(base_bars, "gray", "base")
        if (highlight_bars) this.updateBars_Hist(highlight_bars, "#000000", "highlight")
      } else {
        this.updateBars_Bar(base_bars, "gray", "base")
        if (highlight_bars) this.updateBars_Bar(highlight_bars, "#000000", "highlight")
      }

      d3.selectAll(".base, .highlight")
        .on("mouseover", this.mouseover)
        .on("mousemove", this.mousemove)
        .on("mouseleave", this.mouseleave)
    }

    updateAxis(){
      var data_p = this.transformData(this.data, this.setting.key, this.isHist)
      if(this.isHist){
        this.x = d3.scaleLinear()
          .domain([this.setting.x_domain.min, this.setting.x_domain.max])
          .range([0,this.width]);
      } else {
        this.x = d3.scaleBand()
            .domain(data_p.map(d =>  d.key))
            .range([0, this.width])
            .padding(0.2)
      }
      this.xAxis = d3.axisBottom(this.x)
      this.y.domain([0, d3.max(data_p, d => d.value)])
    }

    updateBars_Hist(bars, color, bar_class){
      bars.enter()
        .append("rect")
        .attr("class", bar_class)
        .merge(bars)
          .transition()
          .duration(500)
            .attr("fill", color)
            .style("fill-opacity", 0.6)
            .attr("x", d => { return this.x(d.x0) })
            .attr("y", d => { return this.y(d.value)} )
            .attr("width", d => { return this.x(d.x1) - this.x(d.x0) })
            .attr("height", d => { return this.height - this.y(d.value)})

      bars.exit().remove()
    }

    updateBars_Bar(bars, color, bar_class){
      bars.enter()
        .append("rect")
        .attr("class", bar_class)
        .merge(bars)
          .transition()
          .duration(500)
            .attr("fill", color)
            .style("fill-opacity", 0.6)
            .attr("x", d => { return this.x(d.key) })
            .attr("y", d => { return this.y(d.value) })
            .attr("width", this.x.bandwidth())
            .attr("height", d => { return this.height - this.y(d.value) })

      bars.exit().remove()

    }


}
