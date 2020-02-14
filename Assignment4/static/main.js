(function () {
    $("#btn").on('click', function () {
        var kval = $("#k").val();
        jQuery.ajax({
            type: "POST",
            url: "ajax/cluster",
            data: {
                'k': kval
            },
            success: function (data) {
                console.log(data);
                d3.select("#scatter > svg").selectAll("*").remove();
                drawClusters(data);

            }
        });
    })
    jQuery.ajax({
        method: "GET",
        url: "/ajax/cluster",
        success: function (data) {
            drawClusters(data);
        }
    })
    drawHist();
    drawSankey();
})()

//dimensions for scatter plot
var width = 500;
var height = 500;
var margin = { left: 60, right: 60, top: 30, bottom: 60 }

var svg1 = d3.select('#scatter')
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom);

function drawClusters(data) {
    var lineg = svg1.append('g')
        .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");
    var dotg = svg1.append('g')
        .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");
    var centerg = svg1.append('g')
        .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");
    //get data

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

    }

    dots = [];
    flag = false;
    for (i = 0; i < data.Attack.length; i++) {
        var dot = {
            x: data.Attack[i],
            y: data.Defense[i],
            name: data.Name[i],
            speed: data.Speed[i],
            group: groups[data.Cluster[i]]
        };
        dots.push(dot);
    }
    console.log(dots);

    //draw 
    var x = d3.scaleLinear()
        .domain([0, d3.max(data.Attack)])
        .range([0, width]);
    var y = d3.scaleLinear()
        .domain([0, d3.max(data.Defense)])
        .range([height, 0]);
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            return "<strong>Name:</strong> <span style='color:red'>" + d.name + "</span><br><strong>Attack:</strong> <span style='color:red'>" + d.x + "</span><br><strong>Defense:</strong> <span style='color:red'>" + d.y + "</span><br><strong>Speed:</strong> <span style='color:red'>" + d.speed + "</span>";
        })
        svg1.append("g")
        .attr("transform", "translate(60," + (height+50)  + ")")
        .call(d3.axisBottom(x))                
        .append("text")
        .attr("fill", "#000")
        .attr("x", width)
        .attr('y', -10)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .text("Attack");

        svg1.append("g")
        .attr("transform", "translate(10"  + ",40)")
        .call(d3.axisRight(y))
        .append("text")
        .attr("fill", "#000")
        .attr("x", 0)
        .attr("y", -5)
        .text("Defense")
        .attr("text-anchor", "start");

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
        .attr('r', 5)
        .on("mouseover", tip.show)
        .on("mouseleave", tip.hide);
    dotg.call(tip);
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

    console.log(data.Speed);
    var lasso_start = function () {
        updateHist(data.Speed);
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

        selected._groups[0].forEach(function (d) {
            selectedArray.push(d3.select(d).data()[0].speed)
        });

        if (selectedArray.length == 0) {
            updateHist(data.Speed);
        } else {
            updateHist(selectedArray);
        }
    };
    //console.log(circles[0]);
    var s = d3.select("#scatter > svg");
    var cir = d3.select("#scatter > svg").selectAll("circle");
    const lasso = d3.lasso()
        .closePathDistance(305)
        .closePathSelect(true)
        .targetArea(svg1)
        .items(circles)
        .on("start", lasso_start)
        .on("draw", lasso_draw)
        .on("end", lasso_end);
    svg1.call(lasso);
}

function updateHist(newdata) {
    var width = 550;
    var height = 550;
    var margin = { left: 60, right: 60, top: 30, bottom: 0 }

    var svg = d3.select("#histogram svg");
    var x = d3.scaleLinear()
        .domain([d3.min(newdata), d3.max(newdata)])     // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
        .range([0, width]);

    // set the parameters for the histogram
    var histogram = d3.histogram()
        //.value(data.x)   // I need to give the vector of value
        .domain(hx.domain())  // then the domain of the graphic
        .thresholds(hx.ticks(40)); // then the numbers of bins

    // And apply this function to data to get the bins
    var bins = histogram(newdata);

    // Y axis: scale and draw:
    var y = d3.scaleLinear()
        .range([height, 0]);
    y.domain([0, d3.max(bins, function (d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
    var colors = d3.scaleLinear()
        .domain([0, d3.max(bins, function (d) { return d.length; })])
        .range([d3.rgb("steelblue").brighter(), d3.rgb("steelblue").darker()]);

    // append the bar rectangles to the svg element
    svg
        .selectAll("rect")
        .data(bins)
        .join("rect")
        .transition()
        .duration(750)
        .attr("x", d => hx(d.x0) + 1)
        .attr("width", d => Math.max(0, hx(d.x1) - hx(d.x0) - 1))
        .attr("y", d => hy(d.length))
        .attr("fill", d => colors(d.length))
        .attr("height", d => hy(0) - hy(d.length));
}
var hx = d3.scaleLinear();
var hy = d3.scaleLinear();

function drawHist() {
    var width = 550;
    var height = 550;
    var margin = { left: 60, right: 60, top: 30, bottom: 0 }

    var svg = d3.select('#histogram')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom);

    jQuery.ajax({
        method: "GET",
        url: "/ajax/histogram",
        success: function (data) {

            // X axis: scale and draw:
            hx
                .domain([d3.min(data.x), d3.max(data.x)])     // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
                .range([0, width]);
            svg.append("g")
                .attr("transform", "translate(0," + height + " )")
                .call(d3.axisBottom(hx))
                .append("text")
                .attr("fill", "#000")
                .attr("x", width + 50)
                .attr('y', margin.bottom)
                .attr("dy", "0.71em")
                .attr("text-anchor", "end")
                .text("Speed");

            // set the parameters for the histogram
            var histogram = d3.histogram()
                //.value(data.x)   // I need to give the vector of value
                .domain(hx.domain())  // then the domain of the graphic
                .thresholds(hx.ticks(40)); // then the numbers of bins

            // And apply this function to data to get the bins
            var bins = histogram(data.x);

            // Y axis: scale and draw:
            hy
                .range([height, 0])
                .domain([0, d3.max(bins, function (d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
            svg.append("g")
                .attr("transform", "translate(" + width + ",0)")
                .call(d3.axisRight(hy));

            var colors = d3.scaleLinear()
                .domain([0, d3.max(bins, function (d) { return d.length; })])
                .range([d3.rgb("steelblue").brighter(), d3.rgb("steelblue").darker()]);

            var tip = d3.tip()
                .attr('class', 'd3-tip')
                .offset([-10, 0])
                .html(function (d) {
                    return "<strong>Total:</strong> <span style='color:red'>" + d.length + "</span>";
                })
            svg.call(tip);
            // append the bar rectangles to the svg element
            var bar = svg.append("g")
                .selectAll("rect")
                .data(bins)
                .join("rect")
                .attr("class", "rect")
                .attr("fill", d => colors(d.length))
                .attr("x", d => hx(d.x0) + 1)
                .attr("width", d => Math.max(0, hx(d.x1) - hx(d.x0) - 1))
                .attr("y", d => hy(d.length))
                .attr("height", d => hy(0) - hy(d.length))
                .on('mouseover', tip.show)
                .on('mouseout', tip.hide);

            bar.append("text")
                .data(bins)
                .attr("dy", ".75em")
                .attr("y", 300)
                .attr("x", d => Math.max(0, hx(d.x1) - hx(d.x0) - 1))
                .attr("text-anchor", "middle")
                .text(function (d) { return "d.length"; });
        }
    })
}

function drawSankey() {
    var margin = { left: 60, right: 60, top: 20, bottom: 30 }

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
                .text(function (d) { return d.id + ":" + d.value; })
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
