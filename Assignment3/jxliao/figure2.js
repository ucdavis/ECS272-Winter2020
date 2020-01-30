// set the dimensions and margins of the graph
var margin2 = {top: 30, right: 100, bottom: 40, left: 100},
    width2 = 1000 - margin2.left - margin2.right,
    height2 = 400 - margin2.top - margin2.bottom;


// append the svg object to the body of the page
var svg2 = d3.select("#vis-stream").append("svg")
    .attr("width", width2 + margin2.left + margin2.right)
    .attr("height", height2 + margin2.top + margin2.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin2.left + "," + margin2.top + ")");


function updatedr2(startdate){

    var enddate_start = startdate.value;
    var updatedr2_option = document.getElementById("dr2");


    for (var i=enddate_start+1; i<=2019; i++ ) {
      var option = document.createElement("option");
      console.log(i);
      option.text = i;
      option.value = i;
      updatedr2_option.add(option);
    }

}



d3.csv('traffic_povit_dom.csv').then(function(data){
  var keys = data.columns.slice(1)
  console.log(keys)
  console.log(data[0].YearMonth)

  var parser = d3.timeParse("%m/%Y");
  //data.YearMonth = parser(data.YearMonth);
  console.log(parser(data[0].YearMonth))

  data.forEach(function(d) {
    d.YearMonth = parser(d.YearMonth);
    d.Passenger_Count = +d.Passenger_Count;
  });


  // Add X axis
  var x = d3.scaleTime()
          .domain(d3.extent(data, function(d) { return d.YearMonth; }))//[new Date(2006,0,1), new Date(2019, 2, 1)])    // values between for month of january
          .range([0,width2]);

  //console.log(d3.extent(data, function(d) { return d.YearMonth; }))

  // draw x axis with labels and move to the bottom of the chart area
  var xAxis = svg2.append("g")
            .attr("class", "axis")   // give it a class so it can be used to select only xaxis labels  below
            .attr("transform", "translate(0," + height2 +  ")")
            .call(d3.axisBottom(x));


  svg2.selectAll(".tick line").attr("stroke", "#b8b8b8")

  // Add X axis label:
  svg2.append("text")
      .attr("text-anchor", "end")
      .attr("x", margin2.left+30)
      .attr("y", height2 +margin2.top )
      .text("Time (year/month)");

  

  var y = d3.scaleLinear()
    .domain([-3000000, 3000000])
    .range([ height2, 0 ])

  svg2.append("g")
      .call(d3.axisLeft(y));

  svg2.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin2.left)
      .attr("x",0 - (height2 / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Passenger_Count");

  var color = d3.scaleOrdinal()
    .domain(keys)
    .range(["#4e79a7","#f28e2c","#e15759","#76b7b2","#59a14f","#edc949","#af7aa1","#ff9da7","#9c755f","#bab0ab"]);

  //stack the data

  var stackedData = d3.stack()
    .offset(d3.stackOffsetSilhouette)
    .keys(keys)
    (data)

  //console.log(stackedData)

  // svg2
  //   .selectAll("mylayers")
  //   .data(stackedData)
  //   .enter()
  //   .append("path")
  //     .style("fill", function(d) { return color(d.key); })
  //     .attr("d", d3.area()
  //       .x(function(d, i) { return x(d.data.YearMonth); })
  //       .y0(function(d) { return y(d[0]); })
  //       .y1(function(d) { return y(d[1]); })
  //   )



  // // create a tooltip
   var Tooltip = svg2
     .append("text")
     .attr("x", 0)
     .attr("y", 0)
     .style("opacity", 0)
     .style("font-size", 17)

  // // Three function that change the tooltip when user hover / move / leave a cell
   var mouseover = function(d) {
     Tooltip.style("opacity", 1)
     d3.selectAll(".myArea").style("opacity", .2)
     d3.select(this)
       .style("stroke", "black")
       .style("opacity", 1)
   }
   var mousemove = function(d,i) {
     grp = keys[i]

     Tooltip.text(grp)
   }
   var mouseleave = function(d) {
     Tooltip.style("opacity", 0)
     d3.selectAll(".myArea").style("opacity", 1).style("stroke", "none")
    }

   // Area generator
   var area = d3.area()
     .x(function(d) { return x(d.data.YearMonth); })
     .y0(function(d) { return y(d[0]); })
     .y1(function(d) { return y(d[1]); })

  // console.log(area)

  // // Show the areas
  var stackplot = svg2
     .selectAll("mylayers")
     .data(stackedData)
     .enter()
    .append("path")
      .attr("class", "myArea")
      .style("fill", function(d) { return color(d.key); })
      .attr("d", area)
      .on("mouseover", mouseover)
      .on("mousemove", mousemove)
      .on("mouseleave", mouseleave)


  var Group_options = ["Passenger_Count_Domestic", "Passenger_Count_International"]
  var Terminals = ["Imperial Terminal","Misc. Terminal","Terminal 1","Terminal 2","Terminal 3","Terminal 4","Terminal 5","Terminal 6","Terminal 7","Terminal 8","International Terminal"]
  
  var years_range = ["2006","2007", "2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019"]

  d3.select("#dr1")
      .selectAll('myOptions')
      .data(years_range)
      .enter()
      .append('option')
      .text(function (d) { return d; }) // text showed in the menu
      .attr("value", function (d) { return d; }) // corresponding value returned by the button

  d3.select("#dr2")
      .selectAll('myOptions')
      .data(years_range)
      .enter()
      .append('option')
      .text(function (d) { return d; }) // text showed in the menu
      .attr("value", function (d) { return d; }) // corresponding value returned by the button



  function updateyear() {
    var opt1 = $('#dr1 option:selected').val();
    var opt2 = $('#dr2 option:selected').val();

    console.log(opt1)

    svg2.append("svg:clipPath")
    .attr("id", "clipper")
    .append("svg:rect")
    .style("stroke", "gray")
    .style("fill", "black")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", width2)
    .attr("height", height2);

    // Update X axis
    x.domain([parser("01/" + opt1),parser("01/" + opt2)]).range([0,width2])
    xAxis.transition().duration(1000).call(d3.axisBottom(x))

    stackplot
     .transition()
     .duration(1000)
      .attr("class", "myArea")
      .style("fill", function(d) { return color(d.key); })
      .attr("d", area)
      .attr("clip-path", "url(#clipper)")

    stackplot
        .exit()
    .remove()
  }

  d3.select("#dr1").on("input", function() {
    updateyear();
  });

  d3.select("#dr2").on("input", function() {
    updateyear();
  });


})