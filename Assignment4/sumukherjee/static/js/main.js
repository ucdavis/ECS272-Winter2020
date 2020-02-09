var origData = null; //has all data {d.X, d.Y, d.cluster}
var select = false;
var selected_cluster_num = false;
window.onload = function() { // calls this on loading index.html
    $.get("loadData", function(data){ //first api call
      //origData = JSON.parse(data);
      groupedData= JSON.parse(data);
      //console.log(data);
      origData=groupedData.df;
      
      clusterData = groupedData.cluster_otherquestion;
      console.log(clusterData);
      renderScatter(origData);
      renderBar(clusterData,selected_cluster_num);
      
    });
  }

  function renderBar(data,cluster_number) {

      //var selected_cluster = d.cluster;
      var scoregroup = ['1.0','2.0','3.0','4.0','5.0'];
      var questions = ['Movies','History','Psychology','Internet'];
      var padding=40;


      var selecteddata  = [];
      
      data.forEach(function(d){
        if (cluster_number==false) { // should it be false or undefined/null?
          if (d.cluster=='all'){
            selecteddata.push(d)
          } 
        }
        else{
          if (d.cluster == cluster_number) {
            selecteddata.push(d)
          }
        } 
      });

      // for (let index = 0; index < data.length; index++) {
      //   var valuetemp = data[index].value;
      //   if (valuetemp < 3){
      //     data[index].group = 1
      //   }
      //   else{
      //     data[index].group = 2
      //   }  
      // }


      var margin = {top: 50, right: 160, bottom: 50, left: 30};

      var width = 1000 - margin.left - margin.right,
         height = 500 - margin.top - margin.bottom;

      var svg = d3.select("#bar")
                  .append("svg")
                  .attr("width", width + margin.left + margin.right)
                  .attr("height", height + margin.top + margin.bottom)
                  .append("g")
                  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      // The scale spacing the groups:
      var x0 = d3.scaleBand()
                 .rangeRound([0, width])
                 .domain(questions)
                 .paddingInner(0.5);


      // The scale for spacing each group's bar:
      var x1 = d3.scaleBand()
                 .domain(scoregroup)
                 .padding(0.05);

      var y = d3.scaleLinear()
                 .domain([0,700])
                 .rangeRound([height, 0]);

      var z = d3.scaleOrdinal()
                 .domain(scoregroup)
                 .range([ "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]); //"#98abc5", "#8a89a6",

      var yAxis = d3.axisLeft()
                 .scale(y)
                 .ticks(6);
      
      // var groupData = d3.nest()
      //            .key(function(d) { return d.question + d.group; })
      //            .rollup(function(v){
      //             function(v) { return d3.sum(v, function(d){return d.count}); }
      //            })
      //            .entries(data)
      //            .map(function(group){ 

      //             let d2 = {
      //               'question': d[0].question,
      //               'group': d[0].group,
      //           }
      //             d2
                   
      //             return d.value; });
               
      //console.log("groupData", groupData)
      


      console.log(selecteddata)

                 
      var stackData = d3.stack()
                 .keys(scoregroup)
                 (selecteddata)
                 //.offset(d3.stackOffsetExpand)
      console.log(stackData)

      x0.domain(clusterData.map(function(d) { return d.question; }));
      x1.domain(clusterData.map(function(d) { return d.group; }))
                   .rangeRound([0, x0.bandwidth()])
                   .padding(0.2);

      var serie = svg.selectAll(".serie")
                   .data(stackData)
                   .enter().append("g")
                     .attr("class", "serie")
                     .attr("fill", function(d) { return z(d.key); });
                 
      serie.selectAll("rect")
                   .data(function(d) { return d; })
                   .enter().append("rect")
                     .attr("class", "serie-rect")
                     .attr("transform", function(d) { return "translate(" + x0(d.data.question) + ",0)"; })
                     .attr("x", function(d) { return x1(d.data.group); })
                     .attr("y", function(d) { return y(d[1]); })
                     .attr("height", function(d) { return y(d[0]) - y(d[1]); })
                     .attr("width", x1.bandwidth())
                     .on("click", function(d, i){ console.log("serie-rect click d", i, d); });
                 
        svg.append("g")
                     .attr("class", "axis")
                     .attr("transform", "translate(0," + height + ")")
                     .call(d3.axisBottom(x0));
               
        svg.append("g")
                     .attr("class", "axis")
                     .call(d3.axisLeft(y).ticks(null, "s"))
                   .append("text")
                     .attr("x", 2)
                     .attr("y", y(y.ticks().pop()) + 0.5)
                     .attr("dy", "0.32em")
                     .attr("fill", "#000")
                     .attr("font-weight", "bold")
                     .attr("text-anchor", "start")
                     .text("Counts");

        //legends

        // svg.append('g')
        //         .attr('class', 'y axis')
        //         .attr('transform', 'translate(' + padding + ', 0)')
        //         .call(yAxis);

        var legend = svg.append('g')
                .attr('class', 'legend')
                .attr('transform', 'translate(' + (width + 12) + ', 0)')
                .attr("text-anchor", "end")
                     .attr("font-family", "sans-serif")
                     .attr("font-size", 10);

        legend.selectAll('rect')
                .data(scoregroup)
                .enter()
                .append('rect')
                .attr('x', 0)
                .attr('y', function(d, i){
                    return i * 18;
                })
                .attr('width', 12)
                .attr('height', 12)
                .attr('fill', function(d, i){
                    return z(i);
                });
            
        legend.selectAll('text')
                .data(scoregroup)
                .enter()
                .append('text')
                .text(function(d){
                    return d;
                })
                .attr('x', 18)
                .attr('y', function(d, i){
                    return i * 18;
                })
                .attr('text-anchor', 'start')
                .attr('alignment-baseline', 'hanging');
    
    function update(data) {


        var selecteddata  = [];
      
        data.forEach(function(d){
          if (cluster_number==false) {
            if (d.cluster=='all'){
              selecteddata.push(d)
            } 
          }
          else{
            if (d.cluster == cluster_number) {
              selecteddata.push(d)
            }
          } 
        });

        var stackData = d3.stack()
        .keys(scoregroup)
        (selecteddata)
        
        serie.data(stackData)

        serie.enter()
            .append("rect")
            .merge(serie)
            .transition()
            .duration(1000)
            .attr("x", function(d) { return x1(d.data.group); })
            .attr("y", function(d) { return y(d[1]); })
            .attr("height", function(d) { return y(d[0]) - y(d[1]); })
            .attr("width", x1.bandwidth())
        
      }

    if (selected_cluster_num != false){
      console.log(selected_cluster_num)
      update(data)
    }
    

  }

  function renderScatter(data) {
        var xmin = undefined,
            xmax = undefined,
            ymin = undefined,
            ymax = undefined;
        for (let loopVar = 0; loopVar < data.length; loopVar++) {
          if (xmin == undefined) {
            xmin = data[loopVar].X;
            xmax = data[loopVar].X;
            ymin = data[loopVar].Y;
            ymax = data[loopVar].Y;
          } else {
            if (xmin > data[loopVar].X) {
              xmin = data[loopVar].X;
            }
            if (xmax < data[loopVar].X) {
              xmax = data[loopVar].X;
            }
            if (ymin > data[loopVar].Y) {
              ymin = data[loopVar].Y;
            }
            if (ymax < data[loopVar].Y) {
              ymax = data[loopVar].Y;
            }
          }
        }
        xmin = Math.floor(xmin) - 1;
        ymin = Math.floor(ymin) - 1;
        xmax = Math.ceil(xmax) + 1;
        ymax = Math.ceil(xmax) + 1;
        var margin = {top: 10, right: 30, bottom: 30, left: 60},
            width = 800 - margin.left - margin.right,
            height = 600 - margin.top - margin.bottom;
        var color = d3.scaleOrdinal().domain(data)
            .range(["blue", "red", "green", "yellow", "black", "orange"]);
  

        var svg = d3.select("#scatter")
            .append("svg")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
            .append("g")
              .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scaleLinear()
            .domain([xmin, xmax])
            .range([ 0, width ]);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));
        
          // Add Y axis
        var y = d3.scaleLinear()
            .domain([ymin, ymax])
            .range([ height, 0]);
        svg.append("g")
            .call(d3.axisLeft(y));

          // Add dots
        svg.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("class", function (d) { return "dot c" + d.cluster } )
            .attr("cx", function (d) { return x(d.X); } )
            .attr("cy", function (d) {  return y(d.Y); } )
            .attr("r", 5)
            .style("fill", function (d) {
              return color(d.cluster);
            })
            .style("stroke", "black")
            .on("mouseover", function(d) {
              if (!select) {
                highlight(d);
              }
            })
            .on("mouseout", function(d) {
              if (!select) {
                doNotHighlight(d); 
              }
            })
            .on("click", function(d) {
              selected_cluster_num = d.cluster;
              console.log(selected_cluster_num);
              if (select == false) {
                select = true;
                highlight(d);
                updatebarchat(d);
              } else {
                select = false;
                selected_cluster_num = false;
                doNotHighlight(d);
              }
              

              //TODO: add barplot interaction code
              //here you have selected cluster so add update function from here
            });



            var highlight = function(d){
              selected_cluster = d.cluster;
              d3.selectAll(".dot")
                .transition()
                .duration(200)
                .style("fill", "lightgrey")
                .attr("r", 3)
          
              d3.selectAll(".c" + selected_cluster)
                .transition()
                .duration(200)
                .style("fill", color(selected_cluster))
                .attr("r", 7)
            }

            var doNotHighlight = function(d){
              d3.selectAll(".dot")
                .transition()
                .duration(200)
                .style("fill", function(dat) {return color(dat.cluster)})
                .attr("r", 5 )
            }
            renderBar(clusterData,selected_cluster_num);
            
}

function changeCluster() {
  $.ajax("cluster", {
    data: JSON.stringify({"clusterNum":$('#widget option:selected').text(), "dat":origData}),
    method: "POST",
    contentType: "application/json"
 }).done(function(data) {
   console.log(data);
   origData = JSON.parse(data);
   d3.select("#scatter").selectAll("*").remove();
   renderScatter(origData);
 });
}