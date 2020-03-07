
var margin = {top: 80, right: 180, bottom: 80, left: 180};
var width = 960 - margin.left - margin.right;
var height = 500 - margin.top - margin.bottom;
barPadding = 10;

var weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

var svg = d3.select("body")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv('../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv')
  .then(csv => {

  // create data by selecting columns from csv
  var data = csv.map(row => {
    return {
      categoryOfCrime: String(row['Category']),
      dayOfWeek: String(row['DayOfWeek']),
    }})
    console.log(data);

//crimesByDayandCategory first sorted by day and crimecategory --> value = number
  var crimesByCategoryandDay = d3.nest()
      .key(function(d) { return d.categoryOfCrime; })
      .key(function(d) { return d.dayOfWeek; }).sortKeys(function(a,b) { return weekDays.indexOf(a) - weekDays.indexOf(b); })
      .rollup(function(leaves) { return leaves.length; })
      .entries(data);
      // console.log(data);
      console.log(crimesByCategoryandDay);

  var crimeCategories = crimesByCategoryandDay.map(function (element) { return element.key});
  var selection = crimeCategories[0];
      console.log(crimeCategories);

//takes the selected crimecategory and gives its object including days and values
      var startCrimeCategory = crimesByCategoryandDay.find(x => x.key == selection);
      console.log(startCrimeCategory);
      console.log(startCrimeCategory.values[0].value);

      var maxStartHeight = 0;
      for (i = 0; i < 7; i++) {
        if (startCrimeCategory.values[i].value > maxStartHeight){
            maxStartHeight = startCrimeCategory.values[i].value;
        }
      }

  var xScale = d3.scaleBand()
    .domain(weekDays)
    .range([0, width]);

  var yScale = d3.scaleLinear()
    .domain([0, maxStartHeight])
    .range([height, 0]);

  var xAxis = d3.axisBottom(xScale).ticks(7);

  var yAxis = d3.axisLeft(yScale);

  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .selectAll("text")
    .style("font-size", "8px")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" );

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

    var updateBars = function(data) {
      console.log(data);
      var maxHeight = 0;
        for (i = 0; i < 7; i++) {
          if (data[i].value > maxHeight){
              maxHeight = data[i].value;
            }}
            console.log(maxHeight);

      yScale.domain([0,maxHeight]);
      yAxis.scale(yScale);

      d3.selectAll("g.y.axis")
           		.transition()
           		.call(yAxis);

      svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr("class", "rectangle")
        .attr('x', (d) => xScale(d.key))
        .attr('y', (d) => yScale(d.value))
        .attr('height', (d) => height - yScale(d.value))
        .attr('width', xScale.bandwidth() - barPadding);

      d3.selectAll('rect')
        .transition()
        .attr("class", "rectangle")
        .attr('y', (d) => yScale(d.value))
        .attr('height', (d) => height - yScale(d.value))
    };

    var selector = d3.select("#drop")
      .append("select")
      .attr("id", "dropdown")
      .on("change", function(d) {
          // selection = document.getElementById("dropdown");
          selection = d3.select('#dropdown option:checked').text();
            console.log(selection);
            var selectedCrimeCategory = crimesByCategoryandDay.find(x => x.key == selection);
            console.log(selectedCrimeCategory);


            updateBars(selectedCrimeCategory.values);
          });

        selector.selectAll("option")
          .data(crimeCategories)
          .enter().append("option")
          .attr("value", function(d) {
            return d;
          })
          .text(function(d){
            return d;
          });

var initialData = startCrimeCategory.values;
updateBars(initialData);

});
