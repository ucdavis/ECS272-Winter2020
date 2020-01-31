d3.csv('../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv')
  .then(csv => {
      // create data by selecting two columns from csv
      var data = csv.map(row => {
        return {
          lon: Number(row['X']),
          lat: Number(row['Y']),
          weekday: String(row['DayOfWeek']),
          date: row['Date'].substr(0,10),
          time: row['Time'],
          dist: String(row['PdDistrict']),
          res: String(row['Resolution']),
          cat: String(row['Category'])
        }
      });

      data = data.filter(function(d){
        return d.dist != "";
      });

      var data_heat = d3.nest()
        .key(function(d) { return d.res; })
        .sortKeys(d3.ascending)
        .key(function(d) { return d.cat; })
        .sortKeys(d3.ascending)
        .rollup(function(v) {
          return {
            count: v.length
          }})
        .entries(data);
      console.log(data_heat);


      var data_str = d3.nest()
        .key(function(d) { return d.date; })
        .sortKeys(d3.ascending)
        .key(function(d) { return d.dist; })
        .sortKeys(d3.ascedning)
        .rollup(function(v){
          return v.length;
          })
        .entries(data);
      console.log(data_str);

      var uniqueDay = d3.map(data, function(d){ return d.weekday; }).keys(); //7
      var uniqueRes = d3.map(data, function(d){ return d.res; }).keys().sort(); //14
      var uniqueCat = d3.map(data, function(d){ return d.cat; }).keys().sort(); //39
      var uniqueDis = d3.map(data, function(d){ return d.dist; }).keys().sort(); //10
      var uniqueDate = d3.map(data, function(d){ return d.date; }).keys(); //366
      var process_date = uniqueDate.map(function(d){
        return new Date(d);
      });
      console.log(uniqueDis);



      /*********************************
      * Visualization codes start here
      * ********************************/
      var width = 800;
      var height = 600;
      var margin = {left: 60, right: 20, top: 20, bottom: 60}

      /*********************************
      * Basic visualization: Heatmap
      * ********************************/

      var svg = d3.select('#container')
        .append('svg')
          .attr('width', width + margin.left + margin.right + 100)
          .attr('height', height + margin.top + margin.bottom + 100)

      var view = svg.append("g")
        .attr("transform", "translate(" + (margin.left+90) + "," + margin.top + ")");

      //Axes
      var x = d3.scaleBand()
        .domain(uniqueRes)
        .range([0, width])
        .padding(0.1);

      view.append("g")
        .attr("transform", "translate(0," + (height + 20) + ")")
        .style("font-size", 6)
        .call(d3.axisBottom(x).ticks(0))
        .select(".domain").remove();

      view.selectAll("text")
        .attr("x", - 20)
        .attr("y", 20)
        .attr("transform", "rotate(-45)");

      var y = d3.scaleBand()
        .domain(uniqueCat)
        .range([height, 0])
        .padding(0.3);

      view.append("g")
        .style("font-size", 8)
        .call(d3.axisLeft(y).ticks(0))
        .select(".domain").remove();

      //Color encoding, tooltip, dropdownMenu for color encoding.
      var color_choice = ["YlOrRd", "Plasma", "Viridis", "YlGnBu"];

      var color = d3.scaleSequential()
        .interpolator(d3.interpolateYlOrRd)
        .domain([-100,600])


      var tooltip = d3.select("#container")
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("border", "none")
        .style("border-radius", "5px")
        .style("padding", "2px")
        .style("position", "absolute")
        .style("margin", "0 auto")
        .style("text-align", "center")
        .style("width", "90px")
        .style("height", "10px")
        .style("background-color", "black")
        .style("font-size", "8px")
        .style("font-family", "Helvetica")
        .style("color", "white")


      //dropdown menu
      var dropdownChange = function(){
        var choice = d3.select(this).property("value");
      };

      var dropdown = d3.select("#container")
        .insert("select", "svg")
        .on("change", dropdownChange);

      dropdown.selectAll("option")
        .data(color_choice)
        .enter()
        .append("option")
        .attr("value", function(d) { return d; })
        .text(function(d) { return d; });

      //plot the data.
      view.selectAll()
        .data(data)
        .enter()
        .append("rect")
          .attr("x", function(d){ return x(d.res) })
          .attr("y", function(d){ return y(d.cat) })
          .attr("rx", 4)
          .attr("ry", 4)
          .attr("width", x.bandwidth() )
          .attr("height", y.bandwidth() )
          .style("fill", function(d) {
            var v = data_heat.find( g => g.key == d.res).values
                      .find( h => h.key == d.cat).value
                      .count;
            return color(v);
          })
          .style("stroke-width", 2)
          .style("stroke", "none")
          .style("opacity", 0.5)
        .on("mouseover", function(d){
          var v = data_heat.find( g => g.key == d.res).values
                    .find( h => h.key == d.cat).value
                    .count;
          if (v > 0){
            tooltip.transition()
              .duration(50)
              .style("opacity", 0.8);
            tooltip.html(v + " incidents in total. ")
              .style("left", (d3.event.pageX) + "px")
              .style("top", (d3.event.pageY - 20) + "px");
          };
        })
        .on("mouseleave", function(d){
          tooltip.transition()
            .duration(150)
            .style("opacity", 0);
        })


      /*********************************
      * Advanced visualization: alluvial diagram
      * ********************************/

      width = 1200;

      var svg2 = d3.select('#container2')
        .append('svg')
          .attr('width', width + margin.left + margin.right + 100)
          .attr('height', height + margin.top + margin.bottom + 100)

      var view2 = svg2.append("g")
        .attr("transform", "translate(" + (margin.left+90) + "," + margin.top + ")");

      var x2 = d3.scaleTime()
        .domain([d3.min(process_date), d3.max(process_date)])
        .range([0, width]);

      view2.append("g")
        .attr("transform", "translate(0," + (height + 20) + ")")
        .call(d3.axisBottom(x2).ticks(d3.timeMonth.every(1)).tickFormat(d3.timeFormat("%B")));

      var y2 = d3.scaleLinear()
        .domain([0, 100000])
        .range([height, 0]);

      view2.append("g")
        .call(d3.axisLeft(y2));

      var color2 = d3.scaleOrdinal()
        .domain(uniqueDis)
        .range(d3.schemeSpectral[11]);

      var stack = d3.stack()
        .keys(uniqueDis)
        .offset(d3.stackOffsetWiggle)
        .order(d3.stackOrderInsideOut)
        (data_str)
      console.log(stack);
      /*
      svg2.selectAll("mylayers")
        .data(stack)
        .enter()
        .append("path")
          .style("fill", function(d) { return color2(d.key); })
          .attr("d", d3.area()
            .x(function(d, i) { return x(d.date); })
        )*/
});
