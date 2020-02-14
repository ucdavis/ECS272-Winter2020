var hist_choices = ["G1", "G2", "G3", "age", "absences"]
var key = hist_choices[0]
var setting = {
  key: key,
  x_domain: {min: 0, max: 22},
  x_ticks: 80,
  x_axis: key.charAt(0).toUpperCase() + key.slice(1)
}

function OnScatterVisSelectionChanged(value) {
    scatter_vis.color_by = value

    scatter_vis.update(null)
    //scatter_vis.init()
}

function OnSanKeyVisSelectionChanged(value, id) {
    var selects = document.getElementsByClassName('sankey-select');

    var columns = []
    for(const select of selects) {
        if (select.value === "none")
            continue

        if (columns.indexOf(select.value) >= 0) {
            this.value = 'none'
            return
        }
        columns.push(select.value)
    }

    alluvial_vis.columns = columns
    alluvial_vis.init()
}

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
    hist_vis.updateDropdown(setting, true)

  } else {
  //else, we are gonna update a barchart
    hist_vis.updateDropdown(setting, false)

  }

}
