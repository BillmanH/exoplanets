
var s_objectColors = {
    'G': '#FDB813',
    'moon':'#F4F1C9',
    'terrestrial':'#73513C',
    'ice':'#A7DEDA',
    'dwarf':'#0EC0A6',
    'gas':'#0EC0A6'
}

function s_objectStrokes (d) { 
    var objectStrokes = {
        "True":"#6b93d6",
        "False":"black"
    }
    return objectStrokes[d.isSupportsLife] 
}

var testvar = "d"
function click_planet(d){
    // input_data = d
    // delete d["x"];
    // delete d["y"];
    // delete d["vx"];
    // delete d["vy"];
    $.ajax({
        url: '/ajax/planet',
        type: 'get',
        data: d,
    dataType: 'json',
    beforeSend: function () {
        d3.selectAll('#pSystem').remove()
      },
    success: function(data){draw_planet(data)}
    });
}

ssystem = dwaw_node(
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


