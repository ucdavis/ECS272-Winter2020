

window.onload = function() { // calls this on loading index.html
    $.get("loadData", function(data){ //first api call
      //origData = JSON.parse(data);
      data= JSON.parse(data);
      console.log(data);
      var result = {"name": "parent", "children": data};
    
      createVisualization(result);
    });
}
// Main function to draw and set up the visualization, once we have the data.
function createVisualization(nodeData) {
    // var nodeData = {
    //     "name": "TOPICS", "children": [{
    //         "name": "Topic A",
    //         "children": [{"name": "Sub A1", "value": 4}, {"name": "Sub A2", "value": 4}]
    //     }, {
    //         "name": "Topic B",
    //         "children": [{"name": "Sub B1", "value": 3}, {"name": "Sub B2", "value": 3}, {
    //             "name": "Sub B3", "value": 3}]
    //     }, {
    //         "name": "Topic C",
    //         "children": [{"name": "Sub A1", "value": 4}, {"name": "Sub A2", "value": 4}]
    //     }]
    // };
    console.log(nodeData);
    var width = 1500;
    var height = 1500;
    var radius = Math.min(width, height) / 2;

    const dark = [
        '#B08B12',
        '#BA5F06',
        '#8C3B00',
        '#6D191B',
        '#842854',
        '#5F7186',
        '#193556',
        '#137B80',
        '#144847',
        '#254E00'
      ];
      
      const mid = [
        '#E3BA22',
        '#E58429',
        '#BD2D28',
        '#D15A86',
        '#8E6C8A',
        '#6B99A1',
        '#42A5B3',
        '#0F8C79',
        '#6BBBA1',
        '#5C8100'
      ];
      
      const light = [
        '#F2DA57',
        '#F6B656',
        '#E25A42',
        '#DCBDCF',
        '#B396AD',
        '#B0CBDB',
        '#33B6D0',
        '#7ABFCC',
        '#C8D7A1',
        '#A0B700'
      ];
      
      const palettes = [light, mid, dark];
      const lightGreenFirstPalette = palettes
        .map(d => d.reverse())
        .reduce((a, b) => a.concat(b));
      
      
    var colors = d3.scale.ordinal().range(lightGreenFirstPalette)
//     var x = d3.scalelinear()
//     .range([0, 2 * Math.PI]);

// var y = d3.scale.sqrt()
//     .range([0, radius]);
    console.log(nodeData);
    // Create primary <g> element
    // var g = d3.select('svg')
    //     .attr('width', width)
    //     .attr('height', height)
    //     .append('g')
    //     .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');
    var vis = d3.select("#chart").append("svg:svg")
    .attr("width", width)
    .attr("height", height)
    .append("svg:g")
    .attr("id", "container")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
      
    // Data strucure
    var partition = d3.layout.partition()
    .size([2 * Math.PI, (radius * radius) +50])
    .value(function(d) { return d.value; });
    var inner = {1:500, 2:535, 3:570, 4:605, 5:640, 6:675, 7:710, 8:745};
    var outer = {1:530, 2:565, 3:600, 4:635, 5:670, 6:705, 7:740, 8:775};
    
    var arc = d3.svg.arc()
    .startAngle(function(d) { return d.x; })
    .endAngle(function(d) { return d.x + d.dx; })
    .innerRadius(function(d) { return inner[d.depth];})
    .outerRadius(function(d) { return outer[d.depth] });

    var nodes = partition.nodes(nodeData)
    .filter(function(d) {
    return (d.dx > 0.005); // 0.005 radians = 0.29 degrees
    });
    nodes = nodes.filter(function(d) {
        return (d.name != "NA" && d.name.length > 0); // BJF: Do not show the "end" markings.
        });
        var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

        var path = vis.data([nodeData]).selectAll("path")
        .data(nodes)
        .enter().append("svg:path")
        .attr("display", function(d) { return d.depth ? null : "none"; })
        .attr("d", arc)
        .attr("fill-rule", "evenodd")
        .style("fill", function(d, i) { console.log(colors(d.name));return colors(d.name); })
        .style("opacity", 1)
        .on("mouseover", function(d) {
            div.transition()
                .duration(200)
                .style("opacity", .9);
            div	.html("<p style='padding-top:10%;'><b>"+d.name+"</b></p>")
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
            })
        .on("mouseout", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
            });
            // nodeLabel = nodes.filter(function(d) {
            //     return (d.name != "NA" && d.name.length > 0); // BJF: Do not show the "end" markings.
            //     });
//     vis.selectAll('.label').data(nodes).enter().append('text')
//         .attr('x', d => arc.centroid(d)[0])
//         .attr('y', d => arc.centroid(d)[1])
//         .attr("transform", function(d) { return "rotate(" + getAngle(d) + ")"})
//         .attr('text-anchor', 'middle')
//   .text(d => d.name)
//         totalSize = path.node().__data__.value;
//         function getAngle(d) {
//             // Offset the angle by 90 deg since the '0' degree axis for arc is Y axis, while
//             // for text it is the X axis.
//             var thetaDeg = (180 / Math.PI * (arc.startAngle()(d) + arc.endAngle()(d)) / 2 - 90);
//             // If we are rotating the text by more than 90 deg, then "flip" it.
//             // This is why "text-anchor", "middle" is important, otherwise, this "flip" would
//             // a little harder.
//             return (thetaDeg > 90) ? thetaDeg - 180 : thetaDeg;
        //}

  }

 