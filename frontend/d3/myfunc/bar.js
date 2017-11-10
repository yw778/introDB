
var drawBarChart_time = function(id,data,w,h,tickformatDate){
	
	var margin = {top: 20, right: 20, bottom: 100, left: 40},
    width = w - margin.left - margin.right,
    height = h - margin.top - margin.bottom;
	
	//var tickformatDate = d3.time.format("%Y-%m-%d %H");
	
	var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);
	
	var y = d3.scale.linear()
	    .range([height, 0]);
	
	var xAxis = d3.svg.axis()
    	.scale(x)
    	.orient("bottom")
    	.tickFormat(tickformatDate);
	
	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left")
	    .ticks(10);
	
	x.domain(data.map(function(d) { return d.date; }));
	y.domain([0, d3.max(data, function(d) { return d.num; })]);
	
	var svg = d3.select(id).append("svg")
		.attr("id", "barchart")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	
	svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
  .selectAll("text")
    .style("text-anchor", "end")
    .attr("dx", "-.8em")
    .attr("dy", "-.55em")
    .attr("transform", "rotate(-90)" );

	svg.append("g")
	    .attr("class", "y axis")
	    .call(yAxis)
	  .append("text")
	    .attr("transform", "rotate(-90)")
	    .attr("y", 6)
	    .attr("dy", ".71em")
	    .style("text-anchor", "end")
	    .text("Number");
	
	svg.selectAll(".bar")
	    .data(data)
	  .enter().append("rect")
	    .attr("class", "bar")
	    .attr("x", function(d) { return x(d.date); })
	    .attr("width", x.rangeBand())
	    .attr("y", function(d) { return y(d.num); })
	    .attr("height", function(d) { return height - y(d.num); });
};


var drawBar_general = function(id,data,w,h, xlabelName, ylabelName){
	
	var tip = d3.tip()
	  .attr('class', 'd3-tip')
	  .offset([-10, 0])
	  .html(function(d) {
	    return "<span style='color:white'>" + d.value + "</span>";
	  });
	
	var margin = {top: 20, right: 20, bottom: 100, left: 40},
    width = w - margin.left - margin.right,
    height = h - margin.top - margin.bottom;
	
	//var tickformatDate = d3.time.format("%Y-%m-%d %H");
	
	var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);
	
	var y = d3.scale.linear()
	    .range([height, 0]);
	
	var xAxis = d3.svg.axis()
    	.scale(x)
    	.orient("bottom");
	
	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left")
	    .ticks(10);
	
	x.domain(data.map(function(d) { return d.name; }));
	y.domain([0, d3.max(data, function(d) { return d.value; })]);
	
	var svg = d3.select(id).append("svg")
		.attr("id", "barchart")
	    .attr("width", w)
	    .attr("height", h)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	svg.call(tip);
	svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(20," + height + ")")
    .call(xAxis)
    .append("text")
	    .attr("transform", "translate(" + (w/2-margin.left) + "," + (30) + ")")
	    .attr("dx", "0em")
	    .attr("dy", "0.8em")
	    .style("text-anchor", "middle")
	    .text(xlabelName);

	

	svg.append("g")
	    .attr("class", "y axis")
	    .attr("transform", "translate(20,0)")
	    .call(yAxis)
	  .append("text")
	    .attr("transform", "translate(-50," + height/2 + ")"+"rotate(-90)")
	    .attr("y", "0em")
	    .attr("dy", "0.8em")
	    .style("text-anchor", "middle")
	    .text(ylabelName);
	colors = d3.scale.category10();
	svg.selectAll(".bar")
	    .data(data)
	  .enter().append("rect")
	    .attr("class", "bar")
	    .attr("x", function(d) { return x(d.name); })
	    .attr("width", x.rangeBand())
	    .attr("transform", "translate(20,0)")
	    .attr("y", function(d) { return y(d.value); })
	    .attr("height", function(d) { return height - y(d.value); })
	    .attr("fill",function(d,i){return colors(i)})
	    .on('mouseover', tip.show)
	    .on('mouseout', tip.hide);
}