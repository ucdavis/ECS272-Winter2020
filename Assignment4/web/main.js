var eventbus = new EventBus()

var data = null
var hist_choices = ["G1", "G2", "G3", "age", "absences"]
var key = hist_choices[0]
var setting = {
  key: key,
  x_domain: {min: 0, max: 22},
  x_ticks: 80,
  x_axis: key.charAt(0).toUpperCase() + key.slice(1)
}

var example_vis = null
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
    hist_vis = new Histogram(data, null,'#hist-vis', hist_vis_dimensions, setting);
    alluvial_vis = new AlluvialVis(data, '#alluvial-vis-container', alluvial_vis_dimensions)
    scatter_vis = new ScatterVis(data, '#scatter-vis-container', scatter_vis_dimensions)
  })

function ThirdDropdownChange(value){
  setting.key = value
  setting.x_axis = value.charAt(0).toUpperCase() + value.slice(1)
  //If we are gonna update a histogram
  if(hist_choices.includes(value)){
    //Adjust domain
    setting.x_domain.min = 0
    setting.x_domain.max = 22
    if (value == "age") {
      setting.x_domain.min = 10
      setting.x_domain.max = 25
    } else if (value == "absences"){
      setting.x_domain.max = 80
    }

    hist_vis.update(data, null, setting, true)

  } else {
  //else, we are gonna update a barchart

    hist_vis.update(data, null, setting, false)

  }

}
