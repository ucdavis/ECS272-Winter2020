(function () {
  // first, load the dataset from the JSON api
  d3.json('https://data.lacity.org/resource/g3qu-7q2u.json')
    .then(jsdata => {
      // clean data
      var data = jsdata.map(row=> {
        return {
            date: row['reportperiod'].substr(0, 10),
            terminal: row['terminal'],
            arrival_departure: row['arrival_departure'],
            domestic_international: row['domestic_international'],
            passenger_count: Number(row['passenger_count'])
        }
      }).filter(row => {
        // remove data on Misc. and Imperial terminals
        return (row['terminal'] != "Misc. Terminal") && (row['terminal'] !='Imperial Terminal')
      });
      var height = 400.0, width = 400.0;
      var margin = {left:60, right: 20, top: 80, bottom: 40};
      var svg = d3.select('#streamcontainer')
        .append('svg')
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom);
      svg.selectAll(".tick line").attr("stroke", "#b8b8b8");
          // Add X axis
      var draw_streamgraph_by_terminal = function(terminal) {
        var tdata = data.filter(d => d.terminal === terminal)
                        .map(d => {
                            return {
                                date: d.date,
                                group: d.domestic_international + " " + d.arrival_departure,
                                passenger_count: d.passenger_count
                            }
                        });
        var tip = document.getElementById("streamtip");
        tip.innerHTML = terminal + " passenger count by date";
        var groups = Array.from(new Set(tdata.map(d=>d.group))).sort();
        var group_sum = {};
        for (var _i in groups) {
            var gn = groups[_i];
            var filtered_data = tdata.filter(d => d.group == gn).map(d=>d.passenger_count);
            group_sum[gn] = 0;
            for (var _j in filtered_data) {
                group_sum[gn] += filtered_data[_j];
            }
        }
        var num_date = Array.from(new Set(tdata.map(d => d.date))).sort();
        var date_num = {};
        for (var _i=0; _i<num_date.length; ++_i){
          date_num[num_date[_i]] = _i;
        }
        var ntdata = d3.nest()
          .key(d=>d.date)
          .entries(tdata).map(d => {
            var ret_value = {date: date_num[d.key]};
            for (var item in groups) {
                ret_value[groups[item]] = 0;
            }
            for (var item in d.values){
                ret_value[d.values[item].group] = d.values[item].passenger_count;
            }
            return ret_value;
          });
        console.log(ntdata);
        var x = d3.scaleLinear()
          .domain([0, num_date.length])
          .range([0, width]);
        var y = d3.scaleLinear()
          .domain([0, 1500000])
          .range([height, 0]);
        var color = d3.scaleOrdinal()
          .domain(groups)
          .range(d3.schemeCategory10);
        var stackedData = d3.stack()
              .keys(groups)
              (ntdata)
        var area = d3.area()
            .x(function(d) {return x(d.data.date); })
            .y0(function(d) { return y(d[0]); })
            .y1(function(d) { return y(d[1]); })
        console.log(stackedData);
        
        svg.append("g")
          .attr("transform", "translate(" + margin.left + ", -" + margin.bottom + ")")
          .selectAll("streamlayers")
          .data(stackedData)
          .enter()
          .append("path")
          .attr("class", "streamarea")
          .style("fill", function(d) { return color(d.key); })
          .style("opacity", 1)
          .attr("d", area)
          .on("mouseenter", function(d) {
             d3.selectAll(".streamarea").style("opacity", 0.6);
          })
          .on("mousemove", function(d, i) {
              tip.innerHTML = terminal +" " + groups[i] + ": " + group_sum[groups[i]].toLocaleString() + " in total.";
              d3.select(this).style("opacity", 1.0);
          })
          .on("mouseleave", function(d) {
            d3.selectAll(".streamarea").style("opacity", 1);
            tip.innerHTML = terminal + " passenger count by date";
          });
        //add X axis
        svg.append("g")
        .attr("transform", "translate(0," + height *0.9 + ")")
        .call(d3.axisBottom(x).tickSize(-height* 0.7).tickValues([8, 16, 24]).tickFormat(n => num_date[n]))
        .select(".domain").remove() 
        // add Y axis
        svg.append("g")
          .attr("transform", "translate(" + margin.left + ", -" + margin.bottom + ")")
          .call(d3.axisLeft(y).ticks(6))
          .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("x", - height)
            .attr("y", - margin.left / 2)
            .attr("dy", "0.1em")
            .attr("text-anchor", "end")
            .text("Count");
      };

      // get passenger count by terminals
      var draw_pie_chart = function() {
        var terminal_names = new Set(Array.from(data.map(d=> {return d.terminal})));
        var passenger_count_by_terminal = {};
        terminal_names.forEach(tname => {
          passenger_count_by_terminal[tname] = 0;
        });
        data.forEach(d => {
            passenger_count_by_terminal[d.terminal] += d.passenger_count;        
        });
        var width = 500;
        var height = 500;
        var margin = {left: 60, right: 20, top: 20, bottom: 60}
        var radius = Math.min(width, height) / 2 - 20;
        var tooltip = document.getElementById('tooltip');
        
        var pie = d3.pie()
          .value(d => d.value);
        var data_ready = pie(d3.entries(passenger_count_by_terminal));
  
        var svg = d3.select('#container')
          .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);
  
        var color = d3.scaleOrdinal()
          .domain(passenger_count_by_terminal)
          .range(d3.schemeCategory10);
  
        var view = svg.append("g")
            .attr("transform", "translate(" + width / 2 + ", " + height / 2 + ")")
            .attr("stroke", "white");
        var arc = d3.arc().innerRadius(0).outerRadius(radius);
        var slices = view.selectAll("g.slice")
              .data(data_ready)
              .enter()
              .append("g")
                .attr("class", "slice")
                .style("opacity", 0.6);
        slices.append("path")
          .attr("d", arc)
          .attr("fill", d => {
              return color(d.data.key);
          })
          .append("title")
            .text(d => `${d.data.key}: ${d.data.value.toLocaleString()}`);
        var terminal_name_abbr = {
          "Terminal 1": "T1",
          "Terminal 2": "T2",
          "Terminal 3": "T3",
          "Terminal 4": "T4",
          "Terminal 5": "T5",
          "Terminal 6": "T6",
          "Terminal 7": "T7",
          "Terminal 8": "T8",
          "Tom Bradley International Terminal": "TBIT",
        };
        slices.append("text")
            .attr("stroke", "black")
            .attr("font-family", "sans-serif")
            .attr("font-size", 14)
            .attr("text-anchor", "middle")
            .attr("transform", d=> {
                  d.innerRadius = radius;
                  d.outerRadius = radius;
                  return "translate(" + arc.centroid(d) + ")";
              })
              .text(d => terminal_name_abbr[d.data.key]);
        slices
          .on("mouseenter", function(d) {
            d3.select(this).style('opacity', 1.0);
            tooltip.innerHTML = d.data.key + ": passenger count = " + d.data.value;
            d3.select("#streamcontainer > svg").selectAll("*").remove();
            draw_streamgraph_by_terminal(d.data.key);
          })
          .on('mouseleave', function(d) {
            d3.select(this).style('opacity', 0.6);
            tooltip.innerHTML = "";
          });
       };
    draw_pie_chart();        
    });
})()
