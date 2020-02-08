var origData = null; //has all data {d.X, d.Y, d.cluster}
var select = false;
window.onload = function() { // calls this on loading index.html
    $.get("loadData", function(data){ //first api call
      origData = JSON.parse(data);
      renderScatter(origData);
      renderBar(origData);
    });
  }

  function renderBar(data) {
//     var margin = {top: 20, right: 160, bottom: 35, left: 30};

// var width = 960 - margin.left - margin.right,
//     height = 500 - margin.top - margin.bottom;

// var svg = d3.select("#bar")
//   .append("svg")
//   .attr("width", width + margin.left + margin.right)
//   .attr("height", height + margin.top + margin.bottom)
//   .append("g")
//   .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

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
              console.log(d.cluster);
              if (select == false) {
                select = true;
                highlight(d);
              } else {
                select = false;
                doNotHighlight(d);
              }
              //TODO: add barplot interaction code
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