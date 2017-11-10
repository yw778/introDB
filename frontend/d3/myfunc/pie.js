var pie = function(id,data,width,height,outerRadius, innerRadius){
    // sort函数自动隐式执行降序排列，而且数据从顶部开始顺时针展示，传入null可以阻止排序
    var pie = d3.layout.pie()
	.sort(null)
	.value(function(d) { return d.value;});
    //定义了10中颜色主题
    var color = d3.scale.category10();
    var svg = d3.select(id).append("svg").attr("width", width + 100).attr("height", height + 100);
    //定义外半径
    
    //定义路径
    var arc = d3.svg.arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius);

    //定义了另一种路径函数
    var arc2 = d3.svg.arc()
        .innerRadius(innerRadius - 10)
        .outerRadius(outerRadius + 20)

    var arcs = svg.selectAll("g")
        .data(pie(data))
        .enter()
        .append("g")
        // 将饼图中心(SVG起点)移至中间
        .attr("transform", "translate(" + (outerRadius+30)  + "," + (outerRadius+50) + ")")
        //为每一块元素添加鼠标事件
        .on("mouseover", function(d) {

            d3.select(this).select("path").transition().attr("d", function(d) {
                console.log(d);
                return arc2(d);
            })
        })
        .on("mouseout", function(d){
            d3.select(this).select("path").transition().attr("d", function(d){
                return arc(d);
            })
        })
    arcs.append("path")
        .attr("fill", function(d, i) {
            return color(i);
        })
        .attr("d", function(d) {
            return arc(d);
        })
    arcs.append("text")
        .attr("transform", function(d) {
            return "translate(" + arc.centroid(d) + ")";
        })
        .attr("text-anchor", "middle")
        .text(function(d) {
            return d.data.name;;
        })
}