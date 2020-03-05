var complexChart = null
var simpleChart = null
var csv_data = null
var current_data = null
var min_year = null
var max_year = null
var current_year = null

// This is the entry point of the app
d3.csv('../datasets/LAX_Terminal_Passengers.csv')
  .then(csv => {
    // log csv in browser console
    console.log(csv)

    // Set data items
    csv_data = csv
    current_data = csv

    // Calculate year range
    min_year = d3.min(csv, d => {
      return new Date(d.ReportPeriod).getFullYear()
    })
    max_year = d3.max(csv, d => {
      return new Date(d.ReportPeriod).getFullYear()
    })

    // Calculate mid year
    current_year = min_year + Math.round((max_year - min_year) * 0.5)

    // Set range limits
    var range = document.getElementById("year_range")
    range.min = min_year
    range.max = max_year
    range.value = current_year

    // Set labels
    d3.select("#min_year").text(min_year)
    d3.select("#max_year").text(max_year)
    d3.select("#current_year").text("Passengers in " + current_year)
    d3.select("#current_flight_type").text("All Flights")

    // Filter data for bar chart
    var filtered_data = filterYear(current_data, current_year)

    // Create appropriate dimensions and init the charts
    var complexChartDimensions = {
      width: 1200,
      height: 500,
      margin: {left: 150, right: 20, top: 20, bottom: 60}
    }

    var simpleChartDimensions = {
      width: 600,
      height: 500,
      margin: {left: 150, right: 20, top: 20, bottom: 270}
    }

    complexChart = new ComplexChart(current_data, '#container-complex', complexChartDimensions)
    simpleChart = new SimpleChart(filtered_data, '#container-simple', simpleChartDimensions)
  })


function onComplexChartSelectionChanged(value) {
  if (complexChart == null || current_data == null)
    return

  console.log("Switching primary view to: " + value)
  d3.select("#current_flight_type").text(value + " Flights")

  if (value == "All") {
    current_data = csv_data
  } else {
    current_data = filterDomesticInternational(csv_data, value == "International")
  }

  complexChart.updateChart(current_data)
  var filtered_data = filterYear(current_data, current_year)
  simpleChart.updateChart(filtered_data)
}

function onSimpleChartSelectionChanged(value) {
  if (simpleChart == null || current_data == null)
    return

  console.log("Switching secondary view to year: " + value)

  current_year = value
  d3.select("#current_year").text("Passengers in " + current_year)

  var filtered_data = filterYear(current_data, current_year)
  simpleChart.updateChart(filtered_data)
}

function filterDomesticInternational(data, isInternational) {
  return data.filter(d => {
    return d.Domestic_International == (isInternational ? "International" : "Domestic")
  })
}

function filterYear(data, year) {
  return data.filter(d => {
    return new Date(d.ReportPeriod).getFullYear() == year;
  })
}
