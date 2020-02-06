window.onload = function() {
    $.get("output1", function(data){
        data = JSON.parse(data);
        var margin = {top: 10, right: 30, bottom: 30, left: 60},
            width = 500 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

        var svg = d3.select("#scatter")
            .append("svg")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
            .append("g")
              .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scaleLinear()
            .domain([0, 5])
            .range([ 0, width ]);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));
        
          // Add Y axis
        var y = d3.scaleLinear()
            .domain([0, 5])
            .range([ height, 0]);
        svg.append("g")
            .call(d3.axisLeft(y));

          // Add dots
        svg.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
            .attr("cx", function (d) { console.log(x(d["Music"]));console.log(y(d["Slow songs or fast songs"]));return x(d["Music"]); } )
            .attr("cy", function (d) {  return y(d["Slow songs or fast songs"]); } )
            .attr("r", 5)
            .style("fill", "#69b3a2")
      });
    
    }