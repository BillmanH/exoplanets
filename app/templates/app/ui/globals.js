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

// coordinate makers
function pivotLocal(min,max){
    coord = {}
    coord.x = Math.floor(Math.random() * (+max + 1 - +min)) + +min;
    coord.y = Math.floor(Math.random() * (+max + 1 - +min)) + +min;
    coord.z = Math.floor(Math.random() * (+max + 1 - +min)) + +min; 
    return coord
  }

function get_specific_node_list(nodes,name){
    var mylist = []
    for (let i = 0; i < nodes.length; i++){
        if(nodes[i].hasOwnProperty(name)){
            mylist.push = nodes[i][name]
        }
    }
    return null
}

function get_specific_node(nodes,objid){
    var mylist = []
    for (let i = 0; i < nodes.length; i++){
        l = nodes[i]
        Object.keys(l).forEach(key=>{
            n = l[key]
            if(n.objid == objid){
                mylist.push(n)
            }
        }) 
    }
    return mylist
}