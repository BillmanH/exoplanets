
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
}

// NOTE: The clickhandler in the solar_system is where this function is activated
function planet_details(data)
    {
        $("body").append("<div id='planetDetails'></div>");
        $("#planetDetails").append("<li>Appended item</li>");
}
