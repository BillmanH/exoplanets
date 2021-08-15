function dwaw_node(
    objid,
    nodes,
    links,
    objectColors,
    orbitalStrength = .15,
    height,
    width
) {
    var svg = d3.select('body').append('svg')
        .attr('width', width)
        .attr('height', height)
        .classed('map', true)
        .classed('planet', true)
        .attr("id", objid);

    radiusScale = d3.scaleLog()
        .domain(
            [
                d3.min(nodes, function (d) { return d.radius; }),
                d3.max(nodes, function (d) { return d.radius; })]
        ).range([0, 20]);

    orbitScale = d3.scaleLinear()
        .domain(
            [
                d3.min(nodes, function (d) { return d.orbitsDistance; }),
                d3.max(nodes, function (d) { return d.orbitsDistance; })]
        ).range([0, 20]);

    var planet_force = d3.forceSimulation(nodes)
        .force('charge', d3.forceManyBody())
        .force("link", d3.forceLink(links)
            .id(d => d.id)
            .distance(function (d) { return orbitScale(d['source'].orbitsDistance) })
            .strength(orbitalStrength)
        )
        .force('center', d3.forceCenter(width / 2, height / 2))
        .on('tick', planet_ticked);


    var point = {}
    function planet_ticked() {
        var u = d3.select('#'+objid)
            .selectAll('circle')
            .data(nodes)

        u.enter()
            .append('circle')
            .attr('r', function (d) { return radiusScale(d.radius) })
            .style("fill", function (d) { return objectColors[d.class] })
            .attr("stroke", 'black')
            .merge(u)
            .attr('cx', function (d) {
                return d.x
            })
            .attr('cy', function (d) {
                return d.y
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

        u.exit().remove()
    }

}