var data = null

d3.csv("./datasets/tmdb\_5000\_movies.csv").then(grandData => {
    data = grandData
    var timeParse = d3.timeParse('%Y-%m-%d')
    data.forEach(function (d) {
        d['release\_date'] = timeParse(d['release\_date'])
    })
    initStreamGraph()
    initBarChart()
})

// Config of stream graph

var streamGraphMargin = { top: 10, right: 10, bottom: 40, left: 60 }
var streamGraphWidth = 800
var streamGraphHeight = 500
var streamGraphInnerWidth, stremGraphInnerHeight

var streamGraphSVG = null
var pieChartSVG = null
var tagCloudSVG = null

var tooltipStreamGraph = document.getElementById('tooltip-stream-graph')

var dropDown = document.getElementById('dropDown')

var mouseOverHandlerStreamGraph = null
var mouseClickHandlerStreamGraph = null
var mouseLeaveHandlerStreamGraph = null

var xScaleStreamGraph = null
var yScaleStreamGraph = null
var zScaleStreamGraph = null

var selectedStream = -1

var overviews = null

var dataByVote
var dataByPopularity

function initStreamGraph() {
    streamGraphInnerWidth = streamGraphWidth - streamGraphMargin.left - streamGraphMargin.right
    streamGraphInnerHeight = streamGraphHeight - streamGraphMargin.top - streamGraphMargin.bottom

    streamGraphSVG = d3.select('#stream-graph-SVG')
        .attr("width", streamGraphWidth)
        .attr("height", streamGraphHeight)
        .append('g')
        .attr("transform",
            "translate(" + streamGraphMargin.left + ", " + streamGraphMargin.top + ")")

    // Prepare data
    // Data by vote average
    nestedData = d3.nest().key(function (d) {
        var date = new Date(d['release\_date'])
        return date.getFullYear()
    }).key(function (d) {
        var voteAverage = parseInt(d['vote\_average'])
        if (voteAverage == 0) return 0
        else if (voteAverage <= 2) return 2
        else if (voteAverage <= 4) return 4
        else if (voteAverage <= 6) return 6
        else if (voteAverage <= 8) return 8
        else return 10
    }).rollup(function (leaves) {
        return leaves.length
    }).entries(data)
    dataByVote = []
    nestedData.forEach(function (d) {
        var t = new Array(7).fill(0)
        t[0] = d.key
        d.values.forEach(function (dv) {
            t[parseInt(dv.key) / 2 + 1] = dv.value
        })
        var o = {}
        o['release\_date'] = t[0]
        o['unrated'] = t[1]
        o['awful'] = t[2]
        o['bad'] = t[3]
        o['so-so'] = t[4]
        o['good'] = t[5]
        o['excellent'] = t[6]
        dataByVote.push(o)
    })
    dataByVote.sort(function (a, b) {
        return parseInt(a['release\_date']) > parseInt(b['release\_date']) ? 1 : -1
    })
    // Data by popularity
    popularities = []
    data.forEach(function (d) {
        popularities.push(parseFloat(d['popularity']))
    })
    popularities.sort(function (a, b) {
        return a - b
    })
    q1 = popularities[Math.round(popularities.length / 4)]
    q2 = popularities[Math.round(popularities.length / 2)]
    q3 = popularities[Math.round(popularities.length * 3 / 4)]
    
    nestedData = d3.nest().key(function (d) {
        var date = new Date(d['release\_date'])
        return date.getFullYear()
    }).key(function (d) {
        var popularity = parseFloat(d['popularity'])
        if (popularity <= q1) return 1
        else if (popularity <= q2) return 2
        else if (popularity <= q3) return 3
        else return 4
    }).rollup(function (leaves) {
        return leaves.length
    }).entries(data)

    dataByPopularity = []
    nestedData.forEach(function (d) {
        var t = new Array(5).fill(0)
        t[0] = d.key
        d.values.forEach(function (dv) {
            t[dv.key] = dv.value
        })
        var o = {}
        o['release\_date'] = t[0]
        o['very\_unpopular'] = t[1]
        o['unpopular'] = t[2]
        o['popular'] = t[3]
        o['very\_popular'] = t[4]
        dataByPopularity.push(o)
    })
    dataByPopularity.sort(function (a, b) {
        return parseInt(a['release\_date']) > parseInt(b['release\_date']) ? 1 : -1
    })
    
    xScaleStreamGraph = d3.scaleTime()
        .range([0, streamGraphInnerWidth])
    yScaleStreamGraph = d3.scaleLinear()
        .range([streamGraphInnerHeight, 0])
    zScaleStreamGraph = d3.scaleOrdinal()
        .range(d3.schemeCategory10)
}

function onChangeStreamGraph() {
    var selectedAspect = dropDown.options[dropDown.selectedIndex].value;
    var selectedData = null
    var possibleKeys = null
    if (selectedAspect == 'vote-average') {
        barChartSVG.selectAll('*')
            .remove()
        tagCloudSVG.selectAll("*").remove();

        selectedData = dataByVote
        possibleKeys = ['unrated', 'awful', 'bad', 'so-so', 'good', 'excellent']
        overviews = []
        for (var i = 0; i < possibleKeys.length; i++) {
            overviews.push([])
        }
        data.forEach(function (d) {
            var voteAverage = parseInt(d['vote\_average'])
            if (voteAverage == 0) overviews[0].push(d['overview'])
            else if (voteAverage <= 2) overviews[1].push(d['overview'])
            else if (voteAverage <= 4) overviews[2].push(d['overview'])
            else if (voteAverage <= 6) overviews[3].push(d['overview'])
            else if (voteAverage <= 8) overviews[4].push(d['overview'])
            else return overviews[5].push(d['overview'])
        })
    } else if (selectedAspect == 'popularity') {
        barChartSVG.selectAll('*')
            .remove()
        tagCloudSVG.selectAll("*").remove();
        selectedData = dataByPopularity
        possibleKeys = ['very\_unpopular', 'unpopular', 'popular', 'very\_popular']
        overviews = []
        for (var i = 0; i < possibleKeys.length; i++) {
            overviews.push([])
        }
        popularities = []
        data.forEach(function (d) {
            popularities.push(parseFloat(d['popularity']))
        })
        popularities.sort(function (a, b) {
            return a - b
        })
        q1 = popularities[Math.round(popularities.length / 4)]
        q2 = popularities[Math.round(popularities.length / 2)]
        q3 = popularities[Math.round(popularities.length * 3 / 4)]
        data.forEach(function (d) {
            var popularity = parseFloat(d['popularity'])
            if (popularity <= q1) overviews[0].push(d['overview'])
            else if (popularity <= q2) overviews[1].push(d['overview'])
            else if (popularity <= q3) overviews[2].push(d['overview'])
            else overviews[3].push(d['overview'])
        })
    } else {
        console.error('No Aspect Selection!')
        return
    }

    var stack = d3.stack()
        .offset(d3.stackOffsetSilhouette)
        .keys(possibleKeys)

    var layers = stack(selectedData)
    xScaleStreamGraph.domain(d3.extent(selectedData, function (d) { return Date.parse(d['release\_date']) }))
    yScaleStreamGraph.domain([-120, 120])

    var xAxisStreamGraph = d3.axisBottom()
        .scale(xScaleStreamGraph)
    var yAxisStreamGraph = d3.axisLeft()
        .scale(yScaleStreamGraph)

    var area = d3.area()
        .x(function (d) { return xScaleStreamGraph(Date.parse(d.data['release\_date'])) })
        .y0(function (d) { return yScaleStreamGraph(d[0]) })
        .y1(function (d) { return yScaleStreamGraph(d[1]) })

    // Define mouse handlers

    mouseLeaveHandlerStreamGraph = function (d) {
        if (selectedStream != -1) return
        streamGraphSVG.selectAll('path')
            .style('stroke', 'none')
            .transition()
            .duration(500)
            .style('opacity', 1)
        tooltipStreamGraph.innerHTML = "Select a stream to continue!"
    }

    mouseClickHandlerStreamGraph = function (d, i) {

        tooltipStreamGraph.innerHTML = "You have selected " + possibleKeys[i] + " movies!"
        barChartSVG.selectAll('*').remove()
        // pieChartSVG.selectAll("*").remove();
        tagCloudSVG.selectAll("*").remove();
        if (selectedStream != i) {
            selectedStream = i
            streamGraphSVG.selectAll('path')
                .style('stroke', 'none')
                .transition()
                .duration(500)
                .style('opacity', function (d, j) {
                    if (j == i) return 1
                    return 0.3
                })
            d3.select(this)
                .style('stroke', 'black')
            setTimeout("onChangeBarChart(overviews[" + i + "].join())", 500)
        } else {
            selectedStream = -1
            streamGraphSVG.selectAll('path')
                .transition()
                .duration(500)
                .style('opacity', function (d, j) {
                    if (j == i) return 1
                    return 0.6
                })
        }
    }

    mouseOverHandlerStreamGraph = function (d, i) {
        if (selectedStream != -1) return
        streamGraphSVG.selectAll('path')
            .transition()
            .duration(500)
            .style('opacity', function (d, j) {
                if (j == i) return 1
                return 0.6
            })
        tooltipStreamGraph.innerHTML = "You have selected " + possibleKeys[i] + " movies!"
        d3.select(this)
            .style('stroke', 'black')
    }

    streamGraphSVG.selectAll('path').remove()
    streamGraphSVG.selectAll('path')
        .data(layers)
        .enter()
        .append('path')
        .style('fill', function (d) { return zScaleStreamGraph(d.key) })
        .attr('d', area)
        .on('mouseover', mouseOverHandlerStreamGraph)
        .on('mouseleave', mouseLeaveHandlerStreamGraph)
        .on('click', mouseClickHandlerStreamGraph)

    streamGraphSVG.append('g')
        .call(xAxisStreamGraph)
        .attr('transform', 'translate(0, ' + streamGraphInnerHeight + ')')
    streamGraphSVG.append('g')
        .call(yAxisStreamGraph)
}

var tooltip = d3.select("body")
    .append("div")
    .attr("class", "tooltip");

tagCloudSVG = d3.select("#word-cloud-SVG")
    .attr('width', 700)
    .attr('height', 500)

var width = 700;
var height = 500;

var r = Math.min(700, 500) / 2.5,
    color = d3.scaleOrdinal(d3.schemeCategory10),
    wordColor = d3.scaleOrdinal(d3.schemeCategory20)

//third vis

function draw(words, i) {
    tagCloudSVG.append("g")
        .append("text")
        .text(function (d) {
            if (i !== -1) {
                return "This is the tag cloud of the " + " \"" + possibleKeysBarChart[i] + "\"" + " in the movie overview."
            } else {
                return "This is the tag cloud of the all types of words in this segment"
            }

        })
        .attr("x", width / 2)
        .attr("y", 30)
        .attr("text-anchor", "middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", "16px")
        .attr("fill", "black");

    tagCloudSVG.append("g")
        .attr("transform", "translate(" + 350 + "," + 250 + ")")
        .selectAll("text1")
        .data(words)
        .enter().append("text")
        .style("font-size", function (d) { return d.size + "px"; })
        .style("font-family", "Impact")
        .attr("text-anchor", "middle")
        .attr("transform", function (d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .style("fill", function (d, i) { return color(i); })
        .text(function (d) { return d.text; });
}