//Data of interest Category, PdDistrict, Date
var margin_new = {top: 30, right: 40, bottom: 150, left: 100};
var width_new = 760 - margin_new.left - margin_new.right;
var height_new = 660 - margin_new.top - margin_new.bottom;
var parser = d3.timeParse('%m/%d/%Y %h:%M:%S %p');
var allDates = [];
var allCategory = [];
var allPd = [];
var catData = [];
var pdData = [];
var color_new = d3.scaleOrdinal(d3.schemeCategory10);
var svg_new = null;
//var view = null;
var renderData;
var renderKey;
var pallet;
var count;
var tooltip = d3.select("body").append("div").attr("class", "toolTip");

(function () {
d3.csv('../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv')
    .then(data_new => {
      // log csv in browser console
      //console.log(csv);
    
      //data_new.forEach(function(d){
          //d['Date']=parser(d['Date'])
      //})
//console.log(data_new) good
allDates = d3.map(data_new,function(d){
    return d['DayOfWeek']
}).keys()
//console.log(allDates) good
    
allCategory = d3.map(data_new,function(d){
    return d['Category']
}).keys()
//console.log(allCategory)
    
allPd = d3.map(data_new,function(d){
    return d['PdDistrict']
}).keys()
//console.log(allPd)

/*// append the svg object to the body of the page
var svg_new = d3.select("#streamGraph")
    .append("svg")
    .attr("width", width_new + margin_new.left + margin_new.right)
    .attr("height", height_new + margin_new.top + margin_new.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin_new.left + "," + margin_new.top + ")");

var view = svg_new.append("g")
.attr("transform", "translate(" + margin_new.left + "," + margin_new.top + ")");*/

//group by category then count each category
var catCount=d3.nest()
.key(function(d){return d['Date'];})
.key(function(d){return d['Category'];})
.rollup(function(v){return v.length;})
.entries(data_new)
//console.log(catCount);   

//group by PdDistrict then count each district
var pdCount=d3.nest()
.key(function(d){return d['Date']})
.key(function(d){return d['PdDistrict'];})
.rollup(function(v){return v.length;})
.entries(data_new)
//console.log(pdCount);

//sort by occurance
catCount.sort(function(b,a){
  return a.value-b.value;
});
pdCount.sort(function(b,a){
  return a.value-b.value;
});

//reformat all data: catData
catCount.forEach(function(d){
    var a = new Array(allCategory.length+1).fill(0)
    a[0]=d.key
    d.values.forEach(function(v){
        a[allCategory.indexOf(v.key)+1]=v.value
    })
    var b = {};
    b['Date']=a[0]
    for(var i=1;i<a.length;i++){
        b[allCategory[i-1]]=a[i]
    }
    catData.push(b)
})
//console.log(catData); 
    
//reformat all data: pdData
pdCount.forEach(function(d){
    var a = new Array(allPd.length+1).fill(0)
    a[0]=d.key
    d.values.forEach(function(v){
        a[allPd.indexOf(v.key)+1]=v.value
    })
    var b = {};
    b['Date']=a[0]
    for(var i=1;i<a.length;i++){
        b[allPd[i-1]]=a[i]
    }
    pdData.push(b)
})
 //console.log(pdData); 
})

myFunction2();
})()


function myFunction2(){
//update 
// append the svg object to the body of the page
console.warn("hey im in function2");
    
    var selectTypeVal = document.getElementById("selectType").value;
    console.log(selectTypeVal);
    if(selectTypeVal=="Category"){
        svg_new.selectAll('path').remove();
        count=count+1;
        if(count>0){
        document.getElementById("streamGraph").remove();
        }
        console.warn("hey im in rendercat");
        renderData = catData
        renderKey = allCategory
        pallet = d3.scaleOrdinal()
        .domain(renderKey)
        .range(['#fff7ab','#ece2f0','#d0d1e6','#a6bddb','#67a9cf','#3690c0','#02818a','#016c59','#014636','#fff5f0','#fee0d2','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#a50f15','#67000d','#f7ecfd','#e0ece8','#bfd3e6','#9ebcda','#8c96c6','#8c6bb1','#88419d','#810f7c','#4d004b','#000000'])
        
    }
    else if (selectTypeVal=="PdDistrict"){
        svg_new.selectAll('path').remove();
        count=count+1;
        if(count>0){
        document.getElementById("streamGraph").remove();
        }
        console.warn("hey im in renderpd");
        renderData = pdData
        renderKey = allPd
        pallet = d3.scaleOrdinal()
    .domain(renderKey)
    .range(['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red','pink','#ece7f2','#9ebcda','#02818a'])
    }
    else{
        console.warn("This should not be happening!!!!!");
        renderData = pdData
        renderKey = allPd
        pallet = d3.scaleOrdinal()
    .domain(renderKey)
    .range(['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red','pink','#ece7f2','#9ebcda','#02818a'])
    }

svg_new = d3.select("#streamGraph")
    .attr("width", width_new + margin_new.left + margin_new.right)
    .attr("height", height_new + margin_new.top + margin_new.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin_new.left + "," + margin_new.top + ")");

view = svg_new.append("g")
.attr("transform", "translate(" + margin_new.left + "," + margin_new.top + ")");
 
var over = function(d,i){
    svg_new.selectAll('path')
    .transition().duration(100).attr("opacity",function(d,j){
        return j != i ? 0.2 : 1;
    })
    d3.select(this).style('stroke','black')
    tooltip
          .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html("You are looking at type: "+ "<br>" + (d.key) + "<br>" );
}

var leave = function(d){
    svg_new.selectAll('path')
        .transition().duration(100).attr('opacity',1).style('stroke','none')
}
    
var xlen = d3.scaleTime()
    .domain(d3.extent(renderData, function(d) {return Date.parse(d.Date)}))
    .range([0, width_new])
    
var ylen = d3.scaleLinear()
    .domain([-300,300])
    .range([height_new, 0]);
    
var stack = d3.stack()
    .offset(d3.stackOffsetSilhouette)
    .keys(renderKey)
    (renderData)

svg_new.selectAll('path').remove();

svg_new.selectAll('path')
    .data(stack)
    .enter()
    .append('path')
        .style('fill', function(d) {return pallet(d.key)})
        .on('mouseover',over)
        .on('mouseleave',leave)
        .attr('d', d3.area()
              .x(function(d) {return xlen(new Date(d.data.Date))})
              .y0(function(d) {return ylen(d[0])})
              .y1(function(d) {return ylen(d[1])})
              .curve(d3.curveMonotoneX)
              //.curve(d3.curveBasis)
             )

svg_new.append("g")
    .attr("transform", "translate(0," + height_new + ")")
    .call(d3.axisBottom(xlen).ticks(12));
    
svg_new.append("g")
    .call(d3.axisLeft(ylen))
}