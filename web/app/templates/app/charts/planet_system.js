// note that the clickhandler for the solar
var p_objectColors = {
    'G': '#FDB813',
    'moon':'#F4F1C9',
    'terrestrial':'#3644E4',
    'ice':'#A7DEDA',
    'dwarf':'#0EC0A6',
    'gas':'#0EC0A6'
}

function draw_planet(pdata){
    // console.log(pdata)
    dwaw_node("pSystem",
            pdata["nodes"],
            pdata["links"],
            p_objectColors,
            .003,
            height,
            width,
            strokesFunc = s_objectStrokes) 
    dwaw_table(
        "planetsTable",
        pdata["nodes"],
        ["class", "name", "mass", "radius", "orbitsDistance", "orbitsName", "isSupportsLife"],  // an array of values that you want shown
        height,
        width
    )
}

