function get_values(l,v){
    var mylist = []
    for (let i = 0; i < l.length; i++){
        if(l[i][v]!=undefined){
            mylist.push(l[i][v])
        }
    } 
    return mylist
}