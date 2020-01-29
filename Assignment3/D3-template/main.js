//load the dataset from a CSV file
d3.csv('../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv')
  .then(csv => {
    var map_visualization = new MapVisualization(csv);
  })

function 