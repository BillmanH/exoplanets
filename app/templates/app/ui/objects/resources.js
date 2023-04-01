{% load static %}

function make_tree(coord){
    var uid = Math.floor((Math.random()) * 0x10000).toString(16)
    var trunkHeight = 3 
    var treetop = 8 + Math.floor(Math.random() * 3) + 1
    var treemat = new BABYLON.StandardMaterial("groundMat");
    var treemat2 = new BABYLON.StandardMaterial("groundMat");
    treemat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/texture_tree.png' %}");
    treemat2.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/texture_leaf.png' %}");
    var trunk = BABYLON.MeshBuilder.CreateCylinder("tree"+uid, {height:trunkHeight,diameter:2});
    var branches = BABYLON.MeshBuilder.CreateCylinder("brances"+uid, {height:treetop,diameterTop:0, diameterBottom:4+ Math.floor(Math.random() * 3) + 1});
    trunk.position = new BABYLON.Vector3(coord.x, trunkHeight/2, coord.z)
    branches.position = new BABYLON.Vector3(coord.x, treetop/2+trunkHeight, coord.z) 
    trunk.material = treemat; //Place the material property of the ground
    branches.material = treemat2;
    branches.material.specularColor = new BABYLON.Color3(0.05, 0.05, 0.05);
    // parameters - arrayOfMeshes, disposeSource, allow32BitsIndices, meshSubclass, subdivideWithSubMeshes, multiMultiMaterial
    var tree = BABYLON.Mesh.MergeMeshes([trunk, branches], true, false, undefined, false, true);
    // removeSingleCollsion(tree,"_disc")
}

function build_organic_resource(r){
    for (let i = 0; i < r.volume; i++){
        var range = ground_dimensions/2
        make_tree(pivotLocal((-1*range),range))
    }
}