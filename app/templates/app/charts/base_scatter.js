function draw_scatter(
    objid,
    nodes,
    objectColors, // dict of types and colors based on class
    height,
    width,
    clickHandler=function(d){console.log("no click handler")},
    strokesFunc = function(d){return "black"}  // strokes logic can be customized
) {
    var svg = d3.select('body').append('svg')
        .attr('width', width)
        .attr('height', height)
        .classed('map', true)
        .attr("id", objid);


    glatScale = d3.scaleLinear()
        .domain(
            [
                d3.min(nodes, function (d) { return d.glat; }),
                d3.max(nodes, function (d) { return d.glat; })]
        ).range([1,100]);
    glonScale = d3.scaleLinear()
        .domain(
            [
                d3.min(nodes, function (d) { return d.glon; }),
                d3.max(nodes, function (d) { return d.glon; })]
        ).range([1,150]);

    var u = d3.select('#'+objid)
        .selectAll('circle')
        .data(nodes)

        u.enter()
        .append('circle')
        .attr('r', function (d) { return 5 })
        .style("fill", function (d) { return objectColors[d.disc_facility] })
        .attr("stroke",  function (d) {return "black" })
        .attr('class', function (d) { return "system" })
        .merge(u)
        .attr('cx', function (d) {
            return glatScale(d.glat)
        })
        .attr('cy', function (d) {
            return glonScale(d.glon)
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

    return svg
}