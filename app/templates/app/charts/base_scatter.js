function draw_scatter(
    objid,
    nodes,
    height,
    width,
    xLabel='X axis',
    yLabel='Y axis',
    // need to know the value to use for X and Y in the scale AND the .attr('cx')
    xy = {"x":"x",
        "y":"y"},
    // optional customization of some functions. 
    // This would be specified by the js script that calls `draw_scatter()`
    circleFill = function (d) { return "white" },
    circleSize = function (d) { return 5 },
    strokeColor = function (d) { return "black" },
    circleClass = function (d) { return "circle" },
    clickHandler = function (d) { console.log("no click handler") },
) {
    const margin = { left: 120, right: 30, top: 20, bottom: 120 };

    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    var svg = d3.select('body').append('svg')
        .attr('width', width)
        .attr('height', height)
        .classed('map', true)
        .attr("id", objid);

    var g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
    var xAxisG = g.append('g')
        .attr('transform', `translate(0, ${innerHeight})`);
    var yAxisG = g.append('g');

    xAxisG.append('text')
        .attr('class', 'axis-label')
        .attr('x', innerWidth / 2)
        .attr('y', 100)
        .text(xLabel);

    yAxisG.append('text')
        .attr('class', 'axis-label')
        .attr('x', -innerHeight / 2)
        .attr('y', -60)
        .attr('transform', `rotate(-90)`)
        .style('text-anchor', 'middle')
        .text(yLabel);

    glatScale = d3.scaleLinear()
        .domain(
            [
                d3.min(nodes, function (d) { return d[xy["x"]]; }),
                d3.max(nodes, function (d) { return d[xy["x"]]; })]
        ).range([10, 100]);
    glonScale = d3.scaleLinear()
        .domain(
            [
                d3.min(nodes, function (d) { return d[xy["y"]]; }),
                d3.max(nodes, function (d) { return d[xy["y"]]; })]
        ).range([10, 150]);

    var u = d3.select('#' + objid)
        .selectAll('circle')
        .data(nodes)

    u.enter()
        .append('circle')
        .attr('r', circleSize)
        .style("fill", circleFill)
        .attr("stroke", strokeColor)
        .attr('class', circleClass)
        .merge(u)
        .attr('cx', function (d) {
            return glatScale(d[xy["x"]])
        })
        .attr('cy', function (d) {
            return glonScale(d[xy["y"]])
        })
        .on("mouseover", (event, d) => {
            return tooltip.style("visibility", "visible").html(dictToHtml(d));
        })
        .on("mousemove", (event) => {
            return tooltip.style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px")
        })
        .on("mouseout", (event) => {
            d3.pointer(event)
            return tooltip.style("visibility", "hidden");
        })
        .on("click", (event, d) => {clickHandler(d)})

    return svg
}