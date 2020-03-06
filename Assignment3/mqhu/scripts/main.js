(function () {

    var legends;
    var sections;
    var center;
    var data;
    var details;
    var uniqueSeen;//unique location
    var uniqueSeenProducer;//uniqueproducer
    var numUnique;
    var numUniqueProducer;//unique Producer
    var source=[];//with all of source year data
    var target=[];
    var newTarget = []; //for all target producer data
    var indexFor1900 =0;
    var indexFor1920 =0;
    var indexFor1940 = 0;
    var indexFor1960 = 0;
    var indexFor1980 = 0;
    var indexFor2000 = 0;

    var seen = [];
    var seenProducer =[];
    const unique = (value, index, self) => {
      return self.indexOf(value) === index
    }

    // first, load the dataset from a CSV file by api
    //SF film location dataset
    d3.csv('https://data.sfgov.org/resource/yitu-d5am.csv')
      .then(csv => {
        csv.forEach(data =>{

          seen.push(data.locations);
          seenProducer.push(data.production_company);
          //transform the datatypt of release year to be number
          data.release_year = Number(data.release_year);
          console.log(data.release_year)
          if((data.release_year <= 1920)&& (data.release_year >= 1900)){
            indexFor1900++;
            source.push(0);
          }else if(data.release_year <=1940){
            indexFor1920++;
            source.push(0);
          }else if(data.release_year <=1960){
            indexFor1940++;
            source.push(1);
          }else if (data.release_year <= 1980) {
            indexFor1960++;
            source.push(1);
          }else if(data.release_year <=2000){
            indexFor1980++;
            source.push(2);
          }else if(data.release_year <=2020){
            indexFor2000++;
            source.push(2);
          }

        })

     //get unique locations
      uniqueSeen = seen.filter(unique)
      numUnique = uniqueSeen.length;
      console.log(uniqueSeen)
      console.log("number of unique location is: "+ numUnique)//from the console we see it is 482

      //get unique producer
      uniqueSeenProducer = seenProducer.filter(unique)
      numUniqueProducer = uniqueSeenProducer.length;
      console.log(uniqueSeenProducer)
      console.log("number of unique location is: "+ numUniqueProducer)//from the console we see it is 67



      var sum = 0;
      sum = indexFor1900 + indexFor1920 + indexFor1940 + indexFor1960 + 
            indexFor1980 + indexFor2000;
      var per1, per2, per3, per4, per5, per6;
      per1 = parseFloat(indexFor1900/sum).toFixed(2) *100;
      per2 = parseFloat(indexFor1920/sum).toFixed(2)*100;
      per3 = parseFloat(indexFor1940/sum).toFixed(2)*100;
      per4 = parseFloat(indexFor1960/sum).toFixed(2)*100;
      per5 = parseFloat(indexFor1980/sum).toFixed(2)*100;
      per6 = parseFloat(indexFor2000/sum).toFixed(2)*100;

      //create data by selecting two columns from csv 
      var data = csv.map(row => {
        return {
          yes: Number(row['Yes Votes']),
          no: Number(row['No Votes']),
          releaseYear :row['loactions']
        }
      })


      /********************************* 
      * Visualization codes start here
      * ********************************/
      var width = 1000;
      var height = 300;
      var margin = {left: 80, right: 20, top: 200, bottom: 60}

      var svg = d3.select('#container')
        .append('svg')
          .attr('width', width + margin.left + margin.right)
          .attr('height', height + margin.top + margin.bottom)
          .style("margin-top", 20)
          .style("margin-left", 30);
           // .style("background", "yellow");


      //create data
      function changeYearGap(){
        details=[{year: "1900-1940", number:indexFor1900+indexFor1920, percentage: (per1+per2).toString()+"%" },
                     {year: "1941-1980", number: indexFor1940+indexFor1960,percentage: (per3+per4).toString()+"%"},
                     {year: "1981-2020", number: indexFor1980+indexFor2000,percentage: (per5+per6).toString()+"%"}
                       ];
        drawPieChart();
      }

      function changeYearGapBack(){
          details = [{year: "1900-1920", number:indexFor1900, percentage: per1.toString()},
                     {year: "1921-1940", number: indexFor1920,percentage: per2.toString()+"%"},
                     {year: "1941-1960", number: indexFor1940,percentage: per3.toString()+"%"},
                     {year: "1961-1980", number: indexFor1960,percentage: per4.toString()+"%"},
                     {year: "1981-2000", number: indexFor1980,percentage: per5.toString()+"%"},
                     {year: "2001-2020", number: indexFor2000,percentage: per6.toString()+"%"}
                     ];
          drawPieChart();
      }
      details = [{year: "1900-1920", number:indexFor1900, percentage: per1.toString()+"%" },
                     {year: "1921-1940", number: indexFor1920,percentage: per2.toString()+"%"},
                     {year: "1941-1960", number: indexFor1940,percentage: per3.toString()+"%"},
                     {year: "1961-1980", number: indexFor1960,percentage: per4.toString()+"%"},
                     {year: "1981-2000", number: indexFor1980,percentage: per5.toString()+"%"},
                     {year: "2001-2020", number: indexFor2000,percentage: per6.toString()+"%"}
                     ];

      var color = d3.scaleOrdinal(['#4daf4a','#377eb8','#ff7f00','#984ea3','#24535f','#f5424e']);
      //arc generator func
      var segment = d3.arc().innerRadius(0)
                            . outerRadius(220)
                            .padAngle(0.05)
                            .padRadius(50);


      drawPieChart();

      function drawPieChart(){

          data = d3.pie().sort(null).value(function(d){return d.number;})
          (details);

          //append title
          svg.append("text")
          .attr("x", 255)             
          .attr("y", 12)
          .attr("text-anchor", "middle")  
          .style("font-size", "16px") 
          .text("Distribution of Release Years of Movies Displayed");

          //for piechart label
          var sectionsPlace = svg.append("g").attr("transform", "translate(250,250)");
          //make retangle box for each reference
          var legendPlace = svg.append("g").attr("transform", "translate(500,220)");

          //for piechart label
          // console.log(details.toString());//print the details
          sections = sectionsPlace.selectAll("path").data(data);
          sections.enter().append("path").attr("d", segment).attr("fill",
          function(d){return color(d.data.number)});

          //for legends
          legends = legendPlace.selectAll(".legends").data(data);
          var legend = legends.enter().append("g").classed("legends",true).
          attr("transform", function(d,i){
            return "translate(0,"+ (i+1)*30 + 
            ")";
          });

          //fill the rectangular box with the same color as that in the pie chart
          legend.append("rect").attr("width",20).attr("height",20).attr("fill",
            function(d){return color(d.data.number)});

          //text elements to display
          legend.append("text").text(function(d){
            return d.data.year;
          })
          .attr("fill", function(d){return d.data.number;})
          .attr("x", 30)
          .attr("y", 15);

          //when click dropdown button, non/number/percentage information shows
          select.addEventListener("mouseup",function(){
          var selectedValue =  select.options[select.selectedIndex].text;
            

          if(selectedValue == "Show Numbers"){
                // console.log(selectedValue);
                d3.select("g").selectAll("text").remove();
                var content = d3.select("g").selectAll("text").data(data);
                content.enter().append("text").each(function(d){
                      center = segment.centroid(d);
                       d3.select(this).attr("x", center[0]).attr("y",center[1])
                                    .text(d.data.number);
                });
          }else if(selectedValue == "Show Percentages"){
              // console.log(selectedValue);
              d3.select("g").selectAll("text").remove();
              var content = d3.select("g").selectAll("text").data(data);
              content.enter().append("text").each(function(d){
              var center = segment.centroid(d);
               d3.select(this).attr("x", center[0]).attr("y",center[1])
                               .text(d.data.percentage);
              });
          }else if(selectedValue == "No Labels"){
            // console.log("does not show parameters");
            d3.select("g").selectAll("text").remove();
          }
          });


          //the second dropdown
          select2.addEventListener("mouseup",function(){
          var selectedValue2 =  select2.options[select2.selectedIndex].text;

          if(selectedValue2 == "Every 40 Years"){
            //remove all svg elements
            svg.selectAll("*").remove();
            changeYearGap();
          }else if(selectedValue2 == "Every 20 Years"){
            //remove all svg elements
            svg.selectAll("*").remove();
            changeYearGapBack();
          }
        })

      }

    })
  



      /********************************* 
      * Second visualization codes start here
      * ********************************/


    function addElement () { 
              var div = document.getElementById( 'rightMove' );
              var newDiv = document.createElement("div"); 
              newDiv.setAttribute("id", "secondVisualization");
              div.parentNode.insertBefore( newDiv, div.nextSibling );
    }
    addElement();

    sencondVis(4);
    function sencondVis(paddingSize){
      console.log(" function called")
      // set the dimensions and margins of the vis
    var margin = {top: 10, right: 10, bottom: 10, left: 10},
        width = 1200 - margin.left - margin.right,
        height = 900 - margin.top - margin.bottom;


    // append the svg object to the body of the page
    var svg2 = d3.select("#secondVisualization").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // Color scale
    var color = d3.scaleOrdinal(d3.schemeCategory20);

    // Set the sankey diagram properties
    var sankey = d3.sankey()
        .nodeWidth(30)
        .nodePadding(paddingSize)
        .size([width, height]);


    d3.json("https://data.sfgov.org/resource/yitu-d5am.json").then(newcsv => 
    {
      let jsonForProducer = {
      };
      for(var m = 3; m<70;m++){
        jsonForProducer[m-3] = ({ "node": m , "name": uniqueSeenProducer[m-3]});
      }
      // console.log(JSON.stringify(jsonForProducer));

      //construct our own json here
      let graph = {
        "nodes":[],
        "links":[]
      };
      graph.nodes.push({
        "node": 0,
        "name": "1900-1940"
      });
      graph.nodes.push({
        "node": 1,
        "name": "1941-1980"
      });
      graph.nodes.push({
        "node": 2,
        "name": "1981-2020"
      });
      for(m =3; m< 70;m++){
        graph.nodes.push({
          "node": m,
          "name": jsonForProducer[m-3].name
        })
      }

    console.log(Object.keys(jsonForProducer).length);
      function getIndex (name) {
       for (var i = 0; i < Object.keys(jsonForProducer).length; i++) {
        if (jsonForProducer[i].name == name) {
          return i;
        }
       }
       return -1;
     }
    for(m = 0; m<1000; m++){
            var indexForJSON= getIndex(newcsv[m].production_company);
            console.log(indexForJSON);
            if((newcsv[m].release_year <= 1940)&& (newcsv[m].release_year >= 1900)){
              graph.links.push({
                "source": 0,
                "target": jsonForProducer[indexForJSON].node,
                "value":1
              })
            }else if(newcsv[m].release_year <=1980){
              graph.links.push({
                "source": 1,
                "target": jsonForProducer[indexForJSON].node,
                "value": 1
              })
            }
             else if(newcsv[m].release_year <=2020){
              graph.links.push({
                "source": 2,
                "target": jsonForProducer[indexForJSON].node,
                "value":1
              })
            }
    }
    // console.log(JSON.stringify(graph))

    // Constructs a new Sankey generator with the default settings.
    sankey.nodes(graph.nodes)
          .links(graph.links)
          .layout(2);


    select3.addEventListener("mouseup",function(){
              var selectedValue3 =  select3.options[select3.selectedIndex].text;

              if(selectedValue3 == "Medium"){
                document.getElementById("secondVisualization").remove();
                console.log("previous vis deleted")

                addElement();//create a new div for second vis
                sencondVis(8);
              }
               else if(selectedValue3 == "Large"){

                document.getElementById("secondVisualization").remove();
                console.log("vis 2 deleted")

                addElement();//create a new div for second vis
                sencondVis(11);
              }
              else if(selectedValue3 == "Small"){
                //back to small padding

                document.getElementById("secondVisualization").remove();
                console.log("vis 3 deleted")

                addElement();//create a new div for second vis
                sencondVis(4);
              }
      });


      //move node func
      function nodeMove(d) {
        d3.select(this)
          .attr("transform",
                "translate("
                   + d.x + ","+ (d.y = Math.max(
                      0, Math.min(height - d.dy, d3.event.y))
                     ) + ")");
        sankey.relayout();
        link.attr("d", sankey.link() );
      }


      // add in the links
      var link = svg2.append("g")
        .selectAll(".link")
        .data(graph.links)
        .enter()
        .append("path")
          .attr("class", "link")
          .attr("d", sankey.link() )
          .style("stroke-width", function(d) { return Math.max(1, d.dy); })
          .sort(function(a, b) { return b.dy - a.dy; });

      // add in the nodes
      var node = svg2.append("g")
        .selectAll(".node")
        .data(graph.nodes)
        .enter().append("g")
          .attr("class", "node")
          .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
          .call(d3.drag()
            .subject(function(d) { 
                return d; 
              })
            .on("start", function() { 
                this.parentNode.appendChild(this); 
              })
            .on("drag", nodeMove));

      // add title
      node.append("text")
            .attr("x", 0)
            .attr("y", function(d) {
               return d.dy / 2; 
             })
            .attr("dy", ".35em")
            .attr("text-anchor", "end")
            .style("color", "red")
            .attr("transform", null)
            .text(function(d) { 
                return d.name; 
            })
          .filter(function(d) { 
              return d.x < width / 2; 
            })
            .attr("x", 10+ sankey.nodeWidth())
            .attr("text-anchor", "start");

      // rectang box
      node.append("rect")
          .attr("height", function(d) { return d.dy; })
          .attr("width", sankey.nodeWidth())
          .style("fill", function(d) {
            return d.color = color(d.name.replace(/ .*/, "")); 
         })
          .style("stroke", function(d) {
             return d3.rgb(d.color).darker(2); 
           })
            // Add hover text
            .append("title")
            .text(function(d) { return d.name + "\n" + "There are " +d.value+ " movies on this node"; });


    });

  }


})()



