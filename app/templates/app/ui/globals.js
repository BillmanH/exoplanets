// filtering data formats like [{},{},{}]
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

// filtering data formats like [{location: {…}, population: {…}, faction: {…}, species: {…}}]
function filter_nodes_res(nodes,element,field, value){
    // element = 'location', field = 'isPopulated', value = 'true'
    var mylist = []
    for (let i = 0; i < nodes.length; i++){
        if(nodes[i][element][field]!=undefined & nodes[i][element][field]==value){
            mylist.push(nodes[i])
        }
    } 
    return mylist
}

function distinct_list(nodes,element,field){
    var mylist = []
    for (let i = 0; i < nodes.length; i++){
        if(nodes[i][element][field]!=undefined & mylist.indexOf(nodes[i][element][field]) === -1){
            mylist.push(nodes[i][element][field])
        }
    }     
    return mylist
}