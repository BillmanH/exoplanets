
var s_objectColors = {
    'G': '#FDB813',
    'moon':'#F4F1C9',
    'terrestrial':'#3644E4',
    'ice':'#A7DEDA',
    'dwarf':'#0EC0A6'
}

function draw_planet(pdata){
    console.log(pdata)
    d3.selectAll('#pSystem').remove()
    dwaw_node("pSystem",
                    nodes,
                    links,
                    s_objectColors,
                    .15,
                    height,
                    width) 
}




