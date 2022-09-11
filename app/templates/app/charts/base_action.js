// stolen from here: http://bl.ocks.org/AMDS/4a61497182b8fcb05906
function actionConfig(
    // Note when using: The arguments need to be present, in order. Even if not used. 
    objid = "error no id",
    height = 400,
    width = 400,
    nodes = [],
){
    this.objid = objid;
    this.height = height;
    this.width = width;
    this.nodes = nodes;
}

// Takes an (agent) and an (actionConfig)
function draw_action(p,a) {

    if (a.nodes[0]=='no actions returned'){


        return svg

    }

    const margin = { left: 120, right: 30, top: 20, bottom: 120 };

    const innerWidth = a.width - margin.left - margin.right;
    const innerHeight = a.height - margin.top - margin.bottom;

    var svg = d3.select('body').append('div')
        .attr('width', a.width)
        .attr('height', a.height/2)
        .classed('action', true)
        .classed('menu', true)
        .attr("id", a.objid);
    
    svg.append('div')
        .classed('action', true)
        .classed('header', true)
        .html(function() {return p['name']});
    

    var g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    var button = g.selectAll('button')
                    .data(a.nodes)
                    .enter()
                    .append('div')
                    .classed('button',true)
                    .html(function(d) {return d['objtype']+': '+d['type']})
                    .on("click", (event, d) => {takeAction(p,d)});

    var action_text = g.selectAll('text')
                    .data(a.nodes)
                    .enter()
                    .append('text')
                    .html(function(d) {return d['comment']});


    return svg
}


// Takes an (agent) and an (action)
function takeAction(p,a){
    cnsl(p.name)
    cnsl(a)
    var d = {"agent":p,
        "action":a}
    cnsl(d)
    $.ajax({
        url: '/ajax/take-action',
        type: 'get',
        data: { 'values' : JSON.stringify(d) },
        dataType: 'json',
        success: function(data){
            document.location.reload()
        },
        error: function(data){
            cnsl(data)
        }
    });
}
