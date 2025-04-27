// upon selectingt a ship, this function will pull up a menu allows the user to select a launch target
// and launch the ship
function search_for_target(text, ship){
    var d = {"text":text, "ship":ship}
    console.log("ship: ",ship, " text: ", text)
    $.ajax({
        url: '/ajax/search-for-target',
        type: 'get',
        data: JSON.stringify(d),
        dataType: 'json',
        beforeSend: function () {
            plz = pleaseWaiter(dashboard)
        },
        success: function(data){
            dropAllControls()
            document.location.reload()
        },
        error: function(data){
            console.log(data)
        }
    });
    
}