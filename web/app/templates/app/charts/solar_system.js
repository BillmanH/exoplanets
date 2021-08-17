
var s_objectColors = {
    'G': '#FDB813',
    'moon':'#F4F1C9',
    'terrestrial':'#73513C',
    'ice':'#A7DEDA',
    'dwarf':'#0EC0A6'
}

ssystem = dwaw_node(
    "sSystem",
    nodes,
    links,
    s_objectColors,
    .15,
    height,
    width
)

supportsLifeColor = {}

d3.selectAll(".terrestrial")
    .attr("stroke", "#3644E4")
    .style("stroke-width", 2)


