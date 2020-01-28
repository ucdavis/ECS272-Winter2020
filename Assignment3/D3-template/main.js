(function () {
  // first, load the dataset from a CSV file
  d3.csv('../datasets/globalterrorismdb_0718dist_shortened.csv')
    .then(csv => {
      // log csv in browser console
      console.log(csv);

      var data = csv.map(row => {
        return {
          latitude: Number(row['latitude']),
          longitude: Number(row['longitude'])
        }
      })

      var map_visualization = new MapVisualization(data);
      map_visualization.draw();
    })
})()