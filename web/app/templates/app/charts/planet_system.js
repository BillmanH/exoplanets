// note that the clickhandler for the solar
var p_objectColors = {
    'G': '#FDB813',
    'moon':'#F4F1C9',
    'terrestrial':'#3644E4',
    'ice':'#A7DEDA',
    'dwarf':'#0EC0A6',
    'gas':'#0EC0A6'
}

// dict of the value you want shown and `label` that you want as the column label
var planet_table_lables = [{"label":"Name","value":"name"}, 
                            {"label":"Class","value":"class"},
                            {"label":"Mass","value":"mass"},
                            {"label":"Radius","value":"radius"},
                            {"label":"Orbiting Distance","value":"orbitsDistance"},
                            {"label":"Orbiting Object","value":"orbitsName"},
                            {"label":"Supports Life","value":"isSupportsLife"}
                        ]

var population_table_lables = [{"label":"Name","value":"name"}, 
                            {"label":"Aggression","value":"population_aggression"},
                            {"label":"Conformity","value":"population_conformity"},
                            {"label":"Constitution","value":"population_constitution"},
                            {"label":"Literacy","value":"population_literacy"}
                        ]

function clickTablePlanet(d){
    $.ajax({
        url: '/ajax/planet-details',
        type: 'get',
        data: d,
        dataType: 'json',
        beforeSend: function () {
            d3.selectAll('#peopleTable').remove()
            // d3.selectAll('#planetsTable').remove()
        },
        success: function(data){
            console.log(data)
            if ("pops" in data){
                draw_table(
                    "peopleTable",
                    data['pops'],
                    population_table_lables
                    )
            }
        }
    });
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
    draw_table(
        "planetsTable",
        pdata["nodes"],
        planet_table_lables,  
        tableClickHandler = clickTablePlanet
    )
}


