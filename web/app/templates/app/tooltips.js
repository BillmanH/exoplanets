function popvalues(a, m) {
    delete a[m]
    return a
}

function r(x) {
    x = Math.round(x * 100) / 100
    return x
}


function limitDict(d) {
    var things_we_dont_print = ["username", "objid", "id", "orbitsId", "vx", "vy", "x", "y"]
    for (i in things_we_dont_print) {
        d = popvalues(d, things_we_dont_print[i])
    }
    return d
}

//for tooltips, convert a dict to HTML
function dictToHtml(d) {
    html = ""
    var dt = {}
    Object.assign(d, dt);
    dt = limitDict(dt)
    for (var k in d) {
        x = k.replace(/_/g, " ")
        y = d[k]
        if (typeof (y) == "string") {
            y = d[k].replace(/_/g, " ")
        } else if (typeof (y) == "number") {
            y = r(y)
        } else if (typeof (y) == "object") {
            y = d[k].toString().replace(/_/g, " ")
        }
        html += x + ": " + y + "<br>"
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
    .html("<p>Default Text</p>");

