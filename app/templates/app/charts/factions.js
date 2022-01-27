var faction_table_lables = [
    { "label": "Faction #", "value": "faction_no" },
    { "label": "Name", "value": "name" },
    { "label": "Type", "value": "objtype" }
]

var pop_table_lables = [{"label":"Name","value":"name"}, 
                            {"label":"Aggression","value":"aggression"},
                            {"label":"Conformity","value":"conformity"},
                            {"label":"Constitution","value":"constitution"},
                            {"label":"Literacy","value":"literacy"}
                        ]

// on load, get population
$.ajax({
    url: '/ajax/pops-all',
    type: 'get',
    data: [],
    dataType: 'json',
    beforeSend: function () {
        d3.selectAll('#peopleTable').remove()
    },
    success: function (data) {
        console.log(data)
        if ("pops" in data) {
            draw_scatter(
                "scatterpops",
                data["pops"],
                height,
                width,
                xy = {"x":"conformity",
                    "y":"aggression"} 
            )
            }
        }
    });

function clickTableFaction(d) {
    // get the pops that are in that faction
    $.ajax({
        url: '/ajax/faction-details',
        type: 'get',
        data: d,
        dataType: 'json',
        beforeSend: function () {
            d3.selectAll('#peopleTable').remove()
            d3.selectAll('#peopleScatter').remove()
        },
        success: function (data) {
            console.log(data)
            if ("pops" in data) {
                draw_table(
                    "peopleTable",
                    data['pops'],
                    pop_table_lables
                )
                draw_scatter(
                    "peopleScatter",
                    data['pops'],
                    height,
                    width,
                    xy = {"x":"aggression",
                        "y":"conformity"}
                )
            }
        }
    });
}

draw_table(
    "factionsTable",
    factions["nodes"],
    faction_table_lables,
    tableClickHandler = clickTableFaction
)