// Takes an (agent) and an (action)
function takeAction(p,a){
    var d = {"agent":p,
        "action":a}
    cnsl(d)
    $.ajax({
        url: '/ajax/take-action',
        type: 'get',
        data: { 'values' : JSON.stringify(d) },
        dataType: 'json',
        beforeSend: function () {
            plz = pleaseWaiter(dashboard)
        },
        success: function(data){
            document.location.reload()
        },
        error: function(data){
            cnsl(data)
        }
    });
}

function takeBuildingAction(p,b){
    var d = {"agent":p,
        "building":b}
    cnsl(d)
    $.ajax({
        url: '/ajax/take-building-action',
        type: 'get',
        data: { 'values' : JSON.stringify(d) },
        dataType: 'json',
        beforeSend: function () {
            plz = pleaseWaiter(dashboard)
        },
        success: function(data){
            document.location.reload()
        },
        error: function(data){
            cnsl(data)
        }
    });
}