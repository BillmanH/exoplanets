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
        var svg = d3.select('body').append('div')
            .attr('width', a.width)
            .attr('height', a.height/2)
            .classed('action', true)
            .classed('menu', true)
            .attr("id", a.objid);       

        var button = svg.append('text')
            .html(function(d) {return p['name']+"has no actions available"});

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

    var g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    var button = g.selectAll('a')
                    .data(a.nodes)
                    .enter()
                    .append('a')
                    .classed('button',true)
                    .attr("href", "takeaction")
                    .html(function(d) {return d['objtype']+': '+d['type']});

    var button = g.selectAll('text')
                    .data(a.nodes)
                    .enter()
                    .append('text')
                    .html(function(d) {return d['comment']});


    return svg
}