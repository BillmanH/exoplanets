function get_values(l,v,t){
    /// l = list; v = value to return; t = type to filter on; 
    var mylist = []
    for (let i = 0; i < l.length; i++){
        if(l[i][v]!=undefined & l[i]["objtype"]==t){
            mylist.push(l[i][v])
        }
    } 
    return mylist
}

function get_node(nodes,oid){
    for (let i = 0; i < nodes.length; i++){
        if(nodes[i].objid==oid){
            return nodes[i]
        }
    }
    return null
}