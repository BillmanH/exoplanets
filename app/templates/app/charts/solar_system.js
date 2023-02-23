
var s_objectColors = {
    'G': '#FDB813',
    'rocky':'#F4F1C9',
    'terrestrial':'#73513C',
    'ice':'#A7DEDA',
    'dwarf':'#0EC0A6',
    'gas':'#0EC0A6'
}

function s_objectStrokes (d) { 
    var objectStrokes = {
        "true":"#6b93d6",
        "false":"black"
    }
    return objectStrokes[d.isSupportsLife.toLowerCase()] 
}


function click_planet(d){
    $.ajax({
        url: '/ajax/planet',
        type: 'get',
        data: d,
        dataType: 'json',
        beforeSend: function () {
            d3.selectAll('#pSystem').remove()
            d3.selectAll('#planetsTable').remove()
            d3.selectAll('#peopleTable').remove()
            d3.selectAll('#factionTable').remove()
            d3.selectAll('#description').remove()
        },
        success: function(data){
            cnsl(data)
            if (data['error'] == "objtype is star"){}
            else {
                draw_planet(data)
                addTextBox(d,data)
            }
        }
    });
}

ssystem = draw_node(
    "sSystem",
    solar_system['nodes'],
    solar_system['edges'],
    s_objectColors,
    .15,
    height,
    width,
    clickHandler = click_planet,
    strokesFunc = s_objectStrokes
)


