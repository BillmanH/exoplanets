factionbuildingHeight = 10

// light
const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(1, 1, 0));

// ground
const ground = BABYLON.MeshBuilder.CreateGround("ground", {width:500, height:500});
const groundMat = new BABYLON.StandardMaterial("groundMat");
groundMat.diffuseColor = new BABYLON.Color3(0, .6, .1);
ground.material = groundMat; //Place the material property of the ground

// center
const center = BABYLON.MeshBuilder.CreateBox("center", {"height":100,"size":1})


function createFaction(n){
    const box = BABYLON.MeshBuilder.CreateBox(n.objid, 
        {"height":factionbuildingHeight,
        "size":5}
      );
      box.parent = center
      coord = pivotLocal()
      box.position = new BABYLON.Vector3(coord.x, factionbuildingHeight/2, coord.z) 
}

function createPop(){

}

var guiIter = 0
factions = distinct_list(data.nodes,'faction','name')
for (let i = 0; i < factions.length; i++) {
    f = factions[i]
    pops = filter_nodes_res(data.nodes,'faction','name', f)
    createFaction(f)
    for (let i = 0; i < pops.length; i++) {

    }

  }

// Goals: 
// https://doc.babylonjs.com/features/featuresDeepDive/mesh/creation/set/height_map