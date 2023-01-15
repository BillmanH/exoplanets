function ajax_getActions(d){
    if(d["isIdle"]=="True"){
        $.ajax({
            url: '/ajax/pop-actions',
            type: 'get',
            data: d,
            dataType: 'json',
            beforeSend: function () {
                plz = pleaseWaiter(dashboard)
            },
            success: function(data){
                plz = dashboard.getControlByName("loadingpleasewait")
                plz.dispose()
                console.log(data)
                make_actions_screen(data)
                return data
            }
        })
    }
    else {
        console.log('object not idle')
    }
}