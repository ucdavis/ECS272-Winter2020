
const width = 1080;
const height = 500;
const svg = d3.select("div#div1").append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")

    .attr("viewBox", "-100 -200 1300 1800")
    .style("padding", 5)
    .style("margin", 5)
    .classed("svg-content", true);

const dataset = d3.csv('./smallset.csv')
dataset.then(function(data) {
    const monthlyPassenger = data.columns.slice(2).map(function(id) {
        return {
            id: id,
            values: data.map(function(d){
                return {
                    YM: d.Year_Month,
                    terminal: id,
                    date: d3.timeParse("%Y-%m-%d")(d.Year_Month),
                    measurement: +d[id]
                };
            })
        };
    });


    const scale_x = d3.scaleTime().range([0,width]);
    const scale_y = d3.scaleLinear().rangeRound([height, 0]);
    scale_x.domain(d3.extent(data, function(d){
        return d3.timeParse("%Y-%m-%d")(d.Year_Month)}));
    scale_y.domain([(0), d3.max(monthlyPassenger, function(c) {
        return d3.max(c.values, function(d) {
            return d.measurement + 5; });
            })
        ]);

    const y_axis = d3.axisLeft().scale(scale_y); 
    const x_axis = d3.axisBottom().scale(scale_x);

    const line = d3.line()
        .x(function(d) { return scale_x(d.date); })
        .y(function(d) { return scale_y(d.measurement); });

    let counter = 0;
    const line_counter = function () {
        var ret = "line-"+counter;
        counter++;
        return ret;
    }

    const tool = d3.select("body").append("div")
        .attr("class", "tool")
        .style("position", "absolute");

    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + height + ")")
        .call(x_axis)
        
    svg.append("g")
        .attr("class", "axis")
        .call(y_axis)
        .append("text")
        .text("Passenger Count");

    const lines = svg.selectAll("lines")
        .data(monthlyPassenger)
        .enter()
        .append("g");
        
        lines.append("path")
        .attr("class", line_counter)
        .attr("d", function(d) { return line(d.values); });

        lines.append("text")
        .datum(function(d) {
            return {
                id: d.id,
                value: d.values[d.values.length - 1]}; })
        .attr("transform", function(d) {
                return "translate(" + (scale_x(d.value.date) + 10)  
                + "," + (scale_y(d.value.measurement) + 5 ) + ")"; })
        .attr("x", 5);
        

    lines.selectAll("points")
    .data(function(d) {return d.values})
    .enter()
    .append("circle")
    .attr("cx", function(d) { return scale_x(d.date); })      
    .attr("cy", function(d) { return scale_y(d.measurement); })    
    .attr("r", 1)
    .attr("class","point")
    .style("opacity", 1)

    lines.selectAll("circles")
    .data(function(d) { return(d.values); } )
    .enter()
    .append("circle")
    .attr("cx", function(d) { return scale_x(d.date); })      
    .attr("cy", function(d) { return scale_y(d.measurement); })    
    .attr('r', 5)
    .style("opacity", 0)
    .on('mouseover', function(d) {
        tool.transition()
    .delay(30)
        .duration(100)
        .style("opacity", 1);
        tool.html(
            "Time: " + d.YM + "<br/>" +
            "Terminal: " + d.terminal + "<br/>" +
            "Total passengers: " + d.measurement)
        .style("background", "#87C4F0")
        .style("text-align", "center")
        .style("left", (d3.event.pageX + 20) + "px")
        .style("top", (d3.event.pageY) + "px");
        const selection = d3.select(this).raise();
        selection
        .transition()
        .delay("20")
        .duration("200")
        .attr("r", 5)
        .style("opacity", 1)
        .style("fill","black")
    })                
    .on("mouseout", function(d) {      
        tool.transition()        
        .duration(100)      
        .style("opacity", 0);  
        const selection = d3.select(this);
        selection
        .transition()
        .delay("2")
        .duration("100")
        .attr("r", 5)
        .style("opacity", 0);
    });
});

