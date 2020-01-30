const pieChart = (selector, data) => {
  const size = 500;
  const fourth = size / 4;
  const half = size / 2;
  const labelOffset = fourth * 1.4;
  const total = data.reduce((acc, cur) => acc + cur.value, 0);
  const container = d3.select(selector);
  
  const chart = container.append('svg')
    .style('width', '100%')
    .attr('viewBox', `0 0 ${size} ${size}`);
  
  const plotArea = chart.append('g')
    .attr('transform', `translate(${half}, ${half})`);
  
  const color = d3.scaleOrdinal()
    .domain(data.map(d => d.name))
    .range(d3.schemeCategory10);

  const pie = d3.pie()
    .sort(null)
    .value(d => d.value);
  
  const arcs = pie(data);
  
  const arc = d3.arc()
    .innerRadius(0)
    .outerRadius(fourth);
  
  const arcLabel = d3.arc()
    .innerRadius(labelOffset)
    .outerRadius(labelOffset);
  
  plotArea.selectAll('path')
    .data(arcs)
    .enter()
    .append('path')
    .attr('fill', d => color(d.data.name))
    .attr('stroke', 'white')
    .attr('d', arc);
  
  const labels = plotArea.selectAll('text')
    .data(arcs)
    .enter()
    .append('text')
    .style('text-anchor', 'middle')
    .style('alignment-baseline', 'middle')
    .style('font-size', '20px')
    .attr('transform', d => `translate(${arcLabel.centroid(d)})`)
    
  labels.append('tspan')
    .attr('y', '-0.6em')
    .attr('x', 0)
    .style('font-weight', 'bold')
    .text(d => `${d.data.name}`);
  
  labels.append('tspan')
    .attr('y', '0.6em')
    .attr('x', 0)
    .text(d => `${d.data.value} (${Math.round(d.data.value / total * 100)}%)`);
};

pieChart('#chart', [
  { name: 'Option A', value: 107 },
  { name: 'Option B', value: 31 },
  { name: 'Option C', value: 635 },
]);