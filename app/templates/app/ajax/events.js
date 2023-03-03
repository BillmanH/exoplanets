function ajax_get_local_events(d){
    return $.ajax({
            url: '/ajax/get-local-events',
            type: 'get',
            data: d,
            dataType: 'json',
            beforeSend: function () {
                plz = pleaseWaiter(dashboard)
            },
            success: function(data){
                data.location = d
                console.log('ajax/get-local-events', data)
            }
        })
}