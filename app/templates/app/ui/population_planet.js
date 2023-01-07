const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(1, 1, 0));

const ground = BABYLON.MeshBuilder.CreateGround("ground", {width:500, height:500});
const groundMat = new BABYLON.StandardMaterial("groundMat");
groundMat.diffuseColor = new BABYLON.Color3(0, .6, .1);
0,154,23
ground.material = groundMat; //Place the material property of the ground

factionbuildingHeight = 10

console.log("nodes", distinct_list(data.nodes,'faction','name'))

function createFaction(n){
    const box = BABYLON.MeshBuilder.CreateBox(n.objid, {"height":factionbuildingHeight});
    box.position.y = factionbuildingHeight/2;
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