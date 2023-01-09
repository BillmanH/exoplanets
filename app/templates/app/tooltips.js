function cnsl(a){
    if (verbose){
        console.log(a)
    }
}

function popvalues(a, m) {
    delete a[m]
    return a
}

function r(x, n=100) {
    x = Math.round(x * n) / n
    return x
}

renames = {}

function limitDict(d) {
    var things_we_dont_print = ["name","username", "objid", "id", "orbitsId",
                                 "vx", "vy", "x", "y","z", "isInFaction", "iter",
                                "gui"]
    for (i in things_we_dont_print) {
        d = popvalues(d, things_we_dont_print[i])
    }
    return d
}

function toProperCase(s)
{
  return s.toLowerCase().replace(/^(.)|\s(.)/g, 
          function($1) { return $1.toUpperCase(); });
}

//for tooltips, convert a dict to HTML
function dictToHtml(d) {
    html = "<div><strong>"+ d['name'] +"</strong>" + ": "+ d['objtype']+ "</div>"
    var dt = Object.assign({}, d);
    dt = limitDict(dt)
    for (var k in dt) {
        x = k.replace(/_/g, " ")
        y = dt[k]
        if (y.toString().indexOf(".") != -1) {y = parseFloat(y.toString())};
        if (typeof (y) == "string") {
            y = dt[k].replace(/_/g, " ")
        } else if (typeof (y) == "number") {
            y = r(y)
        } else if (typeof (y) == "object") {
            y = dt[k].toString().replace(/_/g, " ")
        }
        html += x + ": " + y + "<br>"
    }
    return html
}

function dictToSimpleText(d) {
    html = d['name'] + " : "+ d['objtype'] +["\n"]
    var dt = Object.assign({}, d);
    dt = limitDict(dt)
    for (var k in dt) {
        x = k.replace(/_/g, " ")
        y = dt[k]
        if (y.toString().indexOf(".") != -1) {y = parseFloat(y.toString())};
        if (typeof (y) == "string") {
            y = dt[k].replace(/_/g, " ")
        } else if (typeof (y) == "number") {
            y = r(y)
        } else if (typeof (y) == "object") {
            y = dt[k].toString().replace(/_/g, " ")
        }
        html += x + ": " + y + "\n"
    }
    return html
}


var tooltip = d3.select("body")
    .append("div")
    .style("background-color", 'white')
    .attr("id", "hover-tooltip")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
    .style("padding-top", "5px")
    .style("padding-right", "5px")
    .style("padding-bottom", "5px")
    .style("padding-left", "5px")
    .html("<p>Default Text</p>");

