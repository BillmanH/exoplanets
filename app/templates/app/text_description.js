// TODO: Once this gets more complicated, each `describe` function could easily be brought out to other files. 

function ct(x){
    var newStr = x.replace(/_/g, " ");
    return newStr
}

function evalueateLevels(x){
    var evaluation = "normal"
    if (x < .5) {
        if (x < .2){
            evaluation = "very low"
        } else {
            evaluation = "low"
        }
    }
    if (x >= .5) {
        if (x >= .8){
            evaluation = "very high"
        } else {
            evaluation = "high"
        }
    }
}

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
    cnsl(d)
    var desc = "<p>Orbiting " + d.orbitsName + " , at ~" + d.orbitsDistance + " AUs</p>"
    if (d.isSupportsLife=="True"){
        desc += "<p> " + d.name + " is capable of supporting life.</p>" 
    } else {
        desc += "<p> " + d.name + " is not known to support life.</p>" 
    }
    return desc
}


function describePop(d,nodes){
    cnsl(d)
    if (d['isIdle'] == "True"){
        var desc = "<p>is idle"
        if (d['hasActions'] = "no"){
            desc += ", but has no actions available to take"
        }
    } else {
        var desc = "<p>is not idle"
    }
    desc += "</p>"
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
        case "pop":
            description += describePop(d)
        break;
        default:
            cnsl("error: a discription was called that has no known objecttype")
            description = d.name + " can not be identified"
    }

    var table = d3.select('body')
        .append('div')
        .attr("id", "description")
        .classed('details', true)
        .html(description);
}

function completed(d){
    if (d['job']['status']=="pending"){
        return " is working on "
    } else if (d['job']['status']=="resolved"){
        return " has completed working on "
    }
}

function newsItem(d){
    // console.log(d)
    description = d['agent']['name'] + completed(d) + ct(d['job']['actionType'])
    return description
}

function addNewsBox(d){
    // console.log(d['newsfeed'])
    var description = "<div>"
    for (i = 0; i < d['newsfeed'].length; i++) {
        description += newsItem(d['newsfeed'][i])
    }
    var overviewtext = d3.select('.overview')
    .append('p')
    .attr("id", "newsfeed")
    .append('p')
        .enter()
        .data()
    .html(description)
    .on("click", (event, d) => {marknewsasdone(d)})
}   