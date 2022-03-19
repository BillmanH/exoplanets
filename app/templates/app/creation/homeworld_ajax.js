var pop_table_lables = [{"label":"Name","value":"name"}, 
                            {"label":"Aggression","value":"aggression"},
                            {"label":"Conformity","value":"conformity"},
                            {"label":"Constitution","value":"constitution"},
                            {"label":"Literacy","value":"literacy"},
                            {"label":"Wealth","value":"wealth"}
                        ]

var faction_table_lables = [
    { "label": "Faction #", "value": "faction_no" },
    { "label": "Name", "value": "name" },
    { "label": "Type", "value": "label" }
]

function genesisHomeworld(d) {
    $.ajax({
        url: '/ajax/genesis-homeworld',
        type: 'get',
        data: {"username":username,"solar_system":solar_system['nodes']},
        dataType: 'json',
        success: function (data) {
            console.log("pop data")
            console.log(data)
            if ("pops" in data) {
                draw_table(
                    "peopleTable",
                    data['pops'],
                    pop_table_lables
                )
                draw_table(
                    "FactionTable",
                    data['factions'],
                    faction_table_lables
                )
            }
        }
    });
}   

genesisHomeworld()

a = $("#pleasewait").clone();
$("#pleasewait").remove();
$("body").append(a);