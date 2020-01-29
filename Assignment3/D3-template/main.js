(function () {
  // first, load the dataset from a CSV file
  d3.csv('../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv')
    .then(csv => {
      // log csv in browser console
      console.log(csv);

      var data = csv.map(row => {
        return {
          latitude: Number(row['Y']),
          longitude: Number(row['X'])
        }
      })





      var map_visualization = new MapVisualization(data);
      map_visualization.draw();
    })
})()