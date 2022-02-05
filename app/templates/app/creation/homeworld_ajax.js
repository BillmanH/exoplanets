function genesisHomeworld(d) {
    // get the pops that are in that faction
    $.ajax({
        url: '/ajax/genesis-homeworld',
        type: 'get',
        data: d,
        dataType: 'json',
        success: function (data) {
            console.log(data)
            if ("pops" in data) {
                draw_table(
                    "peopleTable",
                    data['pops'],
                    pop_table_lables
                )
            }
        }
    });
}
