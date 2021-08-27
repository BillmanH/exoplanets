// stolen from here: http://bl.ocks.org/AMDS/4a61497182b8fcb05906
function draw_table(
    objid,
    data,
    titles,  // an array of values that you want shown
    height,
    width,
    tableClickHandler = function(d){console.log(d)} // default function to handle hover 
) {
        // var table = d3.select('#'+objid).append('table');
        var table = d3.select('body')
                        .append('table')
                        .attr("id", objid)
                        .classed('details', true);

        var headers = table.append('thead')
            .append('tr')
            .selectAll('th')
            .data(titles)
            .enter()
                .append('th')
                .text(function (d) {
                    return d.label;
                })

        var rows = table.append('tbody').selectAll('tr')
            .data(data)
            .enter()
                .append('tr')
                .on("click",(event, d) => {tableClickHandler(d)})

        rows.selectAll('td')
        .data(function (d) {
            return titles.map(function (k) {
                return { 'value': d[k.value], 'name': k};
            });
        }).enter()
            .append('td')
            .attr('data-th', function (d) {
                return d.name;
            })
            .attr("id", function(d,i){ return "td"+i})
            .on("mouseover",function(d) {
                d3.select(this).classed("table-hover",true)
            })
            .on("mouseout",function(d) {
                d3.select(this).classed("table-hover",false)
            })
            .text(function (d) {
                return d.value;
            });      
}