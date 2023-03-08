function prep_actions(o){
    console.log("agent: ",o)
    res = ajax_getActions(o.data)

}

function ajax_getActions(d){
    if(d["isIdle"].toLowerCase()=="true"){
        $.ajax({
            url: '/ajax/get-actions',
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
                make_actions_box(data)
                return data
            }
        })
    }
    else {
        console.log('object not idle')
    }
}

function ajax_getBuildings(d){
    if(d["isIdle"].toLowerCase()=="true"){
        $.ajax({
            url: '/ajax/get-possible-buildings',
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
                make_actions_box(data)
                return data
            }
        })
    }
    else {
        console.log('object not idle')
    }
}