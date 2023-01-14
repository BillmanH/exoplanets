function ajax_getActions(d){
    if(d["isIdle"]=="True"){
        $.ajax({
            url: '/ajax/pop-actions',
            type: 'get',
            data: d,
            dataType: 'json',
            beforeSend: function () {

            },
            success: function(data){
                console.log(data)
                return data
            }
        })
    }
    else {
        cnsl('object not idle')
    }
}