function ajax_get_resources(d){
    if(d["isIdle"].toLowerCase()=="true"){
        $.ajax({
            url: '/ajax/get-resources',
            type: 'get',
            data: d,
            dataType: 'json',
            beforeSend: function () {
                plz = pleaseWaiter(dashboard)
            },
            success: function(data){
                plz = dashboard.getControlByName("loadingpleasewait")
                plz.dispose()
                data.pop = d
                console.log(data)
                // make_actions_box(data)
                return data
            }
        })
    }
    else {
        console.log('object not idle')
    }
}