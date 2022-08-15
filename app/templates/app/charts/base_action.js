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


function draw_action(a) {
    const margin = { left: 120, right: 60, top: 20, bottom: 120 };

    const innerWidth = a.width - margin.left - margin.right;
    const innerHeight = a.height - margin.top - margin.bottom;

    var svg = d3.select('body').append('svg')
        .attr('width', a.width)
        .attr('height', a.height/2)
        .classed('action', true)
        .attr("id", a.objid);

    return svg
}