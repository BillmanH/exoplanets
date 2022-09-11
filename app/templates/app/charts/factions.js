var faction_table_lables = [
    { "label": "Faction #", "value": "faction_no" },
    { "label": "Name", "value": "name" },
    { "label": "Type", "value": "objtype" }
]

var pop_table_lables = [{"label":"Name","value":"name"}, 
                            {"label":"Aggression","value":"aggression"},
                            {"label":"Conformity","value":"conformity"},
                            {"label":"Constitution","value":"constitution"},
                            {"label":"Literacy","value":"literacy"},
                            {"label":"Idle","value":"isIdle"}
                        ]

var desire_table_lables = [{"Type":"Name","value":"type"}, 
                            {"label":"Name","value":"name"},
                            {"label":"Weight","value":"weight"},
                            {"label":"type","value":"type"},
                            {"label":"comment","value":"comment"},
                            {"label":"leadingAttribute","value":"leadingAttribute"}
                        ]



// on load, get population
$.ajax({
    url: '/ajax/pops-all',
    type: 'get',
    data: {"username":"{{ user.username | safe }}"},
    dataType: 'json',
    beforeSend: function () {
        d3.selectAll('#peopleTable').remove()
        d3.selectAll('#action').remove()
    },
    success: function (data) {
        cnsl(data)
        if ("pops" in data) {
            var categoryScheme = d3.scaleOrdinal().domain(data["pops"]).range(["black", "blue", "green", "yellow", "black", "grey", "darkgreen", "pink", "brown", "slateblue", "grey1", "orange"])
            allPopsCongig = new scatterConfig(
                objid = "scatterpops",
                nodes = data["pops"],
                height = height,
                width = width,
                scaleToOne = false,
                xy = {"x":"conformity",
                    "y":"aggression"},
                circleFill = function(d){return categoryScheme(d['isInFaction']) },
                circleSize = function (d) { return 5 },
                strokeColor = function (d) { return "black" },
                circleClass = function (d) { return "popCircle" },
                clickHandler = clickPop 
            )
            draw_scatter(allPopsCongig)
            }
        },
    error: function (jqXHR, status, err) {
        console.log(status,err);
        },
    });

function clickTableFaction(d) {
    // get the pops that are in that faction
    $.ajax({
        url: '/ajax/faction-details',
        type: 'get',
        data: d,
        dataType: 'json',
        beforeSend: function () {
            console.log(d)
            d3.selectAll('#peopleTable').remove()
            d3.selectAll('#peopleScatter').remove()
            d3.selectAll('#peopledesires').remove()
            d3.selectAll('#action').remove()
        },
        success: function (data) {
            console.log(data)
            if ("pops" in data) {
                draw_table(
                    "peopleTable",
                    data['pops'],
                    pop_table_lables,
                    tableClickHandler = clickPop
                )
                popScatterA = new scatterConfig(
                    objid = "peopleScatter",
                    nodes = data['pops'],
                    height = height,
                    width = width,
                    scaleToOne = false,
                    xy = {"x":"conformity",
                        "y":"aggression"},
                    circleFill = function (d) { return "black" },
                    circleSize = function (d) { return 5 },
                    strokeColor = function (d) { return "white" },
                    circleClass = function (d) { return "popCircle" },
                    clickHandler = clickPop 
                )
                popScatterB = new scatterConfig(
                    objid = "peopleScatter",
                    nodes = data['pops'],
                    height = height,
                    width = width,
                    scaleToOne = false,
                    xy = {"x":"faction_loyalty",
                        "y":"constitution"},
                    circleFill = function (d) { return "black" },
                    circleSize = function (d) { return 5 },
                    strokeColor = function (d) { return "white" },
                    circleClass = function (d) { return "popCircle" },
                    clickHandler = clickPop 
                )
                draw_scatter(popScatterA)
                draw_scatter(popScatterB)
            }
        }
    });
}

function clickTablePopDesires(d){
    $.ajax({
        url: '/ajax/pop-desires',
        type: 'get',
        data: d,
        dataType: 'json',
        beforeSend: function () {
            d3.selectAll('#peopleScatter').remove()
            d3.selectAll('#peopledesires').remove()
            d3.selectAll('#action').remove()
        },
        success: function(data){
            console.log(data)
            if ("desires" in data){
                draw_table(
                    "peopledesires",
                    data['desires'],
                    desire_table_lables
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

function clickPop(d){
    cnsl(d)
    if(d["isIdle"]=="True"){
        $.ajax({
            url: '/ajax/pop-actions',
            type: 'get',
            data: d,
            dataType: 'json',
            beforeSend: function () {
                d3.selectAll('#peopleScatter').remove()
                d3.selectAll('#peopledesires').remove()
                d3.selectAll('#action').remove()
                d3.selectAll('#description').remove()
            },
            success: function(data){
                console.log(data)
                if (data['error'] == 'no actions returned'){
                    d['hasActions'] = "no"
                    addTextBox(d)
                }
                else {
                        popActionConfig = new actionConfig(
                            objid="action",
                            height = height,
                            width = width,
                            data['actions'],
                            )
                        draw_action(d,popActionConfig)
                }
            }
        })
    }
    else {
        d3.selectAll('#description').remove()
        addTextBox(d)
    }
}

