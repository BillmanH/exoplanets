function ajax_get_local_resources(d){
    return $.ajax({
            url: '/ajax/get-local-resources',
            type: 'get',
            data: d,
            dataType: 'json',
            beforeSend: function () {
                plz = pleaseWaiter(dashboard)
            },
            success: function(data){
                data.location = d
                console.log('ajax/get-local-resources', data)
            }
        })
}