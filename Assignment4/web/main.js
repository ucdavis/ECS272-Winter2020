var data = null
var example_vis = null
var scatter_vis = null

// This is the entry point of the app
d3.csv('../dataset/student-mat.csv')
  .then(csv => {
    // log csv in browser console
    console.log(csv)

    // Set data items
    data = csv

    example_vis = new ExampleVis(data, '#example-vis-container', example_vis_dimensions)
    scatter_vis = new ScatterVis(data, '#scatter-vis-container', scatter_vis_dimensions)
  })