
var s_objectColors = {
    'G': '#FDB813',
    'moon':'#F4F1C9',
    'terrestrial':'#73513C',
    'ice':'#A7DEDA',
    'dwarf':'#0EC0A6'
}

function s_objectStrokes (d) { 
    var objectStrokes = {
        "True":"#6b93d6",
        "False":"black"
    }
    return objectStrokes[d.isSupportsLife] 
}


function click_planet(){
    console.log('was clicked')
    $.ajax({
        url: '/ajax/planet',
        type: 'get',
        data: {
        'planet': 'planet'
    },
    dataType: 'json',
    beforeSend: function () {
        console.log('ajax sent')
      },
    success: function(data){draw_planet(data)}
    });
}

ssystem = dwaw_node(
    "sSystem",
    nodes,
    links,
    s_objectColors,
    .15,
    height,
    width,
    clickHandler = click_planet,
    strokesFunc = s_objectStrokes
)


