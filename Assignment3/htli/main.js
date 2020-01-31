(function () {
  // first, load the dataset from a CSV file
  d3.csv("../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv")
    .then(csv => {
      // log csv in browser console
      console.log(csv);
      // create data by selecting two columns from csv 
      var data = csv.map(row => {
        return {
          category: String(row['Category']),
          day: String(row['DayOfWeek']),
          district: String(row['PdDistrict'])
        }
      })

      //for pie chart - data by each district/category/day
      var dataByDis = d3.nest()
        .key(function (d) { return d.district; })
        .rollup(function (v) {
          return {
            per: v.length / data.length,
            count: v.length
          }
        })
        .entries(data);

      var dataByDayPie = d3.nest()
        .key(function (d) { return d.day; })
        .rollup(function (v) {
          return {
            per: v.length / data.length,
            count: v.length
          }
        })
        .entries(data);

      var types = Array.from(new Set(data.map(d => d.category)));
      var day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
      var days = Array.from(new Set(data.map(d => d.day))).sort((a, b) => {
        return day.indexOf(a) - day.indexOf(b);
      });

      //convert days to numbers
      var ndays = {};
      for (var i = 0; i < days.length; i++) {
        ndays[days[i]] = i;
      }

      var dataByDay = d3.nest()
        .key(function (d) { return d.day; }).sortKeys((a, b) => {
          return day.indexOf(a) - day.indexOf(b);
        })
        .key(function (d) { return d.category; })
        .rollup(function (leaves) { return leaves.length; })
        .entries(data)
        .map(d => {
          var obj = { day: ndays[d.key] };
          for (var t in types) {
            obj[types[t]] = 0;
          }
          for (var v in d.values) {
            obj[d.values[v].key] = d.values[v].value;
          }
          return obj;
        });

      var dataset = [];
      var keyword;
      //pie chart dimensions
      var width = 1100;
      var height = 700;
      var margin = { left: 60, right: 60, top: 20, bottom: 0 }

      var svg = d3.select('#container1')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)



      //pie chart - percentages by district/day
      var drawPieChart = function (op) {
        //set selected dataset
        if (op == "district") {
          dataset = dataByDis;
          keyword = "District";
        } else if (op == "day") {
          dataset = dataByDayPie;
          keyword = "Day";
        }

        var view1 = svg.append("g")
          .attr("transform", "translate(" + width / 1.8 + "," + height / 2.5 + ")").attr('display', 'inline-block');

        //color scale
        var color = d3.scaleOrdinal(["#98abc5", "#8a89a6", "#7b6887", "#6b486b", "#a05d57", "#d0743c", "#ff8c00"])
          .domain(dataset.map(d => d.key));

        var radius = Math.min(width, height) / 2.5;

        // Generate the pie
        var pie = d3.pie().value(function (d) {
          return d.value.per;
        });

        // Generate the arcs
        var arc = d3.arc()
          .innerRadius(0)
          .outerRadius(radius);

        //Generate groups
        var arcs = view1.selectAll("arc")
          .data(pie(dataset))
          .enter()
          .append("g")
          .attr("class", "arc")
          .attr("data", dataset)

        //Draw arc paths
        arcs.append("path")
          .attr("fill", function (d) {
            return color(d.data.key);
          })
          .attr("d", arc)
          .attr("class", d => "path " + d.data.key)

        var label = d3.arc()
          .outerRadius(radius)
          .innerRadius(radius - 120);

        arcs.append("text")
          .attr("transform", function (d) {
            return "translate(" + label.centroid(d) + ")";
          })
          .attr("text-anchor", "middle")
          .text(function (d) { return d.data.key; });


        var c;
        var tooltip = document.getElementById('tooltip1');
        arcs
          .on('mouseover', function (d) {
            c = d3.select('path.path.' + d.data.key).attr('fill');
            d3.select("path.path." + d.data.key).style('fill', 'orange');
            tooltip.innerHTML = keyword + ' = ' + d.data.key + '</br>Total Incidents = ' + d.data.value.count + '</br>Percentage = ' + (d.data.value.per * 100).toFixed(2) + "%";
          })
          .on('mouseout', function (d) {
            d3.select('path.path.' + d.data.key).style('fill', c);
            tooltip.innerHTML = "</br></br></br>";
          });


        //drop down list
        //Handler for dropdown value change
        var dropdownChange = function () {
          console.log("in dropdown");
          var op = d3.select(this).property('value');
          d3.select("#container1 > svg").selectAll("*").remove();
          drawPieChart(op);
        };
        var dropdown = d3.select('#selectButton');
        dropdown
          .on("change", dropdownChange);

        var ops = ["district", "day"];
        dropdown.selectAll("option")
          .data(ops)
          .enter().append("option")
          .attr("value", function (d) { return d; })
          .text(function (d) {
            return d[0].toUpperCase() + d.slice(1, d.length); // capitalize 1st letter
          });
      }


      //streamgraph
      var width1 = 1100;
      var height1 = 400;
      var margin1 = { left: 60, right: 60, top: 40, bottom: 80 }

      var svg1 = d3.select('#container2')
        .append('svg')
        .attr('width', width1 + margin1.left + margin1.right)
        .attr('height', height1 + margin1.top + margin1.bottom)

      var view2 = svg1.append("g")
        .attr("transform", "translate(" + margin1.left + ", " + margin1.top + ")");

      var x = d3.scaleLinear()
        .domain([0, days.length - 1])
        .rangeRound([0, width1]);
      // Add Y axis
      var y = d3.scaleLinear()
        .range([height1, 0])
        .domain([0, 25000]);

      var xAxis = svg1.append("g")
        .attr("transform", "translate(" + margin1.left + "," + height1 * 1.15 + ")")
        .call(d3.axisBottom(x).tickSize(-height1 * 1.1).tickValues([0, 1, 2, 3, 4, 5, 6]).tickFormat(n => days[n]))
        .select(".domain").remove()
      // Customization
      svg1.selectAll(".tick line").attr("stroke", "#b8b8b8")

      var ylAxis = view2.append("g")
        .call(d3.axisLeft(y).ticks(8));

      var yrAxis = view2.append("g")
        .attr("transform", "translate(" + (width1) + ", 0)")
        .call(d3.axisRight(y).ticks(8));

      var z = d3.scaleOrdinal()
        .range(d3.schemeSet3)
        .domain(types);

      // Add X axis label:
      view2.append("text")
        .attr("text-anchor", "end")
        .attr("x", width1 + 60)
        .attr("y", height1 + 60)
        .text("Time (day of week)");

      // Add Y axis label:
      view2.append("text")
        .attr("text-anchor", "end")
        .attr("x", -60)
        .attr("y", -10)
        .text("Number of Incidents")
        .attr("text-anchor", "start")

      //stack data for drawing areas
      var stackedData = d3.stack()
        .keys(types)
        (dataByDay);
      console.log(stackedData[1]);

      // Area generator
      var area = d3.area()
        .x(function (d) { return x(d.data.day); })
        .y0(function (d) { return y(d[0]); })
        .y1(function (d) { return y(d[1]); })

      // Show the areas
      var areas = view2
        .selectAll("mylayers")
        .data(stackedData)
        .enter()
        .append("path")
        .attr("class", function (d) { return "myArea " + d.key; })
        .style("fill", function (d) { return z(d.key); })
        .attr("d", area)
        .attr('opacity', 0.5)

      //tooltip
      var tooltip1 = document.getElementById('tooltip2');
      areas.on("mouseover", function (d) {
        d3.select('#tooltip2').style("opacity", 1)
        d3.selectAll(".myArea").style("opacity", .3)
        d3.select(this)
          .style("stroke", "black")
          .style("opacity", 1)
      })
        .on("mousemove", function (d, i) {
          mousex = d3.mouse(this);
          mousex = mousex[0];
          var invertedx = x.invert(mousex);
          invertedx = Math.round(invertedx);
          console.log(invertedx);
          var mouseday = days[invertedx];
          var val = d[invertedx].data[d.key];
          tooltip1.innerHTML = "Crime Category = " + d.key + "</br>Day = " + mouseday + "</br>Day Total = " + val;
        })
        .on("mouseleave", function (d) {
          d3.select('#tooltip2').style("opacity", 0)
          d3.selectAll(".myArea").style("opacity", 1).style("stroke", "none")
        })

      drawPieChart("district");
    })

})()


