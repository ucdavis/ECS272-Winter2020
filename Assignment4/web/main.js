var data = null
var example_vis = null
var alluvial_vis = null

// This is the entry point of the app
d3.csv('../dataset/student-mat.csv')
  .then(csv => {
    // log csv in browser console
    console.log(csv)

    // Set data items
    data = csv

    // Create appropriate dimensions and init the charts
    var example_vis_dimensions = {
      width: 600,
      height: 500,
      margin: {left: 150, right: 20, top: 20, bottom: 270}
    }

    var alluvial_vis_dimensions = {
      width: 600,
      height: 500,
      margin: {left: 150, right: 20, top: 50, bottom: 270}
    }

    //example_vis = new ExampleVis(data, '#example-vis-container', example_vis_dimensions)
    alluvial_vis = new AlluvialVis(data, '#alluvial-vis-container', alluvial_vis_dimensions)
  })