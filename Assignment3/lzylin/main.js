(function () {
    // first, load the dataset from a CSV file
    d3.csv('./Los_Angeles_International_Airport_-_Passenger_Traffic_By_Terminal.csv', function (error, data) {
        // console.log(data)
        function segColor(c) { return { Arrival: "#807dba", Departure: "#e08214" }[c]; }
        var barData = data.map(function (d) {
            return {
                Terminal: d.Terminal,
                Arrival_Departure: d.Arrival_Departure,
                Passenger_Count: d.Passenger_Count
            }
        });
        barData = barData.filter(function (row) {
            return row['Terminal'] == "Terminal 1" || row['Terminal'] == "Terminal 2" || row['Terminal'] == "Terminal 3" || row['Terminal'] == "Terminal 4" || row['Terminal'] == "Terminal 5" || row['Terminal'] == "Terminal 6" || row['Terminal'] == "Terminal 7" || row['Terminal'] == "Terminal 8" || row['Terminal'] == "Tom Bradley International Terminal";
        })
        var barDataNested = d3.nest()
            .key(function (d) { return d.Terminal; })
            .key(function (d) { return d.Arrival_Departure; })
            .rollup(function (v) {
                return {
                    total_passenger: d3.sum(v, function (d) { return d.Passenger_Count; })
                };
            })
            .entries(barData);
        console.log(barDataNested)
        var flatBarData = [];
        barDataNested.forEach(function (d) {
            ar = 0
            de = 0
            d.values.forEach(function (f) {
                console.log(f.values)
                if (f.key == "Arrival") {
                    ar = f.values['total_passenger'];
                }
                else {
                    de = f.values['total_passenger'];
                }
            })
            flatBarData.push({
                Terminal: d.key,
                freq: { 'Arrival': ar, 'Departure': de }
            });
        });

        console.log(flatBarData)
        var barColor = 'steelblue';
        // computer total for each terminal
        flatBarData.forEach(function (d) {
            d.total = d.freq.Arrival + d.freq.Departure;
            // console.log(d.total);
        });
        function histoGram(id, fD) {
            var hG = {}, hGDim = { t: 20, r: 100, b: 180, l: 100 };
            hGDim.w = 500 - hGDim.l - hGDim.r,
                hGDim.h = 400 - hGDim.t - hGDim.b;

            //create svg for histogram.
            var hGsvg = d3.select(id).append("svg")
                .attr("width", hGDim.w + hGDim.l + hGDim.r)
                .attr("height", hGDim.h + hGDim.t + hGDim.b).append("g")
                .attr("transform", "translate(" + hGDim.l + "," + hGDim.t + ")");

            // create function for x-axis mapping.
            var x = d3.scale.ordinal().rangeRoundBands([0, hGDim.w], 0.1)
                .domain(fD.map(function (d) { return d[0]; }));

            // Add x-axis to the histogram svg.
            hGsvg.append("g").attr("class", "x axis")
                .attr("transform", "translate(0," + hGDim.h + ")")
                .call(d3.svg.axis().scale(x).orient("bottom"))
                .selectAll("text")
                .attr("y", 0)
                .attr("x", 9)
                .attr("dy", ".35em")
                .attr("transform", "translate(-30,60)rotate(-40)")
                .style("text-anchor", "start");
            // Create function for y-axis map.
            var y = d3.scale.linear().range([hGDim.h, 0])
                .domain([0, d3.max(fD, function (d) { return d[1]; })]);

            // Create bars for histogram to contain rectangles and freq labels.
            var bars = hGsvg.selectAll(".bar").data(fD).enter()
                .append("g").attr("class", "bar");

            //create the rectangles.
            bars.append("rect")
                .attr("x", function (d) { return x(d[0]); })
                .attr("y", function (d) { return y(d[1]); })
                .attr("width", x.rangeBand())
                .attr("height", function (d) { return hGDim.h - y(d[1]); })
                .attr('fill', barColor)
                .on("mouseover", mouseover)// mouseover is defined below.
                .on("mouseout", mouseout);// mouseout is defined below.

            //Create the frequency labels above the rectangles.
            bars.append("text").text(function (d) { return d3.format(",")(d[1]) })
                .attr("x", function (d) { return x(d[0]) + x.rangeBand() / 2; })
                .attr("y", function (d) { return y(d[1]) - 5; })
                .attr("text-anchor", "middle")
                .style("font-size", "8px")

            function mouseover(d) {  // utility function to be called on mouseover.
                // filter for selected state.
                var st = flatBarData.filter(function (s) { return s.Terminal == d[0]; })[0],
                    nD = d3.keys(st.freq).map(function (s) { return { type: s, freq: st.freq[s] }; });

                // call update functions of pie-chart and legend.    
                pC.update(nD);
                leg.update(nD);
            }

            function mouseout(d) {    // utility function to be called on mouseout.
                // reset the pie-chart and legend.    
                pC.update(tF);
                leg.update(tF);
            }

            // create function to update the bars. This will be used by pie-chart.
            hG.update = function (nD, color) {
                // update the domain of the y-axis map to reflect change in frequencies.
                y.domain([0, d3.max(nD, function (d) { return d[1]; })]);

                // Attach the new data to the bars.
                var bars = hGsvg.selectAll(".bar").data(nD);

                // transition the height and color of rectangles.
                bars.select("rect").transition().duration(500)
                    .attr("y", function (d) { return y(d[1]); })
                    .attr("height", function (d) { return hGDim.h - y(d[1]); })
                    .attr("fill", color);

                // transition the frequency labels location and change value.
                bars.select("text").transition().duration(500)
                    .text(function (d) { return d3.format(",")(d[1]) })
                    .attr("y", function (d) { return y(d[1]) - 5; });
            }
            return hG;
        }
        // function to handle pieChart.
        function pieChart(id, pD) {
            // var hG={},    hGDim = {t: 60, r: 100, b: 150, l: 80};
            // hGDim.w = 500 - hGDim.l - hGDim.r, 
            // hGDim.h = 400 - hGDim.t - hGDim.b;

            // //create svg for histogram.
            // var hGsvg = d3.select(id).append("svg")
            //     .attr("width", hGDim.w + hGDim.l + hGDim.r)
            //     .attr("height", hGDim.h + hGDim.t + hGDim.b).append("g")
            //     .attr("transform", "translate(" + hGDim.l + "," + hGDim.t + ")");

            var pC = {}, pieDim = { w: 230, h: 230 };
            pieDim.r = Math.min(pieDim.w, pieDim.h) / 2;

            // create svg for pie chart.
            var piesvg = d3.select(id).append("svg")
                .attr("width", pieDim.w).attr("height", pieDim.h).append("g")
                .attr("transform", "translate(" + pieDim.w / 2 + "," + pieDim.h / 2 + ")")


            // create function to draw the arcs of the pie slices.
            var arc = d3.svg.arc().outerRadius(pieDim.r - 10).innerRadius(0);

            // create a function to compute the pie slice angles.
            var pie = d3.layout.pie().sort(null).value(function (d) { return d.freq; });
            console.log(pD)
            // Draw the pie slices.
            piesvg.selectAll("path").data(pie(pD)).enter().append("path").attr("d", arc)
                .each(function (d) { this._current = d; })
                .style("fill", function (d) {
                    console.log(d.data.type);
                    return segColor(d.data.type);
                })
                .on("mouseover", mouseover).on("mouseout", mouseout);

            // create function to update pie-chart. This will be used by histogram.
            pC.update = function (nD) {
                piesvg.selectAll("path").data(pie(nD)).transition().duration(500)
                    .attrTween("d", arcTween);
            }
            // Utility function to be called on mouseover a pie slice.
            function mouseover(d) {
                // call the update function of histogram with new data.
                hG.update(flatBarData.map(function (v) {
                    return [v.Terminal, v.freq[d.data.type]];
                }), segColor(d.data.type));
            }
            //Utility function to be called on mouseout a pie slice.
            function mouseout(d) {
                // call the update function of histogram with all data.
                hG.update(flatBarData.map(function (v) {
                    return [v.Terminal, v.total];
                }), barColor);
            }
            // Animating the pie-slice requiring a custom function which specifies
            // how the intermediate paths should be drawn.
            function arcTween(a) {
                var i = d3.interpolate(this._current, a);
                this._current = i(0);
                return function (t) { return arc(i(t)); };
            }
            return pC;
        }
        function legend(id, lD) {
            var leg = {};

            // create table for legend.
            var legend = d3.select(id).append("table").attr('class', 'legend');

            // create one row per segment.
            var tr = legend.append("tbody").selectAll("tr").data(lD).enter().append("tr");

            // create the first column for each segment.
            tr.append("td").append("svg").attr("width", '16').attr("height", '16').append("rect")
                .attr("width", '15').attr("height", '15')
                .attr("fill", function (d) { return segColor(d.type); });

            // create the second column for each segment.
            tr.append("td").text(function (d) { return d.type; });

            // create the third column for each segment.
            tr.append("td").attr("class", 'legendFreq')
                .text(function (d) { return d3.format(",")(d.freq); });

            // create the fourth column for each segment.
            tr.append("td").attr("class", 'legendPerc')
                .text(function (d) { return getLegend(d, lD); });

            // Utility function to be used to update the legend.
            leg.update = function (nD) {
                // update the data attached to the row elements.
                var l = legend.select("tbody").selectAll("tr").data(nD);

                // update the frequencies.
                l.select(".legendFreq").text(function (d) { return d3.format(",")(d.freq); });

                // update the percentage column.
                l.select(".legendPerc").text(function (d) { return getLegend(d, nD); });
            }

            function getLegend(d, aD) { // Utility function to compute percentage.
                return d3.format("%")(d.freq / d3.sum(aD.map(function (v) { return v.freq; })));
            }

            return leg;
        }

        var datearray = [];
        var colorrange = [];
        function chart(csvpath) {


            colorrange = ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc', '#e5d8bd', '#fddaec', '#b3b3b3']
            strokecolor = colorrange[0];

            var format = d3.time.format("%m/%d/%Y");

            var margin = { top: 20, right: 220, bottom: 30, left: 80 };
            var width = document.body.clientWidth - margin.left - margin.right;
            var height = 450 - margin.top - margin.bottom;

            var tooltip = d3.select("body")
                .append("div")
                .attr("class", "remove")
                .style("position", "absolute")
                .style("z-index", "20")
                .style("visibility", "hidden")
                .style("top", "600px")
                .style("left", "200px");

            var x = d3.time.scale()
                .range([0, width]);

            var y = d3.scale.linear()
                .range([height - 10, 0]);

            var z = d3.scale.ordinal()
                .range(colorrange);

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom")
                .ticks(d3.time.years);

            var yAxis = d3.svg.axis()
                .scale(y);

            var yAxisr = d3.svg.axis()
                .scale(y);

            var stack = d3.layout.stack()
                .offset("silhouette")
                .values(function (d) { return d.values; })
                .x(function (d) { return d.ReportPeriod; })
                .y(function (d) { return d.Passenger_Count; });

            var nest = d3.nest()
                .key(function (d) {
                    // console.log(d.Terminal)
                    return d.Terminal;
                });

            var area = d3.svg.area()
                .interpolate("cardinal")
                .x(function (d) {
                    return x(d.ReportPeriod);
                })
                .y0(function (d) {
                    // console.log(d.y0)
                    return y(d.y0);
                })
                .y1(function (d) { return y(d.y0 + d.y); });

            var svg = d3.select(".streamGraph").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
            // var hehe = d3.csv(csvpath, function (data) {
            //         data = data.filter(function(row){
            //             return row['Terminal'] == "Terminal 1" || ;
            //         })
            //         console.log(data)
            // })
            var graph = d3.csv(csvpath, function (data) {
                data = data.filter(function (row) {
                    return row['Terminal'] == "Terminal 1" || row['Terminal'] == "Terminal 2" || row['Terminal'] == "Terminal 3" || row['Terminal'] == "Terminal 4" || row['Terminal'] == "Terminal 5" || row['Terminal'] == "Terminal 6" || row['Terminal'] == "Terminal 7" || row['Terminal'] == "Terminal 8" || row['Terminal'] == "Tom Bradley International Terminal";
                })
                console.log(data)
                var streamData = data.map(function (d) {
                    return {
                        Terminal: d.Terminal,
                        ReportPeriod: d.ReportPeriod.slice(0, -12),
                        Passenger_Count: d.Passenger_Count
                    }
                });
                var streamDataNested = d3.nest()
                    .key(function (d) { return d.Terminal; })
                    .key(function (d) { return d.ReportPeriod; })
                    .rollup(function (v) {
                        return {
                            total_passenger: d3.sum(v, function (d) { return d.Passenger_Count; })
                        };
                    })
                    .entries(streamData);
                // console.log(streamDataNested)
                flatStreamData = []
                streamDataNested.forEach(function (d) {
                    // console.log(d);
                    d.values.forEach(function (f) {

                        flatStreamData.push({ Terminal: d.key, ReportPeriod: f.key, Passenger_Count: f.values['total_passenger'] });

                    });

                });
                console.log(flatStreamData)
                flatStreamData.forEach(function (d) {
                    // console.log(d.ReportPeriod)
                    d.ReportPeriod = format.parse(d.ReportPeriod);
                    // console.log(d.ReportPeriod.getFullYear())
                    d.Passenger_Count = + d.Passenger_Count;
                });

                var layers = stack(nest.entries(flatStreamData));
                console.log(layers)
                x.domain(d3.extent(flatStreamData, function (d) {
                    return d.ReportPeriod;
                }));
                // flatStreamData.forEach(function (d){
                //     if(d.y0 == null){
                //         d.y0 = 50000
                //         d.y = d.Passenger_Count;
                //     }
                // });
                y.domain([0, d3.max(flatStreamData, function (d) { return d.y0 + d.y; })]);
                svg.append("circle").attr("cx", 850).attr("cy", 170).attr("r", 4).style("fill", "#fbb4ae")
                svg.append("circle").attr("cx", 850).attr("cy", 150).attr("r", 4).style("fill", "#b3cde3")
                svg.append("circle").attr("cx", 850).attr("cy", 130).attr("r", 4).style("fill", "#ccebc5")
                svg.append("circle").attr("cx", 850).attr("cy", 110).attr("r", 4).style("fill", "#decbe4")
                svg.append("circle").attr("cx", 850).attr("cy", 90).attr("r", 4).style("fill", "#fed9a6")
                svg.append("circle").attr("cx", 850).attr("cy", 70).attr("r", 4).style("fill", "#ffffcc")
                svg.append("circle").attr("cx", 850).attr("cy", 50).attr("r", 4).style("fill", "#e5d8bd")
                svg.append("circle").attr("cx", 850).attr("cy", 30).attr("r", 4).style("fill", "#fddaec")
                svg.append("circle").attr("cx", 850).attr("cy", 10).attr("r", 4).style("fill", "#b3b3b3")
                svg.append("text").attr("x", 860).attr("y", 170).text("Terminal 1").style("font-size", "10px").attr("alignment-baseline", "middle")
                svg.append("text").attr("x", 860).attr("y", 150).text("Terminal 2").style("font-size", "10px").attr("alignment-baseline", "middle")
                svg.append("text").attr("x", 860).attr("y", 130).text("Terminal 3").style("font-size", "10px").attr("alignment-baseline", "middle")
                svg.append("text").attr("x", 860).attr("y", 110).text("Terminal 4").style("font-size", "10px").attr("alignment-baseline", "middle")
                svg.append("text").attr("x", 860).attr("y", 90).text("Terminal 5").style("font-size", "10px").attr("alignment-baseline", "middle")
                svg.append("text").attr("x", 860).attr("y", 70).text("Terminal 6").style("font-size", "10px").attr("alignment-baseline", "middle")
                svg.append("text").attr("x", 860).attr("y", 50).text("Terminal 7").style("font-size", "10px").attr("alignment-baseline", "middle")
                svg.append("text").attr("x", 860).attr("y", 30).text("Terminal 8").style("font-size", "10px").attr("alignment-baseline", "middle")
                svg.append("text").attr("x", 860).attr("y", 10).text("Tom Bradley International").style("font-size", "10px").attr("alignment-baseline", "middle")

                svg.selectAll(".layer")
                    .data(layers)
                    .enter().append("path")
                    .attr("class", "layer")
                    .attr("d", function (d) { return area(d.values); })
                    .style("fill", function (d, i) { return z(i); });


                svg.append("g")
                    .attr("class", "x axis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(xAxis);

                svg.append("g")
                    .attr("class", "y axis")
                    .attr("transform", "translate(" + width + ", 0)")
                    .call(yAxis.orient("right"));

                svg.append("g")
                    .attr("class", "y axis")
                    .call(yAxis.orient("left"));

                svg.selectAll(".layer")
                    .attr("opacity", 1.5)
                    .on("mouseover", function (d, i) {
                        svg.selectAll(".layer").transition()
                            .duration(250)
                            .attr("opacity", function (d, j) {
                                return j != i ? 0.4 : 1;
                            })
                    })

                    .on("mousemove", function (d, i) {
                        mousex = d3.mouse(this);
                        mousex = mousex[0];
                        var invertedx = x.invert(mousex);
                        invertedx = invertedx.getMonth() + invertedx.getDate();
                        var selected = (d.values);
                        for (var k = 0; k < selected.length; k++) {
                            datearray[k] = selected[k].ReportPeriod
                            datearray[k] = datearray[k].getMonth() + datearray[k].getDate();
                        }

                        mousedate = datearray.indexOf(invertedx);
                        console.log(d.values[mousedate])
                        pro = d.values[mousedate].Passenger_Count;
                        var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

                        d3.select(this)
                            .classed("hover", true)
                            .attr("stroke", strokecolor)
                            .attr("stroke-width", "0.5px"),
                            tooltip.html("<p>" + d.key + "<br>" + pro + "</p>").style("visibility", "visible").style("font-size", "10px");

                    })
                    .on("mouseout", function (d, i) {
                        svg.selectAll(".layer")
                            .transition()
                            .duration(250)
                            .attr("opacity", "1");
                        d3.select(this)
                            .classed("hover", false)
                            .attr("stroke-width", "0px"), tooltip.html("<p>" + d.key + "<br>" + pro + "</p>").style("visibility", "hidden");
                    })

                var vertical = d3.select(".streamGraph")
                    .append("div")
                    .attr("class", "remove")
                    .style("position", "absolute")
                    .style("z-index", "19")
                    .style("width", "1px")
                    .style("height", "380px")
                    .style("top", "600px")
                    .style("bottom", "30px")
                    .style("left", "0px")
                    .style("right", "100px")
                    .style("background", "#fff");

                d3.select(".streamGraph")
                    .on("mousemove", function () {
                        mousex = d3.mouse(this);
                        mousex = mousex[0] + 100;
                        vertical.style("left", mousex + "px")
                    })
                    .on("mouseover", function () {
                        mousex = d3.mouse(this);
                        mousex = mousex[0] + 100;
                        vertical.style("left", mousex + "px")
                    });
            });
        }
        console.log(flatBarData)
        var tF = ['Arrival', 'Departure'].map(function (d) {
            return { type: d, freq: d3.sum(flatBarData.map(function (t) { return t.freq[d]; })) };
        });

        var sF = flatBarData.map(function (d) { return [d.Terminal, d.total]; });

        var hG = histoGram('#barChart', sF),
            pC = pieChart('#barChart', tF),
            leg = legend('#barChart', tF)
        chart("./Los_Angeles_International_Airport_-_Passenger_Traffic_By_Terminal.csv");

        // console.log(hG)
    })
})()