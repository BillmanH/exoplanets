function draw_scatter(
    objid,
    nodes,
    height,
    width,
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
    var svg = d3.select('body').append('svg')
        .attr('width', width)
        .attr('height', height)
        .classed('map', true)
        .attr("id", objid);


    glatScale = d3.scaleLinear()
        .domain(
            [
                d3.min(nodes, function (d) { return d[xy["x"]]; }),
                d3.max(nodes, function (d) { return d[xy["x"]]; })]
        ).range([1, 100]);
    glonScale = d3.scaleLinear()
        .domain(
            [
                d3.min(nodes, function (d) { return d[xy["y"]]; }),
                d3.max(nodes, function (d) { return d[xy["y"]]; })]
        ).range([1, 150]);

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