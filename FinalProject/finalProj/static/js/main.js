

window.onload = function () { // calls this on loading index.html
    $.get("loadData", function (data) { //first api call
        //origData = JSON.parse(data);
        data = JSON.parse(data);
        console.log(data);
        var result = { "name": "parent", "children": data };

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
        .size([2 * Math.PI, (radius * radius) + 50])
        .value(function (d) { return d.value; });
    var inner = { 1: 500, 2: 535, 3: 570, 4: 605, 5: 640, 6: 675, 7: 710, 8: 745 };
    var outer = { 1: 530, 2: 565, 3: 600, 4: 635, 5: 670, 6: 705, 7: 740, 8: 775 };

    var arc = d3.svg.arc()
        .startAngle(function (d) { return d.x; })
        .endAngle(function (d) { return d.x + d.dx; })
        .innerRadius(function (d) { return inner[d.depth]; })
        .outerRadius(function (d) { return outer[d.depth] });
        console.log("hmmm"); console.log(partition.nodes(nodeData).filter(function (d) {
            return (d.value > 0); // 0.005 radians = 0.29 degrees
        }));
    var nodes = partition.nodes(nodeData)
        .filter(function (d) {
            return (d.dx > 0.005); // 0.005 radians = 0.29 degrees
        });
    nodes = nodes.filter(function (d) {
        return (d.name != "NA" && d.name.length > 0); // BJF: Do not show the "end" markings.
    });
    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    var path = vis.data([nodeData]).selectAll("path")
        .data(nodes)
        .enter().append("svg:path")
        .attr("display", function (d) { return d.depth ? null : "none"; })
        .attr("d", arc)
        .attr("fill-rule", "evenodd")
        .style("fill", '#808080')//function(d, i) { console.log(colors(d.name));return colors(d.name); })
        .style("opacity", 1)
        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .on("click", click);


    function mouseout(d) {
        if (!activeClick) {
            $('#breadcrumbs').html('');
            d3.selectAll("path")
                .style("opacity", 1)
                .transition()
                .duration(1500);
        }
    }
var activeClick = false;

    function click(d) {
        if (d.selected == undefined || d.selected == null || d.selected == false) {
            d.selected = true;
            activeClick = true;
            sequenceArray = getAncestors(d);
            console.log(sequenceArray);
            crumbStr = '';
            for (let node in sequenceArray) {
                if (sequenceArray[node]['name'].length > 0) {
                    crumbStr += sequenceArray[node]['name'];
                    if (node < sequenceArray.length - 1) {
                        crumbStr += '->';
                    }
                }
                
            }
            $('#breadcrumbs').html(crumbStr);
            // Fade all the segments.
            d3.selectAll("path")
                .style("opacity", 0.3)
                .transition()
                .duration(500);

            // Then highlight only those that are an ancestor of the current segment.
            vis.selectAll("path")
                .filter(function (node) {
                    return (sequenceArray.indexOf(node) >= 0);
                })
                .style("opacity", 1)
                .transition()
                .duration(500);
        } else {
            activeClick = false;
            d.selected = false;
            mouseout(d);
        }
    }

    function mouseover(d) {
        if (!activeClick) {
            sequenceArray = getAncestors(d);
            crumbStr = '';
            for (let node in sequenceArray) {
                console.log(sequenceArray[node]['name'].length);
                if (sequenceArray[node]['name'].length != 0) {
                    crumbStr += sequenceArray[node]['name'];
                    if (node < sequenceArray.length - 1) {
                        crumbStr += '->';
                    }
                }
                
            }
            $('#breadcrumbs').html(crumbStr);
            // Fade all the segments.
            d3.selectAll("path")
                .style("opacity", 0.3)
                .transition()
                .duration(500);

            // Then highlight only those that are an ancestor of the current segment.
            vis.selectAll("path")
                .filter(function (node) {
                    return (sequenceArray.indexOf(node) >= 0);
                })
                .style("opacity", 1)
                .transition()
                .duration(500);

                vis.selectAll("path")
                .filter(function (node) {
                    return (sequenceArray.indexOf(node)  ==  sequenceArray.length - 1);
                })
                .style("opacity", 1)
                .transition()
                .duration(500);
        }
    }
    // Given a node in a partition layout, return an array of all of its ancestor
    // nodes, highest first, but excluding the root.
    function getAncestors(node) {
        var path = [];
        var current = node;
        while (current.parent) {
            path.unshift(current);
            current = current.parent;
        }
        return path;
    }

}

