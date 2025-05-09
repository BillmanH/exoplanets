// Takes an (agent) and an (action)
function building_take_action(building, action){
    var d = {"agent":building,
        "action":action}
    cnsl(d)
    $.ajax({
        url: '/ajax/building-take-action',
        type: 'get',
        data: { 'values' : JSON.stringify(d) },
        dataType: 'json',
        beforeSend: function () {
            plz = pleaseWaiter(dashboard)
        },
        success: function(data){
            dropAllControls()
            // document.location.reload()
            console.log("results: ",data)
            if (data['result'] == false){
                building['status'] = "unable to build: " + data['message'] 
            } else if (data['result'] == 'valid: Building has inventory'){
                show_inventory(building,data['stored_objects'])
            } else {
                building['status'] = "building: " + data['job']
            }
            objectDetails(building)
        },
        error: function(data){
            console.log(data)
        }
    });
}



function building_remove(b){
    var d = {"building":b}
    cnsl("buildign being removed: ",d)
    $.ajax({
        url: '/ajax/remove-building-action',
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
