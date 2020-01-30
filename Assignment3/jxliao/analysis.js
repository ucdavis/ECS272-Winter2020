d3.csv("Traffic.csv").then( function(data) {
	data.forEach(function(d) {
    	d.Passenger_Count = +d.Passenger_Count;
  		});

    console.log(data[0]);

    var maxLand = d3.max(data, function(d) { return d.Passenger_Count; });
	console.log(maxLand);

	var PassengerCountsum_AD = d3.nest()
		.key(function(d) {return d.Terminal; })
  		.key(function(d) { return d.Arrival_Departure; })
  		.rollup(function(v) { return d3.sum(v, function(d){return d.Passenger_Count}); })
  		.entries(data)
  		.map(function(group){
  			return {
  				Terminal: group.key,
  				Passenger_Count_Arrival: group.values[0].value,
  				Passenger_Count_Departure: group.values[1].value
  			}
  		});

  		

  	

  	var flat_PassengerCountsum_AD = []

    });

