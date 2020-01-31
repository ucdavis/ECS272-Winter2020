var width = 960,
  height = 600,
  scale = 270000,
  latitude = 37.7750,
  longitude = -122.4183;
var selectedStr = "";
var showNone = false;
var sankyFilteredRows = [];
function toggleNone() {
  showNone = !showNone;
  console.log(showNone);

  if (!showNone) {
    let newFiltered = [];
    for (let i = 0; i < filteredRows.length; i++) {
      if (filteredRows[i].Resolution != 'NONE') {
        console.log("in");
        newFiltered.push(filteredRows[i]);
      }
    }
    sankyFilteredRows = newFiltered;
  } else {
    sankyFilteredRows = filteredRows;
  }
  changeSankyFilter();
}

var svg = d3.select("#test")
  .attr("width", width)
  .attr("height", height);

var hoods = svg.append("g")
  .attr("id", "hoods");

var circles = svg.append("g")
  .attr("id", "circles");

var xym = d3.geo.mercator()
  .scale(scale)
  .rotate([-longitude, 0])
  .center([0, latitude]);

var path = d3.geo.path().projection(xym);
var districtdiv = d3.select("body").append("div")
  .attr("class", "dist-tooltip");


d3.json("SFN.geojson", function (data) {
  hoods.selectAll("path").data(data.features)
    .enter().append("svg:path")
    .attr("d", path)
    .style("fill", function () { return "#003366" })
    .on("mouseover", function (e) {

      districtdiv.style("display", "none");
      districtdiv
        .html("Zip: " + e.id)
        .style("left", (d3.event.pageX + 12) + "px")
        .style("top", (d3.event.pageY - 10) + "px")
        .style("opacity", 1)
        .style("display", "block")
        .transition().duration(10000)
      d3.select(this).style("fill", "teal");
    })
    .on("mouseout", function (e) {
      districtdiv.html(" ").style("display", "none");

      d3.select(this).style("fill", "#003366")
    })
    .attr("stroke", "white")
    .attr("stroke-width", 1)
});

// var xy = xym([longitude, latitude])
// console.log(xy)
// hoods.append('text')
//   .attr('x', 960)
//   .attr('y', 30)
//   .text('San Francisco Crime')
//   .attr('fill', 'tomato')
//   .attr('font-family', 'sans-serif')
//   .attr('font-size', 32)
//   .transition().duration(1000)
//   .attr('x', 10);
var div = d3.select("body").append("div")
  .attr("class", "tooltip");

var first = true;
var positions = [];
var form_add = [];
var pdId = [];
var lonlat = [];

var tip = d3.select('#tip');
var lpic = d3.select('#lpic');
var options = [];
var filteredRows = [];
var filteredPosns = [];
var allRows = [];

async function filtering(loadedRows, selectedStr) {
  filteredRows = [];
  filteredPosns = [];
  console.log("filtering");
  console.log(selectedStr);
  loadedRows.forEach(function (row) {
    row.lat = parseFloat(row.Y);
    row.lon = parseFloat(row.X);
    if (!options.includes(row.Category)) {
      options.push(row.Category);
    }

    if (row.Category.trim() === selectedStr) {

      filteredRows.push(row);
      filteredPosns.push(xym([row.lon, row.lat]));
    }
    //console.log(row.lon)
    positions.push(xym([row.lon, row.lat]));
    form_add.push(row.form_add)
    pdId.push(row.PdId)
    lonlat.push([row.lon, row.lat])
    //console.log(row.form_add);

  });

}

async function selectfiltering(loadedRows, selectedStr) {
  filteredPosns = [];
  filteredRows = [];
  console.log("selectfiltering");
  console.log(selectedStr);
  console.log(loadedRows.length);
  loadedRows.forEach(function (row) {
    row.lat = parseFloat(row.Y);
    row.lon = parseFloat(row.X);


    if (row.Category.trim() == selectedStr) {

      console.log("match");
      filteredRows.push(row);
      filteredPosns.push(xym([row.lon, row.lat]));
    }
    //console.log(row.lon)

  });

}

d3.csv("Police_Department_Incidents_-_Previous_Year__2016_.csv", function (loadedRows) {
  //var positions = [];
  //mData = loadedRows;  
  allRows = loadedRows;
  for (let i = 0; i < allRows.length; i++) {
    if (parseInt(allRows[i].Time.split(":")[1]) > 30) {
      allRows[i].Time = parseInt(allRows[i].Time.split(":")[0]);
    } else {
      if (parseInt(allRows[i].Time.split(":")[0]) == 23) {
        allRows[i].Time = 0;
      } else {
        allRows[i].Time = parseInt(allRows[i].Time.split(":")[0]) + 1;
      }
    }
  }
  console.log(loadedRows[0]);
  filtering(allRows, "BURGLARY").then(dat => {

    var dropDown = $('#widget');
    var innerStr = '';
    options.forEach(opt => {
      if (opt.trim() === "BURGLARY") {
        innerStr += '<option value="' + opt + '" selected="selected">' + opt + '</option>'
      } else {
        innerStr += '<option value="' + opt + '">' + opt + '</option>'
      }
    });
    dropDown.html(innerStr);
    let newFiltered = [];
    for (let i = 0; i < filteredRows.length; i++) {
      if (filteredRows[i].Resolution != 'NONE') {
        console.log("in");
        newFiltered.push(filteredRows[i]);
      }
    }
    sankyFilteredRows = newFiltered;
    renderCircle(filteredPosns);
    renderSanky("BURGLARY", "DayOfWeek");
    //
  });
});

function changeFilter() {

  console.log($('#widget option:selected').text());
  console.log("allRows");
  selectedStr = $('#widget option:selected').text();
  console.log(allRows.length);
  selectfiltering(allRows, $('#widget option:selected').text()).then(() => {
    console.log(filteredPosns.length);
    d3.select("#circles").selectAll("*").remove();
    d3.select("#chart").selectAll("*").remove();
    if (!showNone) {
      let newFiltered = [];
      for (let i = 0; i < filteredRows.length; i++) {
        if (filteredRows[i].Resolution != 'NONE') {
          console.log("in");
          newFiltered.push(filteredRows[i]);
        }
      }
      sankyFilteredRows = newFiltered;
    } else {
      sankyFilteredRows = filteredRows;
    }

    renderCircle(filteredPosns);
    renderSanky($('#widget option:selected').text(), 'DayOfWeek');
  });
}

function renderCircle(filteredPosns) {

  circles.selectAll("circle")
    .data(filteredPosns)
    .enter().append("circle")
    .attr("cx", function (d, i) { return filteredPosns[i][0]; })
    //.transition().duration(10000).attr("cx", function(d,i){return positions[i][0];})
    .attr("cy", function (d, i) { return filteredPosns[i][1]; })
    //.transition().duration(1000).attr("cy", function(d,i){return positions[i][1];})
    .attr("r", "2.5px")
    .attr("stroke", "black")
    .style("fill", function (d) {

      return "yellow";
    })
    .attr("id", function (d, i) { return pdId[i]; })
    .on("mouseover", function (d, i) {
      d3.select(this).style("fill", " red")
        .transition(100).attr('r', 10)
      //d3.select(circles).circle.style('fill','lawngreen')
      cy = this.cy.baseVal.value;

      tip.style('display', 'block')
        .style('left', 650 + 'px')
        .style('top', 30 + 'px')
        //.select(".hoods").text(form_add[i])  //form_add[i];})
        .select("#tip .zip").text(function () { return 'Vertigo'; });


      div.style("display", "none");
      div
        .html(filteredRows[i].Descript)
        .style("left", (d3.event.pageX + 12) + "px")
        .style("top", (d3.event.pageY - 10) + "px")
        .style("opacity", 1)
        .style("display", "block");
    })
    .on("mouseout", function () {
      d3.select(this).style("fill", "yellow").transition(100).attr('r', 2.5)
      tip.style('display', 'none');
      lpic.style('display', 'none');
      div.html(" ").style("display", "none");
    });
  // circles.selectAll('circle').transition(100).attr("r",3);
}

function renderSanky(selectedStr, selectedField) {

  createSankyData(selectedStr, selectedField).then(graph => {
    var units = "Widgets";
    //console.log(graph);

    var smargin = { top: 10, right: 10, bottom: 10, left: 10 },
      swidth = 700 - smargin.left - smargin.right;

    if (selectedField == "Time") {
      sheight = 1000 - smargin.top - smargin.bottom;
    } else {
      sheight = 480 - smargin.top - smargin.bottom;
    }

    var formatNumber = d3.format(",.0f"),    // zero decimal places
      format = function (d) { return formatNumber(d) + " " + units; },
      color = d3.scale.category20();

    color = d3.scale.linear().domain([1, 20])
      .interpolate(d3.interpolateHcl)
      .range([d3.rgb("#007AFF"), d3.rgb('#FFF500')]);
    var svg = d3.select("#chart")
      .attr("width", swidth + smargin.left + smargin.right)
      .attr("height", sheight + smargin.top + smargin.bottom)
      .append("g")
      .attr("transform",
        "translate(" + smargin.left + "," + smargin.top + ")");
    var color = d3.schemeCategory20;
    var sankey = d3.sankey()
      .nodeWidth(36)
      .nodePadding(40)
      .size([swidth, sheight]);

    var path = sankey.link();
    sankey
      .nodes(graph.nodes)
      .links(graph.links)
      .layout(32);

    var link = svg.append("g").selectAll(".link")
      .data(graph.links)
      .enter().append("path")
      .attr("class", "link")
      .attr("d", path)
      .style("stroke-width", function (d) { return Math.max(1, d.dy); })
      .sort(function (a, b) { return b.dy - a.dy; });

    link.append("title")
      .text(function (d) {
        return d.source.name + " → " +
          d.target.name + "\n" + format(d.value);
      });
    // color = d3.scale.linear().domain([1,20])
    // .interpolate(d3.interpolateHcl)
    // .range([d3.rgb("#007AFF"), d3.rgb('#FFF500')]);
    var color = d3.scale.category10();
    var node = svg.append("g").selectAll(".node")
      .data(graph.nodes)
      .enter().append("g")
      .attr("class", "node")
      .attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
      })
      .call(d3.behavior.drag()
        .origin(function (d) { return d; })
        .on("dragstart", function () {
          this.parentNode.appendChild(this);
        })
        .on("drag", dragmove));

    node.append("rect")
      .attr("height", function (d) { return d.dy; })
      .attr("width", sankey.nodeWidth())
      .style("fill", function (d) {
        return d.color = color(d.name);
      })
      .style("stroke", function (d) {
        return d3.rgb(d.color).darker(2);
      })
      .append("title")
      .text(function (d) {
        return d.name + "\n" + format(d.value);
      });

    node.append("text")
      .attr("x", -6)
      .attr("y", function (d) { return d.dy / 2; })
      .attr("dy", ".35em")
      .attr("text-anchor", "end")
      .attr("transform", null)
      .text(function (d) {
        if (Number.isInteger(d.name)) {
          return d.name + ":00";
        }
        return d.name;
      })
      .filter(function (d) { return d.x < width / 2; })
      .attr("x", 6 + sankey.nodeWidth())
      .attr("text-anchor", "start");

    function dragmove(d) {
      d3.select(this).attr("transform",
        "translate(" + (
          d.x = Math.max(0, Math.min(width - d.dx, d3.event.x))
        )
        + "," + (
          d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))
        ) + ")");
      sankey.relayout();
      link.attr("d", path);
    }

  });
}

function changeSankyFilter() {
  //console.log(filteredRows);
  d3.select("#chart").selectAll("*").remove();
  //console.log($('#widget2').children("option:selected").val());
  renderSanky($('#widget option:selected').text(), $('#widget2').children("option:selected").val())
}


async function createSankyData(selectedStr, selectedField) {
  graph = { "nodes": [], "links": [] };
  let nodeVal = 0;
  let resDict = [];
  let dayArr = [];
  graph.nodes.push({ "node": nodeVal++, "name": selectedStr });
  for (let loopVar = 0; loopVar < sankyFilteredRows.length; loopVar++) {
    let prevNode = null;
    // console.log(filteredRows[loopVar].DayOfWeek);
    for (let inloop = 0; inloop < graph.nodes.length; inloop++) {
      if (graph.nodes[inloop].name == sankyFilteredRows[loopVar].Resolution) {
        prevNode = graph.nodes[inloop];
        break;
      }
    }

    if (prevNode == null) {
      graph.nodes.push({ "node": nodeVal++, "name": sankyFilteredRows[loopVar].Resolution });
      graph.links.push({ "source": 0, "target": nodeVal - 1, "value": 0 });
    }


    let prevRes = null;
    for (let inloop = 0; inloop < resDict.length; inloop++) {
      if (resDict[inloop].key == sankyFilteredRows[loopVar].Resolution) {
        prevRes = resDict[inloop];
        break;
      }
    }
    if (prevRes == undefined) {
      newRes = {};
      newRes.count = 1;
      newRes.nodeVal = nodeVal - 1;
      newRes.key = sankyFilteredRows[loopVar].Resolution;
      newRes.days = [];
      newDay = { "day": sankyFilteredRows[loopVar][selectedField], "count": 1 };

      if (dayArr[sankyFilteredRows[loopVar][selectedField]] == undefined) {
        let dayName = sankyFilteredRows[loopVar][selectedField];
        graph.nodes.push({ "node": nodeVal++, "name": dayName });
        newDay.nodeVal = nodeVal - 1;
        dayArr[dayName] = newDay.nodeVal;
      } else {
        newDay.nodeVal = dayArr[sankyFilteredRows[loopVar][selectedField]];
      }
      newRes.days.push(newDay);
      resDict.push(newRes);
    } else {

      prevRes.count++;
      let prevResDay = null;
      for (let i = 0; i < prevRes.days.length; i++) {
        if (prevRes.days[i].day == sankyFilteredRows[loopVar][selectedField]) {
          prevResDay = prevRes.days[i];
          break;
        }
      }
      if (prevResDay == null) {

        if (dayArr[sankyFilteredRows[loopVar][selectedField]] == undefined) {
          newDay = { "day": sankyFilteredRows[loopVar][selectedField], "count": 1 };
          graph.nodes.push({ "node": nodeVal++, "name": sankyFilteredRows[loopVar][selectedField] });
          newDay.nodeVal = nodeVal - 1;
          prevRes.days.push(newDay);
          dayArr[sankyFilteredRows[loopVar][selectedField]] = newDay.nodeVal;
        } else {
          newDay = { "day": sankyFilteredRows[loopVar][selectedField], "count": 1 };
          newDay.nodeVal = dayArr[sankyFilteredRows[loopVar][selectedField]];
          prevRes.days.push(newDay);
        }
      } else {
        prevResDay.count++;
      }

    }
  }
  // console.log(dayArr);
  // console.log(resDict);
  for (let i = 0; i < resDict.length; i++) {

    for (let j = 0; j < graph.links.length; j++) {
      if (graph.links[j].target == resDict[i].nodeVal) {
        graph.links[j].value = resDict[i].count;
        break;
      }
    }

    for (let k = 0; k < resDict[i].days.length; k++) {
      let newlink = {};
      newlink.source = resDict[i].nodeVal;
      newlink.target = resDict[i].days[k].nodeVal;
      newlink.value = resDict[i].days[k].count;
      graph.links.push(newlink);
    }
  }
  // console.log(graph);
  return graph;
}

