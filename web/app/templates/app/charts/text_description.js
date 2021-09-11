// TODO: Once this gets more complicated, each `describe` function could easily be brought out to other files. 

function describePlanet(d,nodes){
    var desc = "<p>Orbiting " + d.orbitsName + " , at ~" + d.orbitsDistance + " AUs</p>"
    if (d.isSupportsLife=="True"){
        desc += "<p> " + d.name + " is capable of supporting life.</p>" 
    } else {
        desc += "<p> " + d.name + " is not known to support life.</p>" 
    }
    return desc
}

function describeMoon(d,nodes){
    console.log(d)
    var desc = "<p>Orbiting " + d.orbitsName + " , at ~" + d.orbitsDistance + " AUs</p>"
    if (d.isSupportsLife=="True"){
        desc += "<p> " + d.name + " is capable of supporting life.</p>" 
    } else {
        desc += "<p> " + d.name + " is not known to support life.</p>" 
    }
    return desc
}

function addTextBox(d, nodes){
    // d = a single item, like a planet that will be described
    // nodes = a list of items, that can be aggregated to proved description
    var description = "<p>" + d.name + " , a " + d.objtype + " </p>"
    switch(d.objtype) {
        case "planet":
            description += describePlanet(d,nodes)
        break;
        case "moon":
            description += describeMoon(d,nodes)
        break;
        default:
            console.log(d)
            description = d.name + " can not be identified"
    }

    var table = d3.select('body')
        .append('div')
        .attr("id", "description")
        .classed('details', true)
        .html(description);
}