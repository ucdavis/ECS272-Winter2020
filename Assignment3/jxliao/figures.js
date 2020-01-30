// set the dimensions and margins of the graph
var margin = {top: 30, right: 100, bottom: 50, left: 100},
    width = 1000 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;


// append the svg object to the body of the page
var svg = d3.select("#vis-barplot")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");


function checkLabel (label) {
    	arr = label.split(" ");
    	if (arr.length == 4) {
    		return arr[2] + " " +arr[3];
    	}  else {
    		return label;
    	}
    }

d3.csv('LAX_Terminal_Passengers.csv').then(function(data){

    data.forEach(function(d) {
    	d.Passenger_Count = +d.Passenger_Count;
  	});

	var PassengerCountsum_AD = d3.nest()
		  .key(function(d) {return d.Terminal; })
  		.key(function(d) { return d.Arrival_Departure; })
  		.rollup(function(v) { return d3.sum(v, function(d){return d.Passenger_Count}); })
  		.entries(data)
  		.map(function(group){
  			return {
  				Terminal: checkLabel(group.key),
  				Passenger_Count_Arrival: group.values[0].value,
  				Passenger_Count_Departure: group.values[1].value
  			}
  		});

  	console.log(JSON.stringify(PassengerCountsum_AD));

  var allGroup = ["Passenger_Count_Arrival", "Passenger_Count_Departure"]
	var Terminals = ["Imperial Terminal","Misc. Terminal","Terminal 1","Terminal 2","Terminal 3","Terminal 4","Terminal 5","Terminal 6","Terminal 7","Terminal 8","International Terminal"]

    // add the options to the button
	d3.select("#selectButton")
      .selectAll('myOptions')
     	.data(allGroup)
      .enter()
    	.append('option')
      .text(function (d) { return d; }) // text showed in the menu
      .attr("value", function (d) { return d; }) // corresponding value returned by the button

    var myColor = d3.scaleOrdinal()
      .domain(allGroup)
      .range(d3.schemeSet2);


    var x = d3.scaleBand()
          .range([0, width])
          .domain(Terminals)
          .padding(0.1);

    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));
      //.call(_config.xAxisGen)
      //    .selectAll('.x .tick text') // select all the x tick texts
      //    .call(function(t){                
      //      t.each(function(d){ // for each one
      //        var self = d3.select(this);
      //        var s = self.text().split(' ');  // get the text and split it
      //        self.text(''); // clear it out
      //        self.append("tspan") // insert two tspans
      //          .attr("x", 0)
       //         .attr("dy",".8em")
       //         .text(s[0]);
       //       self.append("tspan")
       //         .attr("x", 0)
       //         .attr("dy",".8em")
       //         .text(s[1]);
        //    })
       // });



    // Make y scale, the domain will be defined on bar update
	var y = d3.scaleLinear()
			.domain([0, 80000000])
       		.range([height, 0]);
    svg.append("g")
  		.call(d3.axisLeft(y));

  svg.append("text")             
      .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.top + 10) + ")")
      .style("text-anchor", "middle")
      .text("Terminal");

  svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Passenger_Count");



  // append the rectangles for the bar chart
  	var bar = svg.selectAll("rect")
      		.data(PassengerCountsum_AD)
    		.enter().append("rect")
      				.attr("class", "bar")
      				.attr("x", function(d) { return x(d.Terminal); })
      				.attr("width", x.bandwidth())
      				.attr("y", function(d) { return y(d.Passenger_Count_Arrival); })
      				.attr("height", function(d) { return height - y(d.Passenger_Count_Arrival); })
      				.attr("fill", function(d){ return myColor("Arrival") });

    // A function that update the chart
    function update(selectedGroup) {

      // Create new data with the selection?
      var dataFilter = PassengerCountsum_AD.map(function(d){return {Terminal: d.Terminal, value:d[selectedGroup]} })

      // Give these new data to update line
      	bar
          .data(dataFilter)
          .transition()
          .duration(1000)
          .attr("x", function(d) { return x(d.Terminal); })
          .attr("y", function(d) { return y(d.value); })
          .attr("height", function(d) { return height - y(d.value); })
          .attr("fill", function(d){ return myColor(selectedGroup) })
    }

    // When the button is changed, run the updateChart function
    d3.select("#selectButton").on("change", function(d) {
        // recover the option that has been chosen
        var selectedOption = d3.select(this).property("value")
        // run the updateChart function with this selected option
        update(selectedOption)
    })




})



