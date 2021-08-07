
var width = 640,
    height = 480,
    defaultNodeSize = 10;
var svg = d3.select('body').append('svg')
    .attr('width', width)
    .attr('height', height);

// https://github.com/d3/d3-force#simulation
var force = d3.forceSimulation(nodes)
    .force('charge', d3.forceManyBody())
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force("link", d3.forceLink(links).id(d => d.id))
    .on('tick', ticked);

var point = {}
function ticked() {
    var u = d3.select('svg')
        .selectAll('circle')
        .data(nodes)

    u.enter()
        .append('circle')
        .attr('r', function (d) { return d.radius * 10 })
        .merge(u)
        .attr('cx', function (d) {
            return d.x
        })
        .attr('cy', function (d) {
            return d.y
        })
        .on("mouseover", (event) => {
            return tooltip.style("visibility", "visible").html(dictToHtml(d3.select(this).datum().data));
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