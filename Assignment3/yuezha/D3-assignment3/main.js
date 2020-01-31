(function(){
  d3.csv('../datasets/LAX_Terminal_Passengers.csv')
    .then(csv=>{
      console.log(csv);
      
      var terminalsData=csv.map(function(d){
        return {
          terminal: d.Terminal,
          arrivalDeparture: d.Arrival_Departure,
          year: d.ReportPeriod.substring(6,10),
          passengerCount: d.Passenger_Count
        }
      });

      var terminalsAndYearsData=d3.nest()
      .key(function(d){
        return d.terminal;
      })
      .key(function(d){
        return d.year;
      })
      .rollup(function(d){
        return {totalPassenger: d3.sum(d, function(e){
          return e.passengerCount;
        })}
      })
      .entries(terminalsData);

      var data_cod=[];

      terminalsAndYearsData.forEach(function(d){
        obj={
          terminal:d.key
        }
        d.values.forEach(function(e){
          obj[e.key]=e.value
        })
        data_cod.push(obj);
      })

      console.log(data_cod)

      var width=1200;
      var height=400;
      var margin={left: 60, right:20, top:20, bottom:90};



      //Parallel Coordinates graph 
      dimensions=d3.keys(data_cod[1])
      dimensions.unshift(dimensions.pop())
      //.filter(function(d){ return d!='terminal'});
      var y={}

      for (i in dimensions){
        if (dimensions[i]!='terminal'){
          name=dimensions[i]
          y[name]=d3.scaleLinear()
          .domain([0, d3.max(data_cod, function(e){
            if(dimensions[i] in  e)
            return e[dimensions[i]]['totalPassenger'];
            e[dimensions[i]]={
              totalPassenger: 0
            };
          })])
          .range([height, 0])
        }
      }
      
      terminal_name=["Imperial Terminal", "Misc. Terminal", "Terminal 1", "Terminal 2", "Terminal 3", "Terminal 4", "Terminal 5", "Terminal 6", "Terminal 7", "Terminal 8", "Tom Bradley International Terminal"];
      y['terminal']=d3.scaleBand().rangeRound([0, height])
      .domain(terminal_name);

      x=d3.scalePoint()
      .range([0, width])
      .padding(1)
      .domain(dimensions);

      console.log(y)

      function path(d){
        return d3.line()(dimensions.map(function(p){
          if(p=='terminal')
            return [x(p), y[p](d[p])];
          else
            return [x(p), y[p](d[p]['totalPassenger'])];
        }));
      }

      var svg_cod=d3.select('#container').append('svg')
      .attr('width', width+margin.left+margin.right)
      .attr('height', height+margin.top+margin.bottom)
      .append('g')
      .attr('transform', 'translate('+margin.left+','+margin.top+')');

      svg_cod.selectAll('myPath')
      .data(data_cod)
      .enter().append('path')
      .attr('d', path)
      .style('fill', 'none')
      .style('stroke', '#69b3a2')
      .style('opacity', '0.8')


      svg_cod.selectAll('myAxis')
      .data(dimensions).enter()
      .append('g')
      .attr('transform', function(d){return 'translate('+x(d)+')';})
      .each(function(d){
        d3.select(this).call(d3.axisLeft().ticks(6).scale(y[d])).style('font-size', 7);
      })
      .append('text')
      .style('text-anchor', 'middle')
      .attr('y', height+15)
      .text(function(d) {return d})
      .style('fill', 'black').style('font-size', 10)




      //bar chart
      dimensions.shift()
      var svg_bar=d3.select('#container').append('svg')
      .attr('width', width+margin.left+margin.right)
      .attr('height', height+margin.top+margin.bottom)
      .append('g')
      .attr('transform', 'translate('+2*margin.left+','+margin.top+')');
     

      data_bar=[]
      data_cod.forEach(function(d){
        var obj={
          terminal: d.terminal}
        obj.totalPassenger=0
        for (i in dimensions)
          obj.totalPassenger+=d[dimensions[i]]['totalPassenger'];
        data_bar.push(obj);
      })


      x_bar=d3.scaleBand()
      .rangeRound([0, width-margin.left-margin.right])
      .padding(0.1)
      .domain(data_bar.map(function(d){return d.terminal}));

      y_bar=d3.scaleLinear()
      .rangeRound([height, 0])
      .domain([0, d3.max(data_bar, function(d){return d.totalPassenger})])

      console.log(data_bar)

      svg_bar.selectAll('myBar')
      .data(data_bar)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('fill', 'steelblue')
      .attr('x', d=>x_bar(d.terminal))
      .attr('y', d=>y_bar(d.totalPassenger))
      .attr('width', x_bar.bandwidth())
      .attr('height', function(d){return height-y_bar(d.totalPassenger)});


      svg_bar.append('g')
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x_bar))
      .selectAll('text')
      .attr("y", 0)
      .attr("x", 9)
      .attr("dx", "-10")
      .attr('dy', '20')
      .attr("transform", "rotate(45)")
      .style("text-anchor", "start");


      svg_bar.append('g')
      .call(d3.axisLeft(y_bar))
      .append('text')
      .attr('y', 6)
      .attr("fill", "black")
      .attr("transform", "rotate(-90)")
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")
      .text("Passenger Count From 2006 to 2019");
      
    })

})()