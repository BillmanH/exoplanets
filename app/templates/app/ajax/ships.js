// upon selectingt a ship, this function will pull up a menu allows the user to select a launch target
// and launch the ship
function search_for_target(text, ship, ship_launch_control){
    var d = {"text":text, "ship":JSON.stringify(ship)}
    console.log("ship: ",ship, " text: ", text)
    $.ajax({
        url: '/ajax/search-for-target',
        type: 'get',
        data: d,
        dataType: 'json',
        beforeSend: function () {
            plz = pleaseWaiter(dashboard)
        },
        success: function(data){
            plz = dashboard.getControlByName("loadingpleasewait")
            plz.dispose()
            console.log("possible_targets: ",data)
            possible_targets = data.possible_targets
            for (let i = 0; i < possible_targets.length; i++) {
                f = {}
                f.data = possible_targets[i]
                f.gui = {buttonColor:"white",
                    depth:1}
                f.iter = i+1
                f.gui.text_button = true
                f.gui.displayed_values = ["objtype","name","orbitsDistance"]
                f.gui.clickButton = function(f ) {
                    console.log(f.data.name, " button was pushed")
                    objectDetails(f.data)
                    calculate_prelaunch(ship, f.data)
                };
                addButtonToBox(f,ship_launch_control)
            }        
        },      
        error: function(data){
            console.log(data)
        }
    });
    
}

function calculate_prelaunch(ship, target){
    var d = {"ship":JSON.stringify(ship), "target":JSON.stringify(target)}
    console.log("ship: ",ship, " target: ", target)
    $.ajax({
        url: '/ajax/calculate-prelaunch',
        type: 'get',
        data: d,
        dataType: 'json',
        beforeSend: function () {
            plz = pleaseWaiter(dashboard)
        },
        success: function(data){
            plz = dashboard.getControlByName("loadingpleasewait")
            plz.dispose()
            console.log("prelaunch data: ",data)
            objectDetails(ship)
        },      
        error: function(data){
            console.log(data)
        }
    });
}