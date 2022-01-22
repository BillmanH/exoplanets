var faction_table_lables = [{"label":"Faction #","value":"faction_no"}, 
                            {"label":"Name","value":"name"},
                            {"label":"Type","value":"objtype"}
                        ]


draw_table(
    "planetsTable",
    factions["nodes"],
    faction_table_lables,  
    tableClickHandler = function(d){console.log(d)}
)