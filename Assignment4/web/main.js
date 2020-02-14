var eventbus = new EventBus()

var data = null
var hist_vis = null
var scatter_vis = null
var alluvial_vis = null

// This is the entry point of the app
d3.csv('../dataset/student-mat.csv')
  .then(csv => {
    // log csv in browser console
    console.log(csv)

    // Set data items
    data = csv

    //change to the input as hist_vis
    hist_vis = new Histogram(data,'#hist-vis', hist_vis_dimensions, setting);
    alluvial_vis = new AlluvialVis(data, '#alluvial-vis-container', alluvial_vis_dimensions)
    scatter_vis = new ScatterVis(data, '#scatter-vis-container', scatter_vis_dimensions)
  })
