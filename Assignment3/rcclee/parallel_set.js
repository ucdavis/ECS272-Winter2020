var chart = d3.parsets()
      .dimensions(["Terminal", "Domestic_International", "Arrival_Departure"])
      .value(function(d) {
        return d.Passenger_Count;
      });

var vis = d3.select("div#div1").append("svg")
    .attr("width", chart.width())
    .attr("height", chart.height());


var dataset = d3.csv("../datasets/LAX_Terminal_Passengers.csv", function(error, csv) {
  vis.datum(csv).call(chart);
});

d3.keys(dataset[0]).filter(function(key){ return key == "Terminal" || key == "Arrival_Departure" || key == "Domestic_International" || key == "Passenger_Count"})

