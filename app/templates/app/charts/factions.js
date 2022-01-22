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

function clickTableFaction(d) {
    $.ajax({
        url: '/ajax/faction-details',
        type: 'get',
        data: d,
        dataType: 'json',
        beforeSend: function () {
            // d3.selectAll('#peopleTable').remove()
        },
        success: function (data) {
            console.log(data)
            if ("pops" in data) {
                draw_table(
                    "peopleTable",
                    data['pops'],
                    pop_table_lables
                )
            }
            addTextBox(d, data)
        }
    });
}

draw_table(
    "planetsTable",
    factions["nodes"],
    faction_table_lables,
    tableClickHandler = function (d) { console.log(d) }
)