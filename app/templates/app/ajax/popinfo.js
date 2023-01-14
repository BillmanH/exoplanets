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
                console.log(data)
                plz = dashboard.getControlByName("loadingpleasewait")
                plz.dispose()
                return data
            }
        })
    }
    else {
        cnsl('object not idle')
    }
}