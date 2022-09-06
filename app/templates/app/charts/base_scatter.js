
function scatterConfig(
    // Note when using: The arguments need to be present, in order. Even if not used. 
    objid = "error no id",
    nodes = [],
    height = 400,
    width = 400,
    // scaleToOne = true : the scatter plot will scale the values between 0 and 1.
    // scaleToOne = false : the plot will scale to the values in the `xy` dict.
    scaleToOne = true,
    // need to know the value to use for X and Y in the scale AND the .attr('cx')
    xy = {"x":"x",
        "y":"y"},
    // optional customization of some functions. 
    // This would be specified by the js script that calls `draw_scatter()`
    circleFill = function (d) { return "white" },
    circleSize = function (d) { return 5 },
    strokeColor = function (d) { return "black" },
    circleClass = function (d) { return "circle" },
    clickHandler = function (d) { console.log("no click handler") }
) {
        this.objid = objid;
        this.nodes = nodes;
        this.height = height;
        this.width = width;
        this.scaleToOne = scaleToOne;
        this.xy = xy;
        this.circleFill = circleFill;
        this.circleSize = circleSize;
        this.strokeColor = strokeColor;
        this.circleClass = circleClass;
        this.clickHandler = clickHandler;
}



function draw_scatter(a=scatterConfig) {
    const margin = { left: 120, right: 60, top: 20, bottom: 120 };

    const innerWidth = a.width - margin.left - margin.right;
    const innerHeight = a.height - margin.top - margin.bottom;

    var svg = d3.select('body').append('svg')
        .attr('width', a.width)
        .attr('height', a.height)
        .classed('map', true)
        .attr("id", a.objid);

    var g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
    var xAxisG = g.append('g')
        .attr('transform', `translate(0, ${innerHeight})`);
    var yAxisG = g.append('g');

    xAxisG.append('text')
        .attr('class', 'axis-label')
        .attr('x', innerWidth / 2)
        .attr('y', 100)
        .text(a.xy["x"]);

    yAxisG.append('text')
        .attr('class', 'axis-label')
        .attr('x', -innerHeight / 2)
        .attr('y', -60)
        .attr('transform', `rotate(-90)`)
        .style('text-anchor', 'middle')
        .text(a.xy["y"]);


    if (a.scaleToOne){
        glatScale = d3.scaleLinear().domain([0,1]).range([0, innerWidth]);
        glonScale = d3.scaleLinear().domain([0,1]).range([0, innerHeight]);   
    } else {
        glatScale = d3.scaleLinear()
            .domain(
                [
                    d3.min(a.nodes, function (d) { return d[a.xy["x"]]; }),
                    d3.max(a.nodes, function (d) { return d[a.xy["x"]]; })]
            ).range([0, innerWidth]);
        glonScale = d3.scaleLinear()
            .domain(
                [
                    d3.min(a.nodes, function (d) { return d[a.xy["y"]]; }),
                    d3.max(a.nodes, function (d) { return d[a.xy["y"]]; })]
            ).range([0, innerHeight]);
    }

    var t = g.selectAll("text")
        .data(a.nodes)

    t.enter()
        .append("text")
        .text(function(d) {return d["name"]})
        .attr("x", function(d) {return glatScale(d[a.xy["x"]])})
        .attr("y", function(d) {return glonScale(d[a.xy["y"]])})
        .attr("font-size", "15px")
        .attr("fill", "white")

    var u = g.selectAll('circle')
        .data(a.nodes)

    u.enter()
        .append('circle')
        .attr('r', a.circleSize)
        .style("fill", a.circleFill)
        .attr("stroke", a.strokeColor)
        .attr('class', a.circleClass)
        .attr('cx', function (d) {
            return glatScale(d[a.xy["x"]])
        })
        .attr('cy', function (d) {
            return glonScale(d[a.xy["y"]])
        })
        .on("mouseover", (event, d) => {
            return tooltip.style("visibility", "visible").html(dictToHtml(d));
        })
        .on("mousemove", (event) => {
            return tooltip.style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px")
        })
        .on("mouseout", (event) => {
            d3.pointer(event)
            return tooltip.style("visibility", "hidden");
        })
        .on("click", (event, d) => {a.clickHandler(d)})

    return svg
}