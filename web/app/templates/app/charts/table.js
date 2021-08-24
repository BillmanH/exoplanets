// stolen from here: http://bl.ocks.org/AMDS/4a61497182b8fcb05906
function dwaw_table(
    objid,
    data,
    titles,  // an array of values that you want shown
    height,
    width
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
                    return d;
                })

        var rows = table.append('tbody').selectAll('tr')
            .data(data)
            .enter()
                .append('tr');

        rows.selectAll('td')
        .data(function (d) {
            return titles.map(function (k) {
                return { 'value': d[k], 'name': k};
            });
        }).enter()
            .append('td')
            .attr('data-th', function (d) {
                return d.name;
            })
            .text(function (d) {
                return d.value;
            });
            

    return svg
}