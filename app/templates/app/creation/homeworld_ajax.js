var pop_table_lables = [{"label":"Name","value":"name"}, 
                            {"label":"Aggression","value":"aggression"},
                            {"label":"Conformity","value":"conformity"},
                            {"label":"Constitution","value":"constitution"},
                            {"label":"Literacy","value":"literacy"},
                            {"label":"Wealth","value":"wealth"},
                            {"label":"Health","value":"health"}
                        ]

var faction_table_lables = [
    { "label": "Name", "value": "name" },
    { "label": "Type", "value": "label" }
]

function genesisPopDesire(d){
    // Desires and actions are in the same call
    $.ajax({
        url: '/ajax/genesis-pop-desire',
        // Doesn't really need client data, but as a placeholder
        data: {"username":username},
        dataType: 'json',
        success: function (data) {
            console.log("pop desires, was created")
            $("body").append("When you are ready, <a href='/systemmap' class='menu button'>go to the system map</a>");
        }
    })
}


function genesisHomeworld(d) {
    $.ajax({
        url: '/ajax/genesis-homeworld',
        type: 'get',
        data: {"username":username},
        dataType: 'json',
        success: function (data) {
            console.log("pops, were created")
            if ("pops" in data) {
                draw_table(
                    "peopleTable",
                    data['pops'],
                    pop_table_lables
                )
                console.log(data['factions'])
                draw_table(
                    "FactionTable",
                    data['factions'],
                    faction_table_lables
                )
            }
            genesisPopDesire()
        },
        
    });
}

genesisHomeworld()

