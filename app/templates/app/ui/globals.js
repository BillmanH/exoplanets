
function cs(s){
    r = s.replace('_', ' ')
    return r
}

function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1) ) + min;
  }
  
function createGroundDecal(o, ground, texture, size){
    const decalMat = new BABYLON.StandardMaterial();
        decalMat.diffuseTexture = new BABYLON.Texture(texture);
        decalMat.zOffset = -1;
           
    pos = o.position
    pos.y = ground.getHeightAtCoordinates(o.position.x,o.position.z)
    // var y = ground.getHeightAtCoordinates(o.coord.x,o.coord.z)

    groundDecal = BABYLON.MeshBuilder.CreateDecal("decal",
                                                    ground,
                                                    {
                                                        position: pos,
                                                        size: new BABYLON.Vector3(size, size, size)
                                                    }
                                                    , false);

    groundDecal.material = decalMat;
    // console.log("decal", groundDecal.position, o.coord)
}

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

// eager, finds first node with matching objid or null
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

function filter_nodes_list(nodes,element, value){
    // filtering data formats like [{…},{…},{…},{…},{…},{…}]
    var mylist = []
    for (let i = 0; i < nodes.length; i++){
        if(nodes[i][element]==value){
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

var targAnimEnded = function(test) {
    console.log("targAnimEnded:", test);
}

var animateCameraTargetToObject = function(cam, speed, frameCount, pos) {
    var ease = new BABYLON.CubicEase();
    ease.setEasingMode(BABYLON.EasingFunction.EASINGMODE_EASEINOUT);
    var aable1 = BABYLON.Animation.CreateAndStartAnimation('at5', cam, 'target', speed, frameCount, cam.target, pos, 0, ease, targAnimEnded);
    aable1.disposeOnEnd = true;
}

