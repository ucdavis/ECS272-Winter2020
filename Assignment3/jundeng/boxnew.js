//x is the type of crime, y is the total amount of that crime
(function () {
  // first, load the dataset from a CSV file
  d3.csv('../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv')
    .then(csv => {
      // log csv in browser console
      //console.log(csv);

      // select Category row
      var data = csv.map(row => {
        return {
          Category: String(row['Category']),
          Day: String(row["DayOfWeek"]),
          Location_x: Number(row["X"]),
          Location_y: Number(row["Y"]),
          Date:Date(row['Date']),
          PdDistrict:String(row['PdDistrict'])
        }
      })
      
      //group by category then count for bar chart
      var crimeCount=d3.nest()
      .key(function(d){return d.Category;})
      .rollup(function(v){return v.length;})
      .entries(data)
      
      
    //console.log(crimeCount);   
      
      //group by category then count for bar chart
      var dayCount=d3.nest()
      .key(function(d){return d.Day;})
      .key(function(d){return d.Category;})
      .rollup(function(v){return v.length;})
      .entries(data)
      //console.log(dayCount);
      //      .rollup(function(v){return v.length;})
      
      //sort by occurance
      crimeCount.sort(function(b,a){
          return a.value-b.value;
      });
      /********************************* 
      * Bar Chart Visualization codes start here
              * ********************************/
        var margin = {top: 30, right: 40, bottom: 150, left: 100},
            width = 700 - margin.left - margin.right,
            height = 700 - margin.top - margin.bottom;

    // append the svg object to the body of the page
        var svg = d3.select("#container")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");
      
      var view = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
       
/*var tempY = 20000;
//slider 
  var data = [0,5000, 10000, 15000, 20000, 25000,30000,35000,40000,45000,50000,55000];

  var sliderSimple = d3
    .sliderBottom()
    .min(d3.min(data))
    .max(d3.max(data))
    .width(700)
    .ticks(10)
    .default(20000)
    .on('onchange', val=> {
      d3.select('p#value-simple').text(d3.val);
    });
      

  var gSimple = d3
    .select('div#slider-simple')
    .append('svg')
    .attr('width', 750)
    .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)');

  gSimple.call(sliderSimple);*/

      // X axis
      var x = d3.scaleBand()
        .range([ 0, width ])
        .domain(crimeCount.map(function(d) { return d.key; }))
        .padding(0.2);
      
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
      
        .selectAll("text")
          .attr("transform", "translate(-30,0)rotate(-45)")
          .style("text-anchor", "end");


    // Add Y axis
      var y = d3.scaleLinear()
        .domain([0, 20000])
        .range([ height, 0]);
      
      svg.append("g")
        .call(d3.axisLeft(y));

      var color = d3.scaleOrdinal(d3.schemeCategory10);
      var tooltip = d3.select("body").append("div").attr("class", "toolTip");
      
      // Bars
      svg.selectAll("mybar")
        .data(crimeCount)
        .enter()
        .append("rect")
          .attr("x", function(d) { return x(d.key); })
          .attr("y", function(d) { return y(d.value); })
          .attr("width", x.bandwidth())
          .attr("height", function(d) { return height - y(d.value); })
          .attr("fill", function(d, i) {
            return color(i);
          })
          .attr("id", function(d, i) {
            return i;
            })
          .on("mouseover",function(d){
          d3.select(this).attr("fill","blue");
          tooltip
          .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html((d.key) + "<br>" + + (d.value));})
      
          .on("mouseout", function(d, i) {
            d3.select(this).attr("fill", function() {
                tooltip.style("display", "none");
                return "" + color(this.id) + "";
            });
      })
      /********************************* 
      * Parallel Coordinate Visualization codes start here
              * ********************************/
var margin1 = {top: 30, right: 40, bottom: 20, left: 200},
    width1 = 960 - margin1.left - margin1.right,
    height1 = 500 - margin1.top - margin1.bottom;

var dimensions = [
  {
    name: "Category",
    scale: d3.scaleOrdinal(crimeCount.keys(),[0, height1]),
    type: "string"
  },
  {
    name: "DayOfWeek",
    scale: d3.scaleOrdinal(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],[0, height1]),
    type: "string"
  },
  {
    name: "PdDistrict",
    scale: d3.scaleOrdinal(dayCount.keys(),[0, height1]),
    type: "string"
  },
  {
    name: "X",
    scale: d3.scaleLinear().domain([37.7784,37.81]).range([height1, 0]),
    type: "number"
  },
  {
    name: "Y",
    scale: d3.scaleLinear().domain([-122.36,-122.52]).range([height1, 0]),
    type: "number"
  },
];
      
var x1 = d3.scaleOrdinal()
    .domain(dimensions.map(function(d) { return d.Category; }))
    .range([0, width1]);
 
var line = d3.line()
    .defined(function(d) { return !isNaN(d[1]); });
      
var yAxis = d3.axisLeft();
      
var svg1 = d3.select("#parallel").append("svg")
    .attr("width", width1 + margin1.left + margin1.right)
    .attr("height", height1 + margin1.top + margin1.bottom)
  .append("g")
    .attr("transform", "translate(" + margin1.left + "," + margin1.top + ")");

var dimension = svg1.selectAll(".dimension")
    .data(dimensions)
  .enter().append("g")
    .attr("class", "dimension")
    .attr("transform", function(d) { return "translate(" + x1(d.Category) + ")"; });

/*
d3.csv("../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv", function(data1) {
  dimensions.forEach(function(dimension) {
    dimension.scale.domain(dimension.type === "number"
        ? d3.extent(data, function(d) { return +d[dimension.Category]; })
        : data.map(function(d) { return d[dimension.Category]; }).sort());
  });

  svg1.append("g")
      .attr("class", "background")
    .selectAll("path")
      .data(data1)
    .enter().append("path")
      .attr("d", draw);

  svg1.append("g")
      .attr("class", "foreground")
    .selectAll("path")
      .data(data1)
    .enter().append("path")
      .attr("d", draw);

  dimension.append("g")
      .attr("class", "axis")
      .each(function(d) { d3.select(this).call(yAxis.scale(d.scale)); })
    .append("text")
      .attr("class", "title")
      .attr("text-anchor", "middle")
      .attr("y", -9)
      .text(function(d) { return d.Category; });

  var ordinal_labels = svg1.selectAll(".axis text")
      .on("mouseover", mouseover)
      .on("mouseout", mouseout);

  var projection = svg1.selectAll(".background path,.foreground path")
      .on("mouseover", mouseover)
      .on("mouseout", mouseout);

  function mouseover1(d) {
    svg1.classed("active", true);

    // this could be more elegant
    if (typeof d === "string") {
      projection.classed("inactive", function(p) { return p.Category !== d; });
      projection.filter(function(p) { return p.Category === d; }).each(moveToFront);
      ordinal_labels.classed("inactive", function(p) { return p !== d; });
      ordinal_labels.filter(function(p) { return p === d; }).each(moveToFront);
    } else {
      projection.classed("inactive", function(p) { return p !== d; });
      projection.filter(function(p) { return p === d; }).each(moveToFront);
      ordinal_labels.classed("inactive", function(p) { return p !== d.name; });
      ordinal_labels.filter(function(p) { return p === d.Category; }).each(moveToFront);
    }
  }

  function mouseout1(d) {
    svg1.classed("active", false);
    projection.classed("inactive", false);
    ordinal_labels.classed("inactive", false);
  }

  function moveToFront() {
    this.parentNode.appendChild(this);
  }
});

function draw(d) {
  return line(dimensions.map(function(dimension) {
    return [x(dimension.Category), dimension.scale(d[dimension.Category])];
  }));
    
}*/
  })
})
  ()

function myFunction(){
d3.csv('../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv')
    .then(csv => {
      // log csv in browser console
      //console.log(csv);

      // select Category row
      var data = csv.map(row => {
        return {
          Category: String(row['Category']),
          Day: String(row["DayOfWeek"]),
          Location_x: Number(row["X"]),
          Location_y: Number(row["Y"])
        }
      })
      //group by category then count for bar chart
      var crimeCount=d3.nest()
      .key(function(d){return d.Category;})
      .rollup(function(v){return v.length;})
      .entries(data)
      //console.log(crimeCount);   
      
      //group by category then count for bar chart
      var dayCount=d3.nest()
      .key(function(d){return d.Day;})
      .key(function(d){return d.Category;})
      .rollup(function(v){return v.length;})
      .entries(data)
      //console.log(dayCount);
      //      .rollup(function(v){return v.length;})
      
      //sort by occurance
      crimeCount.sort(function(b,a){
          return a.value-b.value;
      });
      /********************************* 
      * Bar Chart Visualization codes start here
              * ********************************/
        var margin = {top: 30, right: 20, bottom: 150, left: 100},
            width = 700 - margin.left - margin.right,
            height = 700 - margin.top - margin.bottom;

    // append the svg object to the body of the page
        var svg = d3.select("#container")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");
      
      var view = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
//update 
    var selectYval = document.getElementById("selectY").value;
    console.log(selectYval);
    
      // X axis
      var x = d3.scaleBand()
        .range([ 0, width ])
        .domain(crimeCount.map(function(d) {return d.key; }))
        .padding(0.2);
      
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
      
        .selectAll("text")
          .attr("transform", "translate(-30,0)rotate(-45)")
          .style("text-anchor", "end");


    // Add Y axis
      var y = d3.scaleLinear()
        .domain([0, selectYval])
        .range([ height, 0]);
      
      svg.append("g")
        .call(d3.axisLeft(y));

      var color = d3.scaleOrdinal(d3.schemeCategory10);
      var tooltip = d3.select("body").append("div").attr("class", "toolTip");
      
      // Bars
      svg.selectAll("mybar")
        .data(crimeCount)
        .enter()
        .append("rect")
          .attr("x", function(d) { return x(d.key); })
          .attr("y", function(d) { return y(d.value); })
          .attr("width", x.bandwidth())
          .attr("height", function(d) { return height - y(d.value); })
          .attr("fill", function(d, i) {return color(i);})
          .attr("id", function(d, i) {return i;})
          .on("mouseover",function(d){d3.select(this).attr("fill","blue");
          tooltip
          .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html((d.key) + "<br>" + + (d.value));})
      
          .on("mouseout", function(d, i) {
            d3.select(this).attr("fill", function() {
                tooltip.style("display", "none");
                return "" + color(this.id) + "";
            });
      })
       
})}
          