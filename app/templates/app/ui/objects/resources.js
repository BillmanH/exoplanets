{% load static %}

function make_tree(coord){
    var trunkHeight = 5
    var treetop = 8
    var treemat = new BABYLON.StandardMaterial("groundMat");
    var treemat2 = new BABYLON.StandardMaterial("groundMat");
    treemat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/texture_tree.png' %}");
    treemat2.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/texture_leaf.png' %}");
    var trunk = BABYLON.MeshBuilder.CreateCylinder("tree_trunk", {height:trunkHeight,diameter:2});
    var branches = BABYLON.MeshBuilder.CreateCylinder("tree_brances", {height:treetop,diameterTop:0, diameterBottom:4});
    trunk.position = new BABYLON.Vector3(coord.x, trunkHeight/2, coord.z)
    branches.position = new BABYLON.Vector3(coord.x, treetop/2+trunkHeight, coord.z) 
    trunk.material = treemat; //Place the material property of the ground
    branches.material = treemat2;
}

function build_mesh_resource(r){
    for (let i = 0; i < r.volume; i++){
        var range = ground_dimensions/2
        make_tree(pivotLocal((-1*range),range))
    }
}