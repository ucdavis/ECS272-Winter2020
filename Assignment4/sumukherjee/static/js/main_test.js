var origData = null; //has all data {d.X, d.Y, d.cluster}
var select = false;
var selected_cluster_num = -1;
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

  function renderBar(data,selected_cluster_num) {

      //var selected_cluster = d.cluster;
      // if ('1.0' in Object.keys(data[0])) {
      //   var scoregroup = ['1.0','2.0','3.0','4.0','5.0'];
      // }
      // else if ('1' in Object.keys(data[0])) {
      //   var scoregroup = ['1','2','3','4','5'];
      // }

      var scoregroup = ['1.0','2.0','3.0','4.0','5.0'];
      
      var questions = ['Movies','History','Psychology','Internet'];
      var padding=40;


      var selecteddata  = [];
      
      data.forEach(function(d){
        if (selected_cluster_num <0 ) { // should it be false or undefined/null?
          if (d.cluster=='all'){
            //d.pn = 
            selecteddata.push(d)
          } 
        }
        else{
          if (d.cluster == selected_cluster_num) {
            selecteddata.push(d)
          }
        } 
      });

      console.log(selecteddata)
      console.log(selecteddata[0])

      var margin = {top: 50, right: 160, bottom: 50, left: 30};

      var width = 1000 - margin.left - margin.right,
         height = 500 - margin.top - margin.bottom;

      var svg = d3.select("#bar")
                  .append("svg")
                  .attr("width", width + margin.left + margin.right)
                  .attr("height", height + margin.top + margin.bottom)
                  .append("g")
                  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                  // List of groups = species here = value of the first column called group -> I show them on the X axis
                
                  // Add X axis
      var x = d3.scaleBand()
                      .domain(questions)
                      .range([10, width])
                      .padding([0.2])
                  svg.append("g")
                    .attr("transform", "translate(0," + height + ")")
                    .call(d3.axisBottom(x).tickSize(0));
                
                  // Add Y axis
      var y = d3.scaleLinear()
                    .domain([0, 700])
                    .range([ height, 0 ]);
                  svg.append("g")
                    .call(d3.axisLeft(y));
                
                  // Another scale for subgroup position?
        var xSubgroup = d3.scaleBand()
                    .domain(scoregroup)
                    .range([0, x.bandwidth()])
                    .padding([0.05])
                
                  // color palette = one color per subgroup
        var color = d3.scaleOrdinal()
                    .domain(scoregroup)
                    .range([ "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"])
                
                  // Show the bars
                  svg.append("g")
                    .selectAll("g")
                    // Enter in data = loop group per group
                    .data(selecteddata)
                    .enter()
                    .append("g")
                      .attr("transform", function(d) { return "translate(" + x(d.question) + ",0)"; })
                    .selectAll("rect")
                    .data(function(d) {
                      return scoregroup.map(function(key) { 
                        if (key.length == 1){
                          key = key + '.0'
                        }
                        return {key: key, value: d[key]}; }); })
                    .enter().append("rect")
                      .attr("x", function(d) { return xSubgroup(d.key); })
                      .attr("y", function(d) { return y(d.value); })
                      .attr("width", xSubgroup.bandwidth())
                      .attr("height", function(d) { return height - y(d.value); })
                      .attr("fill", function(d) { return color(d.key); });
                

        //legends

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
                    return color(i);
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

        console.log("scttarplot")
        console.log(data[0])

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
              
              if (select == false) {
                selected_cluster_num = d.cluster;
                console.log(selected_cluster_num);
                select = true;
                highlight(d);
                d3.select("#bar").selectAll("*").remove();
                renderBar(clusterData,selected_cluster_num);
              } else {
                select = false;
                selected_cluster_num = -1;
                doNotHighlight(d);
                d3.select("#bar").selectAll("*").remove();
                renderBar(clusterData,selected_cluster_num);
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

            //renderBar(clusterData,selected_cluster_num);
            
}

function changeCluster() {
  $.ajax("cluster", {
    data: JSON.stringify({"clusterNum":$('#widget option:selected').text(), "dat":origData}),
    method: "POST",
    contentType: "application/json"
 }).done(function(data) {
    
   groupedData = JSON.parse(data);

   origData=groupedData.df;
   
   clusterData = groupedData.cluster_otherquestion;
   console.log(clusterData)
   d3.select("#scatter").selectAll("*").remove();
   d3.select("#bar").selectAll("*").remove();
   renderScatter(origData);
   renderBar(clusterData,-1);
 });
}