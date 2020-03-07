  //parameter
  var width = 1300,
      height = 450;

  //set svg window
  var svg = d3.select("#container").append("svg")
    .attr("width", width)
    .attr("height", height);

  //projection
  var projection = d3.geo.equirectangular()
    	.scale(8000)
    	.translate([width / 2, height / 2])
	.rotate([84.5,-37.8]);

  var projection1 = d3.geo.equirectangular()
    	.scale(8000)
    	.translate([width / 2, height / 2])
	.rotate([84.7,-37.6]);

  //load map
  d3.json("data/ky.json", function(error, topology) {
	if (error) throw error;
	
	console.log("topojson", topology)
	var geojson = topojson.feature(topology, topology.objects.cb_2015_kentucky_county_20m);
	console.log("geojson", geojson)

	//path
  	var path = d3.geo.path()
		.projection(projection);

	// draw the map
	svg.selectAll("path")
		.data(geojson.features)
		.enter()
		.append("path")
		.attr("d", path);
  });

	  // With Hex code
	  svg.append("circle").attr("cx",150).attr("cy",20).attr("r",4)
  	  .style("fill", "#69b3a2");

	  // With Hex code
	  svg.append("circle").attr("cx",150).attr("cy",40).attr("r",9)
  	  .style("fill", "steelblue" );

	  // With RGBA (last number is the opacity)
	  svg.append("circle").attr("cx",150).attr("cy",70).attr("r",14)
  	  .style("fill", "rgba(198, 45, 205, 0.8)" )


	  //Mapping indication
	  svg.append("text")
	     .attr("x", 170)
	     .attr("y", 25)
	     .text("A");

	  svg.append("text")
	     .attr("x", 170)
	     .attr("y", 45)
	     .text("B");

	  svg.append("text")
	     .attr("x", 170)
	     .attr("y", 75)
	     .text("C");

  //load fooddata
  d3.csv("data/FoodService.csv", function(error, foodData) {
	if (error) throw error;
	
	console.log(foodData)

	//draw food circle
	svg.selectAll(".food-circle")
	  .data(foodData)
	  .enter().append("circle")
	  .attr("class", "circles")
	  .attr("r", function(d) {
		var size = d.Grade.charCodeAt();
		if (size)
		{
			size=(size-65)*5+4;
			return size;
		}
	  	else
		return 0;
	  })
	  .attr("cx", function(d) {
		var coords = projection([d.Longitude, d.Latitude])
	  	return coords[0];
	  })
	  .attr("cy", function(d) {
		var coords = projection([d.Longitude, d.Latitude])
	  	return coords[1];
	  })
	  .style("fill", function(d) {
	  	if (d.Grade.charCodeAt() == 65)
			return "#69b3a2";
		if (d.Grade.charCodeAt() == 66)
			return "steelblue";
		if (d.Grade.charCodeAt() == 67)
			return "rgba(198, 45, 205, 0.8)";
	  });

  });

  //dropdown menu interation
  function change(control) {
    var value = control.value;
    console.log(value);
    var test, color;
    if (value == "A") {
	test = 4;
	color = "#69b3a2";
    }
    if (value == "B") {
	test = 9;
	color = "steelblue";
    }
    if (value == "C") {
	test = 14;
	color = "rgba(198, 45, 205, 0.8)";
    }
    d3.selectAll(".circles")
      .style("fill", function() {
	if (value == "ALL" && d3.select(this).attr("r") == 4)
	   return "#69b3a2";
	if (value == "ALL" && d3.select(this).attr("r") == 9)
	   return "steelblue";
	if (value == "ALL" && d3.select(this).attr("r") == 14)
	   return "rgba(198, 45, 205, 0.8)";
	if (d3.select(this).attr("r") != test)
	  return "#ccc";
	else return color;
	})
 }

  // parallel chart
  d3.csv('data/FoodService2.csv', function(data) {
    var colors = d3.scale.ordinal()
    .range(["#a6cee3","#1f78b4","#b2df8a","#33a02c",
            "#fb9a99","#e31a1c","#fdbf6f","#ff7f00",
            "#cab2d6","#6a3d9a","#ffff99","#b15928"]);

    var color = function(d) { return colors(d.TypeDescription
); };

    var parcoords = d3.parcoords()("#example")
    .data(data)
    .showControlPoints(false)
    .color(color)
    .alpha(0.25)
    .composite("darken")
    .margin({ top: 24, left: 150, bottom: 12, right: 0 })
    .mode("queue")
    .render()
    .reorderable()
    .interactive()
    .brushMode("1D-axes");  // enable brushing

    parcoords.svg.selectAll("text")
      .style("font", "10px sans-serif");

    // opacity
	d3.select("#opacity").on("change", function() {
		d3.select("#opac").text(this.value);
		parcoords.alpha(this.value).render();
	});
s
    //brightness
	d3.select("#brightness").on("click", function() {
		var mode = this.value;
		console.log(mosde);
		if (mode == "darken") {
			this.value = "lighten";
			parcoords.composite("darken");
		}
		else {
			this.value = "darken";
			parcoords.composite("lighten");
		}
	});
   });
  
