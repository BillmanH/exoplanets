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
            dropAllControls()
            document.location.reload()
        },
        error: function(data){
            cnsl(data)
        }
    });
}

function get_current_action(p){
    var d = {"agent":p}
    $.ajax({
        url: '/ajax/get-current-action',
        type: 'get',
        data: { 'values' : JSON.stringify(d) },
        dataType: 'json',
        beforeSend: function () {
            plz = pleaseWaiter(dashboard)
        },
        success: function(data){
            dropAllControls()
            console.log(data)
            make_current_action_box(actions_control_panel, data['current_action'])
        },
        error: function(data){
            console.log(data)
        }
    });
}

function constructBuilding(p,b){
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
            dropAllControls()
            document.location.reload()
        },
        error: function(data){
            cnsl(data)
        }
    });
}