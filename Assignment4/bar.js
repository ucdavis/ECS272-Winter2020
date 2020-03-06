// Config of bar chart

var barChartMargin = { top: 10, right: 10, bottom: 40, left: 60 }
var barChartWidth = 400
var barChartHeight = 250
var barPadding = 5
var barChartInnerWidth, barChartInnerHeight, barWidth

var barChartSVG = null

var possibleKeysBarChart = ['topics', 'nouns', 'dates', 'people', 'verbs', 'acronyms']

var selectedBar = -1

var tip = d3.select("#bar-chart")
    .append("div")
    .attr("class", "tip")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden");

function initBarChart() {
    // pieChartSVG.selectAll("*").remove();
    // removePieChartElement();

    barChartInnerWidth = barChartWidth - barChartMargin.left - barChartMargin.right
    barChartInnerHeight = barChartHeight - barChartMargin.top - barChartMargin.bottom
    barWidth = (barChartInnerWidth / possibleKeysBarChart.length)

    barChartSVG = d3.select('#bar-chart-SVG')
        .attr("width", barChartWidth)
        .attr("height", barChartHeight)
        .append('g')
        .attr("transform",
            "translate(" + barChartMargin.left + ", " + barChartMargin.top + ")")

}

// function removePieChartElement(){
//     var Piediv = document.getElementById('pie-chart');
//      Piediv.remove();  
// }

function onChangeBarChart(text) {
    // pieChartSVG.selectAll("*").remove();
    // removePieChartElement();

    selectedBar = -1
    document.getElementById("tooltip-bar-chart").innerHTML = "Touch a bar to see the quantity!"
    barChartSVG.selectAll('*')
        .remove()
    tagCloudSVG.selectAll("*")
        .remove();

    // NLP
    // if (text.length > 30000) {
    //     text = text.substring(0, 30000);
    // }

    var NLP = nlp(text)
    topics = NLP.topics().out("frequency");
    nouns = NLP.nouns().out("frequency");
    dates = NLP.dates().out("frequency");
    people = NLP.people().out("frequency");
    verbs = NLP.verbs().out("frequency");
    acronyms = NLP.acronyms().out("frequency");

    wholeWords = topics.concat(nouns, dates, people, verbs, acronyms);
    wholeWords.sort(function (a, b) {
        return (a.count > b.count) ? -1 : 1
    })

    var barChartData = [
        d3.sum(topics, function (d) { return d.count }),
        d3.sum(nouns, function (d) { return d.count }),
        d3.sum(dates, function (d) { return d.count }),
        d3.sum(people, function (d) { return d.count }),
        d3.sum(verbs, function (d) { return d.count }),
        d3.sum(acronyms, function (d) { return d.count })
    ]
    var terms = [topics, nouns, dates, people, verbs, acronyms]
    var yScaleBarChart = d3.scaleLinear()
        .domain([0, d3.max(barChartData)])
        .range([0, barChartInnerHeight])

    var xScaleBarChart = d3.scalePoint()
        .domain(possibleKeysBarChart)
        .range([barWidth / 2, barChartInnerWidth - barWidth / 2 - barPadding])

    var xAxisBarChart = d3.axisBottom()
        .scale(xScaleBarChart)

    var yAxisBarChart = d3.axisLeft()
        .scale(d3.scaleLinear().domain([0, d3.max(barChartData)]).range([barChartInnerHeight, 0]))

    //set the layout for the initial tag cloud
    layout = d3.layout.cloud()
        .size([700, 400])
        .words(wholeWords.slice(0, 100).map(function (d) { return { text: d.normal, size: 5 * Math.log(d.count) + 0.5 * d.count }; }))
        .padding(2)
        .font("Impact")
        .fontSize(function (d) { return d.size; })
        .on("end", function (d) { draw(d, -1) })
        .start();


    var mouseOverHandlerBarChart = function (d, i) {

        if (selectedBar != -1) return
        d3.select(this)
            .style('opacity', '0.7')


        document.getElementById("tooltip-bar-chart").innerHTML = "<font color=\"red\">There are " + barChartData[i] + ' ' + possibleKeysBarChart[i] + ' in the chosen subset.</font>'
    }

    var mouseClickHandlerBarChart = function (d, i) {
        tagCloudSVG.selectAll("*").remove();
        document.getElementById("tooltip-bar-chart").innerHTML = "<font color=\"red\">There are " + barChartData[i] + ' ' + possibleKeysBarChart[i] + ' in the chosen subset.</font>'
        if (selectedBar != i) {
            selectedBar = i
            barChartSVG.selectAll("rect")
                .style('stroke', 'none')
                .style('opacity', '1')
            d3.select(this)
                .style('stroke', 'yellow')
                .style('opacity', '0.7')

            //set layout corresponding tagcloud
            layout = d3.layout.cloud()
                .size([700, 400])
                .words(terms[i].slice(0, 100).map(function (d) { return { text: d.normal, size: 5 * Math.log(d.count) + 1 * d.count }; }))
                .padding(2)
                .font("Impact")
                .fontSize(function (d) { return d.size; })
                .on("end", function (d) { draw(d, i) })
                .start();
        } else {
            selectedBar = -1
            d3.select(this)
                .style('stroke', 'none')
            // resume the initial tagcloud
            layout = d3.layout.cloud()
                .size([700, 400])
                .words(wholeWords.slice(0, 100).map(function (d) { return { text: d.normal, size: 5 * Math.log(d.count) + 0.5 * d.count }; }))
                .padding(2)
                .font("Impact")
                .fontSize(function (d) { return d.size; })
                .on("end", function (d) { draw(d, -1) })
                .start();
        }
    }

    var mouseLeaveHandlerBarChart = function (d, i) {
        if (selectedBar != -1) return
        barChartSVG.selectAll("rect")
            .style('opacity', '1')
        document.getElementById("tooltip-bar-chart").innerHTML = "Touch a bar to see the quantity!"
    }

    barChartSVG.selectAll("rect")
        .data(barChartData)
        .enter()
        .append("rect")
        .attr("y", function (d) {
            return barChartInnerHeight - yScaleBarChart(d)
        })
        .attr("height", function (d) {
            return yScaleBarChart(d)
        })
        .attr("width", barWidth - barPadding)
        .attr("fill", "#0080FF")
        .attr("x", function (d, i) {
            return barWidth * i
        })
        .on("mouseover", mouseOverHandlerBarChart)
        .on("mouseleave", mouseLeaveHandlerBarChart)
        .on("click", mouseClickHandlerBarChart)

    barChartSVG.append('g')
        .attr('transform', 'translate(0, ' + barChartInnerHeight + ')')
        .call(xAxisBarChart)

    barChartSVG.append('g')
        .call(yAxisBarChart)
}