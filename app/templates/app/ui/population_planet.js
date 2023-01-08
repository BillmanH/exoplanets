{% load static %}
factionbuildingHeight = 10

// light
const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(1, 1, 0));

// ground
const ground = BABYLON.MeshBuilder.CreateGround("ground", {width:500, height:500});
const groundMat = new BABYLON.StandardMaterial("groundMat");
groundMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/surface_green.png' %}");
ground.material = groundMat; //Place the material property of the ground

// center
const center = BABYLON.MeshBuilder.CreateBox("center", {"height":20,"size":1})


function createFaction(n){
    const box = BABYLON.MeshBuilder.CreateBox(n.objid+"box", 
        {"height":factionbuildingHeight,
        "size":5}
      );
      box.parent = center
      box.position = new BABYLON.Vector3(n.coord.x, factionbuildingHeight/2, n.coord.z) 
      const boxMat = new BABYLON.StandardMaterial(n.objid + "_groundMat");
      boxMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/skyscraper.png' %}");
      box.material = boxMat; 
      
    var disc = BABYLON.MeshBuilder.CreateCylinder("disc", {diameter:50, height:1});
        disc.position.y = factionbuildingHeight/2*-1
        disc.parent = box
    const discMat = new BABYLON.StandardMaterial(n.objid + "_groundMat");
        discMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/city_disc.png' %}");
        disc.material = discMat; 
}

function createPop(n,f){
    var orbiting = scene.getMeshByName(f.objid+"box");
    const box = BABYLON.MeshBuilder.CreateBox(n.objid+"box", 
        {"height":factionbuildingHeight/2,
        "size":5}
    );
    box.parent = orbiting
    box.position = new BABYLON.Vector3(n.coord.x, factionbuildingHeight/4*-1, n.coord.z) 
    var phi = Math.random() * 2 * Math.PI; 
    box.rotation.y = phi;

    const boxMat = new BABYLON.StandardMaterial(n.objid + "_groundMat");
        boxMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/skyscraper_2.png' %}");
        box.material = boxMat; 
}



var guiIter = 0
factions = distinct_list(data.nodes,'faction','objid')
console.log(factions)
for (let i = 0; i < factions.length; i++) {
    f = get_specific_node(data.nodes,factions[i])[0]   
    pops = filter_nodes_res(data.nodes,'faction','name', f.name)
    console.log(pops)
    f.coord = pivotLocal(-150,150)
    createFaction(f)
    for (let j = 0; j < pops.length; j++) {
        p = pops[j]
        p.coord = pivotLocal(-15,15)
        createPop(p,f)
    }

  }

// Goals: 
// https://doc.babylonjs.com/features/featuresDeepDive/mesh/creation/set/height_map