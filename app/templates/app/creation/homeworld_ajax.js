function genesisHomeworld(d) {
    $.ajax({
        url: '/ajax/genesis-homeworld',
        type: 'get',
        data: {"username":username,"solar_system":solar_system['nodes']},
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

genesisHomeworld()