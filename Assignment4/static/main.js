(function () {
    $("#btn").on('click', function () {
        var kval = $("#k").val();
        jQuery.ajax({
            type: "POST",
            url: "ajax/cluster",
            data: {
                'k': kval
            },
            success: function (result) {
                console.log(result);
                // alert(result);
            }
        });
    })
    drawClusters();
    drawHist();
    drawSankey();
})()
function submit() {
    $('#sendk').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: 'ajax/cluster',
            type: 'post',
            data: $('#k').val(),
            success: function (data) {
                console.log(data);
                //whatever you wanna do after the form is successfully submitted
            }
        });
    });
}
function drawClusters() {
    var width = 500;
    var height = 500;
    var margin = { left: 60, right: 60, top: 30, bottom: 0 }

    var svg = d3.select('#scatter')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);
    var lineg = svg.append('g')
        .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");
    var dotg = svg.append('g')
        .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");
    var centerg = svg.append('g')
        .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");
    //get data
    jQuery.ajax({
        method: "GET",
        url: "/ajax/cluster",
        success: function (data) {
            //alert("Success");
            console.log(data);

            K = data.K;
            groups = [];
            for (var i = 0; i < K; i++) {
                var attack = [], defense = [];
                for (j = 0; j < data.Attack.length; j++) {
                    if (data.Cluster[j] === i) {
                        attack.push(data.Attack[j]);
                        defense.push(data.Defense[j]);
                    }
                }
                //console.log(a);
                attack.sort((a, b) => a - b);
                defense.sort((a, b) => a - b);

                var g = {
                    dots: [],
                    color: 'hsl(' + (i * 360 / K) + ',100%,50%)',
                    center: {
                        x: attack[Math.floor(attack.length / 2)],
                        y: defense[Math.floor(defense.length / 2)]
                    },
                    init: {
                        center: {}
                    }
                };
                g.init.center = {
                    x: g.center.x,
                    y: g.center.y
                };
                groups.push(g);
                console.log(g.center.x + " " + g.center.y);
            }

            dots = [];
            flag = false;
            for (i = 0; i < data.Attack.length; i++) {
                var dot = {
                    x: data.Attack[i],
                    y: data.Defense[i],
                    speed: data.Speed[i],
                    group: groups[data.Cluster[i]]
                };
                dots.push(dot);
            }
            console.log(dots);

            //draw 
            var x = d3.scaleLinear()
                .domain([0, d3.max(data.Attack)])
                .range([height, 0]);
            var y = d3.scaleLinear()
                .domain([0, d3.max(data.Defense)])
                .range([height, 0]);
            var circles = dotg.selectAll('circle')
                .data(dots)
                .enter()
                .append('circle')
                .attr('cx', function (d) { return x(d.x); })
                .attr('cy', function (d) { return y(d.y); })
                .attr('data-x', d => d.x)
                .attr('data-y', d => d.y)
                .attr('data-speed', d => d.speed)
                .attr('class', 'circle')
                .attr('fill', function (d) { return d.group.color; })
                .attr('opacity', 0.5)
                .attr('r', 5);
            console.log(circles);

            if (dots[0].group) {
                var l = lineg.selectAll('line')
                    .data(dots);
                var updateLine = function (lines) {
                    lines
                        .attr('x1', function (d) { return x(d.x); })
                        .attr('y1', function (d) { return y(d.y); })
                        .attr('x2', function (d) { return x(d.group.center.x); })
                        .attr('y2', function (d) { return y(d.group.center.y); })
                        .attr('stroke', function (d) { return d.group.color; });
                };
                updateLine(l.enter().append('line'));
                updateLine(l.transition().duration(500));
                l.exit().remove();
            } else {
                lineg.selectAll('line').remove();
            }

            var c = centerg.selectAll('path')
                .data(groups);
            var updateCenters = function (centers) {
                centers
                    .attr('transform', function (d) { return "translate(" + x(d.center.x) + "," + y(d.center.y) + ") rotate(45)"; })
                    .attr('fill', function (d, i) { return d.color; })
                    .attr('stroke', '#aabbcc');
            };
            c.exit().remove();
            updateCenters(c.enter()
                .append('path')
                .attr('d', d3.symbol().type(d3.symbolCross))
                .attr('stroke', '#aabbcc'));
            updateCenters(c
                .transition()
                .duration(500));

            var lasso_start = function () {
                console.log('start')
                lasso.items()
                    .attr("r", 5)
                    .classed("not_possible", true)
                    .classed("selected", false);
            };

            var lasso_draw = function () {
                console.log('draw')
                lasso.possibleItems()
                    .classed("not_possible", false)
                    .classed("possible", true);
                lasso.notPossibleItems()
                    .classed("not_possible", true)
                    .classed("possible", false);
            };

            var lasso_end = function () {
                console.log('end')
                lasso.items()
                    .classed("not_possible", false)
                    .classed("possible", false);
                lasso.selectedItems()
                    .classed("selected", true)
                    //.attr('fill', 'orange')
                    .attr("r", 8);
                lasso.notSelectedItems()
                    //.attr('fill', d => d.group.color)
                    .attr("r", 5);

                var selectedArray = [];
                var selected = lasso.selectedItems();
                console.log(selected);
                selected._groups[0].forEach(function (d) {
                    selectedArray.push(d3.select(d).data()[0].speed)
                });
                console.log(selectedArray);
                updateHist(selectedArray);
            };
            console.log(circles[0]);
            var s = d3.select("#scatter > svg");
            var cir = d3.select("#scatter > svg").selectAll("circle");
            const lasso = d3.lasso()
                .closePathDistance(305)
                .closePathSelect(true)
                .targetArea(svg)
                .items(circles)
                .on("start", lasso_start)
                .on("draw", lasso_draw)
                .on("end", lasso_end);
            svg.call(lasso);


        }
    })
}

function updateHist(newdata) {
    var width = 500;
    var height = 500;
    var margin = { left: 60, right: 60, top: 30, bottom: 0 }

    /* Note that here we only have to select the elements - no more appending! */
    /*plot.selectAll("rect")
        .data(newdata)
        .transition()
        .duration(750)
        .attr("x", function (d, i) {
            return xScale(i);
        })
        .attr("width", width / currentDatasetBarChart.length - barPadding)
        .attr("y", function (d) {
            return yScale(d.measure);
        })
        .attr("height", function (d) {
            return height - yScale(d.measure);
        })
        .attr("fill", colorChosen)
        ;
*/
var svg = d3.select("#histogram svg");
        var x = d3.scaleLinear()
        .domain([d3.min(newdata), d3.max(newdata)])     // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
        .range([0, width]);

    // set the parameters for the histogram
    var histogram = d3.histogram()
        //.value(data.x)   // I need to give the vector of value
        .domain(x.domain())  // then the domain of the graphic
        .thresholds(x.ticks(40)); // then the numbers of bins

    // And apply this function to data to get the bins
    var bins = histogram(newdata);
    console.log(bins);
    // Y axis: scale and draw:
    var y = d3.scaleLinear()
        .range([height, 0]);
    y.domain([0, d3.max(bins, function (d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously

    // append the bar rectangles to the svg element
    svg
        .selectAll("rect")
        .data(bins)
        .join("rect")
        .transition()
        .duration(750)
        .attr("x", d => x(d.x0) + 1)
        .attr("width", d => Math.max(0, x(d.x1) - x(d.x0) - 1))
        .attr("y", d => y(d.length))
        .attr("fill", "orange")
        .attr("height", d => y(0) - y(d.length));
}


function drawHist() {
    var width = 500;
    var height = 500;
    var margin = { left: 60, right: 60, top: 30, bottom: 0 }

    var svg = d3.select('#histogram')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);
    jQuery.ajax({
        method: "GET",
        url: "/ajax/histogram",
        success: function (data) {
            console.log(data.x);
            // X axis: scale and draw:
            var x = d3.scaleLinear()
                .domain([d3.min(data.x), d3.max(data.x)])     // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
                .range([0, width]);
            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            // set the parameters for the histogram
            var histogram = d3.histogram()
                //.value(data.x)   // I need to give the vector of value
                .domain(x.domain())  // then the domain of the graphic
                .thresholds(x.ticks(40)); // then the numbers of bins

            // And apply this function to data to get the bins
            var bins = histogram(data.x);
            console.log(bins);
            // Y axis: scale and draw:
            var y = d3.scaleLinear()
                .range([height, 0]);
            y.domain([0, d3.max(bins, function (d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
            svg.append("g")
            //.attr("transform", "translate(" + margin.left + ",0)")
                .call(d3.axisLeft(y));

            // append the bar rectangles to the svg element
            svg.append("g")
                .attr("fill", "orange")
                .selectAll("rect")
                .data(bins)
                .join("rect")
                .attr("x", d => x(d.x0) + 1)
                .attr("width", d => Math.max(0, x(d.x1) - x(d.x0) - 1))
                .attr("y", d => y(d.length))
                .attr("height", d => y(0) - y(d.length));
        }
    })
}

function drawSankey() {
    var margin = { left: 60, right: 60, top: 20, bottom: 10 }

    var width = 1200 - margin.left - margin.right;
    var height = 800 - margin.top - margin.bottom;

    var svg = d3.select('#sankey')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    jQuery.ajax({
        method: "GET",
        url: "/ajax/sankey",
        success: function (data) {
            //alert(data);
            ids = [];
            for (i = 0; i < data.nodes.length; i++) {
                ids.push(data.nodes[i].id);
            }

            // Constructs a new Sankey generator with the default settings.
            //data.links[0].target = "Fire";
            console.log(data);
            color.domain(ids);
            var nodeMap = {};
            data.nodes.forEach(function (x) { nodeMap[x.id] = x; });
            data.links = data.links.map(function (x) {
                return {
                    source: nodeMap[x.source],
                    target: nodeMap[x.target],
                    value: x.value
                };
            });
            var sankey = d3.sankey()
                .nodeWidth(36)
                .nodePadding(10)
                .size([width, height]);
            sankey
                .nodes(data.nodes)
                .links(data.links)
                .layout(32);

            // add in the links
            var link = svg.append("g").selectAll(".link")
                .data(data.links)
                .enter().append("path")
                .attr("class", "link")
                .attr("d", sankey.link())
                .style("stroke-width", function (d) { return Math.max(1, d.dy); })
                .sort(function (a, b) { return b.dy - a.dy; });

            // add in the nodes
            var node = svg.append("g")
                .selectAll(".node")
                .data(data.nodes)
                .enter().append("g")
                .attr("class", "node")
                .attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; })
                .call(d3.drag()
                    .subject(function (d) { return d; })
                    .on("start", function () { this.parentNode.appendChild(this); })
                    .on("drag", dragmove));

            // add the rectangles for the nodes
            node
                .append("rect")
                .attr("height", function (d) { return d.dy; })
                .attr("width", sankey.nodeWidth())
                .style("fill", function (d) { return d.color = color(d.id); })
                .style("stroke", function (d) { return d3.rgb(d.color).darker(2); })
                // Add hover text
                .append("title")
                .text(function (d) { return d.id; });
            // add in the title for the nodes
            node.append("text")
                .attr("x", -6)
                .attr("y", function (d) { return d.dy / 2; })
                .attr("dy", ".35em")
                .attr("text-anchor", "end")
                .attr("transform", null)
                .text(function (d) { return d.id; })
                .filter(function (d) { return d.x < width / 2; })
                .attr("x", 6 + sankey.nodeWidth())
                .attr("text-anchor", "start");
            // the function for moving the nodes
            function dragmove(d) {
                d3.select(this).attr("transform",
                    "translate(" + (
                        d.x = Math.max(0, Math.min(width - d.dx, d3.event.x))
                    ) + "," + (
                        d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))
                    ) + ")");
                sankey.relayout();
                link.attr("d", sankey.link());
            }
        }

    })
}
function getClusterData() {
    jQuery.ajax({
        method: "GET",
        url: "/ajax/cluster",
        success: function (data) {
            alert("Success");
            console.log(data);
        }
    })
};

function getSankeyData() {
    jQuery.ajax({
        method: "GET",
        url: "/ajax/sankey",
        success: function (data) {
            alert("Success");
            console.log(data);
        }
    })
};

function getHistData() {
    jQuery.ajax({
        method: "GET",
        url: "/ajax/histogram",
        success: function (data) {
            alert("Success");
            console.log(data);
        }
    })
};