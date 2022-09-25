
function getNewsFeed (){
    $.ajax({
        url: '/ajax/newsfeed',
        type: 'get',
        data: {},
        dataType: 'json',
        beforeSend: function () {
            d3.selectAll('#newsfeed').remove()
        },
        success: function(data){
            console.log(data)
            if (data['error'] == 'no actions returned'){
            }
            else {
                console.log(data)
                // draw_table(
                //     "newsfeed",
                //     data,
                //     titles,  // an array of values that you want shown
                //     tableClickHandler = function(d){console.log(d)} // default function to handle hover 
                // )
            }
        }
    })
}