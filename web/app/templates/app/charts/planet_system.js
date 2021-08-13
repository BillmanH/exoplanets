
var width = 640,
    height = 480,
    defaultNodeSize = 10,
    orbitalStrength = .15;

var plan_svg = d3.select('body').append('svg')
    .attr('width', width)
    .attr('height', height)
    .classed('map', true)
    .classed('planet', true)
    .attr("id", 'map_planet');

p_b_box = document.querySelector('#map_planet').getBoundingClientRect()


var p_objectColors = {
    'G': '#FDB813',
    'moon': '#F4F1C9',
    'terrestrial': '#3644E4',
    'ice': '#A7DEDA',
    'dwarf': '#0EC0A6'
}
// normalize the radius

p_planetScale = d3.scaleLog()
    .domain(
        [
            d3.min(nodes, function (d) { return d.radius; }),
            d3.max(nodes, function (d) { return d.radius; })]
    ).range([0, 20]);

p_orbitScale = d3.scaleLinear()
    .domain(
        [
            d3.min(nodes, function (d) { return d.orbitsDistance; }),
            d3.max(nodes, function (d) { return d.orbitsDistance; })]
    ).range([0, 20]);

var planet_force = d3.forceSimulation(nodes)
    .force('charge', d3.forceManyBody())
    .force("link", d3.forceLink(links)
        .id(d => d.id)
        .distance(function (d) { return p_orbitScale(d['source'].orbitsDistance) })
        .strength(w)
    )
    .force('center', d3.forceCenter(p_b_box.right - (p_b_box.width / 2),
        p_b_box.bottom - (p_b_box.height / 2))
    )
    .on('tick', planet_ticked);


var point = {}
function planet_ticked() {
    var u = d3.select('#map_planet')
        .selectAll('circle')
        .data(nodes)

    u.enter()
        .append('circle')
        .attr('r', function (d) { return p_planetScale(d.radius) })
        .style("fill", function (d) { return p_objectColors[d.class] })
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

