var dataByTerminal = null
var dataByArrivalDeparture = null
var dataByDomesticInternational = null

var streamGraphSVG = null
var streamGraphInnerWidth = 0
var streamGraphInnerHeight = 0

var Tooltip = document.getElementById('Tooltip')

var dropDown = document.getElementById('dropDown')

function init2() {
    var streamGraphMargin = {top: 10, right: 10, bottom: 40, left:60}
    var streamGraphWidth = 700
    var streamGraphHeight = 500
    streamGraphInnerWidth = streamGraphWidth - streamGraphMargin.left - streamGraphMargin.right
    streamGraphInnerHeight = streamGraphHeight - streamGraphMargin.top - streamGraphMargin.bottom

    streamGraphSVG = d3.select('#stream-graph')
        .attr("width", streamGraphWidth)
        .attr("height", streamGraphHeight)
        .append('g')
        .attr("transform",
            "translate(" + streamGraphMargin.left + ", " + streamGraphMargin.top + ")")
    
    // Prepare Data for Display in Advance
    nestedData = d3.nest().key(function (d) {
        return d['ReportPeriod'];
    }).key(function (d) {
        return d['Arrival_Departure']
    }).rollup(function (leaves) {
        return d3.sum(leaves, function (d) {
            return parseInt(d['Passenger_Count'])
        })
    }).entries(data)

    dataByArrivalDeparture = []
    nestedData.forEach(function (d) {
        var t = new Array(arrivalDeparture.length + 1).fill(0)
        t[0] = d.key
        d.values.forEach(function (dv) {
            t[arrivalDeparture.indexOf(dv.key) + 1] = dv.value
        })
        var o = {};
        o['ReportPeriod'] = t[0]
        for (var i = 1; i < t.length; i++) {
            o[arrivalDeparture[i - 1]] = t[i]
        }
        dataByArrivalDeparture.push(o)
    })

    nestedData = d3.nest().key(function (d) {
        return d['ReportPeriod'];
    }).key(function (d) {
        return d['Domestic_International']
    }).rollup(function (leaves) {
        return d3.sum(leaves, function (d) {
            return parseInt(d['Passenger_Count'])
        })
    }).entries(data)

    dataByDomesticInternational = []
    nestedData.forEach(function (d) {
        var t = new Array(domesticInternational.length + 1).fill(0)
        t[0] = d.key
        d.values.forEach(function (dv) {
            t[domesticInternational.indexOf(dv.key) + 1] = dv.value
        })
        var o = {};
        o['ReportPeriod'] = t[0]
        for (var i = 1; i < t.length; i++) {
            o[domesticInternational[i - 1]] = t[i]
        }
        dataByDomesticInternational.push(o)
    })

    //Changed need to be restored
    nestedData = d3.nest().key(function (d) {
        return d['ReportPeriod'];
    }).key(function (d) {
        return d['Terminal']
    }).rollup(function (leaves) {
        return d3.sum(leaves, function (d) {
            return parseInt(d['Passenger_Count'])
        })
    }).entries(data)

    dataByTerminal = [] // lodash
    nestedData.forEach(function (d) {
        var t = new Array(terminals.length + 1).fill(0)
        t[0] = d.key
        d.values.forEach(function (dv) {
            t[terminals.indexOf(dv.key) + 1] = dv.value
        })
        var o = {};
        o['ReportPeriod'] = t[0]
        for (var i = 1; i < t.length; i++) {
            o[terminals[i - 1]] = t[i]
        }
        dataByTerminal.push(o)
    })

    // console.log(dataByTerminal)
    // console.log(dataByArrivalDeparture)
    // console.log(dataByDomesticInternational)
}

function onChange2(){
    var selectedAspect = dropDown.options[dropDown.selectedIndex].value;
    // console.log(selectedAspect)
    var colorRange = []
    var selectedData = null
    var possibleKeys = null
    if(selectedAspect == 'arrival_departure') {
        colorRange = ["#FFFF00", "0000FF"]
        selectedData = dataByArrivalDeparture
        possibleKeys = arrivalDeparture
    } else if(selectedAspect == 'domestic_international') {
        colorRange = ["#FF0000", "00FFFF"]
        selectedData = dataByDomesticInternational
        possibleKeys = domesticInternational
    } else {
        // colorRange = ["#FF0000", "#FF7F00", "#FFFF00", "#7FFF00", "#00FF00", "#00FF7F", "#00FFFF", "#007FFF", "#0000FF", "#7F00FF", "#FF00FF", "#FF007F"]
        colorRange = d3.schemeDark2
        selectedData = dataByTerminal
        possibleKeys = terminals
    }

    // var xScale2 = d3.scalePoint()
    //     .range([0, streamGraphInnerWidth])
    Tooltip.innerHTML = 'Touch the stream to get the detailed quantity!'
    
    var xScale2 = d3.scaleTime()
        .range([0, streamGraphInnerWidth])

    var yScale2 = d3.scaleLinear()
        .range([streamGraphInnerHeight, 0])
    var zScale2 = d3.scaleOrdinal()
        .range(colorRange)
    
    var stack = d3.stack()
        .offset(d3.stackOffsetSilhouette)
        .keys(possibleKeys)
    
    var layers = stack(selectedData)

    // console.log(layers)

    // xScale2.domain(timeStamps)
    // xScale2.domain([new Date(2006, 0, 1), new Date(2008, 4, 1)])
    xScale2.domain(d3.extent(selectedData, function(d) {return Date.parse(d.ReportPeriod)}))
    // console.log(d3.extent(selectedData, function(d) {return Date.parse(d.reportperiod)}))
    yScale2.domain([-4000000, 4000000])

    var xAxis2 = d3.axisBottom()
        .scale(xScale2)

    var yAxis2 = d3.axisLeft()
        .scale(yScale2)

    var area = d3.area()
    .x(function(d) {return xScale2(new Date(d.data.ReportPeriod))})
    .y0(function(d) {return yScale2(d[0])})
    .y1(function(d) {return yScale2(d[1])})

    var mouseOver = function(d, i) {
        streamGraphSVG.selectAll('path')
            .transition()
            .duration(500)
            .style('opacity', function(d, j) {
                if(j == i) return 1
                return 0.3
            })
        d3.select(this)
            .style('stroke', 'black')
    }

    var mouseMove = function(d, i) {
        mouseX = d3.mouse(this)[0]
        var invertedX = xScale2.invert(mouseX)
        var roundedX = timeStamps[0]
        for(var j = 0; j < timeStamps.length; j++) {
            if(Math.abs(Date.parse(invertedX) - Date.parse(timeStamps[j])) < Math.abs(Date.parse(invertedX) - Date.parse(roundedX))) {
                roundedX = timeStamps[j]
            }
        }
        var count = 0
        selectedData.forEach(function(d) {
            if(d['ReportPeriod'] == roundedX) {
                count = d[possibleKeys[i]]
            }
        })
        roundedX = new Date(roundedX)
        Tooltip.innerHTML = 'You have selected <b>' + possibleKeys[i] + '</b>, where the passenger count is <b>' + count + '</b> in <b>' + (roundedX.getMonth() + 1) + '/' + roundedX.getFullYear() + '</b>.'
    }

    var mouseLeave = function(d) {
        streamGraphSVG.selectAll('path')
            .style('stroke', 'none')
            .transition()
            .duration(500)
            .style('opacity', 1)
        Tooltip.innerHTML = Tooltip.innerHTML = 'Touch the stream to get the detailed quantity!'
    }

    streamGraphSVG.selectAll('path').remove();

    streamGraphSVG.selectAll('path')
        .data(layers)
        .enter()
        .append('path')
            .style('fill', function(d) {return zScale2(d.key)})
            .attr('d', area)
            .on('mouseover', mouseOver)
            .on('mouseleave', mouseLeave)
            .on('mousemove', mouseMove)
    
    streamGraphSVG.append('g')
        .call(xAxis2)
        .attr('transform', 'translate(0, ' + streamGraphInnerHeight + ')')
        .selectAll('text')
        .attr('transform', 'translate(-11,10) rotate(-50)')
    
    streamGraphSVG.append('g')
        .call(yAxis2)
}