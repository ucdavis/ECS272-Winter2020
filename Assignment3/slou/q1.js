var data = null;

var timeStamps = []
var terminals = []
var domesticInternational = ['Domestic', 'International']
var arrivalDeparture = ['Arrival', 'Departure']

var barChartWidth = 700, barChartHeight = 500, barPadding = 5
var barWidth = 0
var barChartSVG = d3.select('#bar-chart')
    .attr('width', barChartWidth)
    .attr('height', barChartHeight)
d3.csv("../datasets/Los_Angeles_International_Airport_-_Passenger_Traffic_By_Terminal.csv").then(grandData => {
    data = grandData

    var timeFormat = d3.timeParse('%m/%d/%y %h:%M:%S %p')
    data.forEach(function(d) {
        // var time = new Date(d['reportperiod'])
        // d['reportperiod'] = time.getFullYear() + '/' + (time.getMonth() + 1)
        d['reportperiod'] = timeFormat(d['reportperiod'])
    })
    console.log(data)

    timeStamps = d3.map(data, function(d) {return d['ReportPeriod']}).keys()

    terminals = d3.map(data, function(d) {return d['Terminal']}).keys()

    init1();
    init2();
})


function init1() {
    d3.select('#slider')
        .attr('max', timeStamps.length - 1)
    barWidth = (barChartWidth / terminals.length);
    // console.log(terminals)
    onChange1();
}

function onChange1() {
    var sliderValue = document.getElementById('slider').value
    var selectedTime = timeStamps[sliderValue]
    document.getElementById('reportperiod').innerHTML = "Passenger Count in " + selectedTime + " for Each Terminal"

    var filteredData1 = new Array(terminals.length).fill(0)
    data.forEach(function (d) {
        if (d['ReportPeriod'] == selectedTime) {
            filteredData1[terminals.indexOf(d['Terminal'])] += parseInt(d['Passenger_Count'])
        }
    })
    // console.log(filteredData1)

    barChartSVG.selectAll("rect")
        .remove();

    var yScale1 = d3.scaleLinear()
        .domain([0, d3.max(filteredData1)])
        .range([0, barChartHeight - 200])

    var xScale1 = d3.scalePoint()
        .domain(terminals)
        .range([barWidth / 2, barChartWidth - barWidth / 2 - barPadding])

    var xAxis1 = d3.axisBottom()
        .scale(xScale1)

    barChartSVG.selectAll("rect")
        .data(filteredData1)
        .enter()
        .append("rect")
        .attr("y", function (d) {
            return barChartHeight - yScale1(d) - 200
        })
        .attr("height", function (d) {
            return yScale1(d)
        })
        .attr("width", barWidth - barPadding)
        .attr("transform", function (d, i) {
            var translate = [barWidth * i, 0];
            return "translate(" + translate + ")";
        });
    barChartSVG.selectAll("text")
        .remove();
    var text = barChartSVG.selectAll("text")
        .data(filteredData1)
        .enter()
        .append("text")
        .text(function (d) {
            if (d < 1000) return d;
            else if (d < 1000000) return (d / 1000).toFixed(0) + 'K';
            else return (d / 1000000).toFixed(0) + 'M';
        })
        .attr("y", function (d) {
            if (barChartHeight - yScale1(d) - 202 < 14) {
                return barChartHeight - yScale1(d) - 182
            } else return barChartHeight - yScale1(d) - 202;
            // return svgHeight - yScale(d) - 22
        })
        .attr("x", function (d, i) {
            return barWidth * (i + 0.2);
        })
        .attr("fill", "#FF0000")

    barChartSVG.selectAll("g")
        .remove()

    var xAxisTranslate = barChartHeight - 200;

    barChartSVG.append("g")
        .attr("transform", "translate(0, " + xAxisTranslate + ")")
        .attr('x', barChartWidth / 2)
        .call(xAxis1)
        .selectAll("text")
        .attr("transform", "translate(-8,30) rotate(-60)")

}