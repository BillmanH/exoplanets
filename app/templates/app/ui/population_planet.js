{% load static %}

factionbuildingHeight = 10
ground_dimensions = 500
shinyness = 0.05



// light
const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(1, 1, 0));

// ground
const ground = BABYLON.MeshBuilder.CreateGround("ground", {width:ground_dimensions, height:ground_dimensions});
const groundMat = new BABYLON.StandardMaterial("groundMat");
    groundMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/surface_green_2.png' %}");
    ground.material = groundMat; //Place the material property of the ground
    ground.material.specularColor = new BABYLON.Color3(shinyness, shinyness, shinyness);

// center
const center = BABYLON.MeshBuilder.CreateBox("center", {"height":20,"size":1})
    center.isVisible = false


// redering natural resources
function render_resources(resources){
    if (data.hasOwnProperty('resources')){
        if  (resources.length > 0){
            for (let i = 0; i < resources.length; i++){
                resource = resources[i]
                if(resource.name.toLowerCase()=="organic"){
                    build_organic_resource(resource)
                }
            }
        }
    }
}

render_resources(data['resources'])

function createFaction(n){
    const box = BABYLON.MeshBuilder.CreateBox(n.data.objid+"_box", 
        {"height":factionbuildingHeight,
        "size":10}
      );
      box.parent = center
      box.position = new BABYLON.Vector3(n.coord.x, factionbuildingHeight/2, n.coord.z) 
      const boxMat = new BABYLON.StandardMaterial(n.data.objid + "_groundMat");
      boxMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/skyscraper.png' %}");
      box.material = boxMat; 
      
    var disc = BABYLON.MeshBuilder.CreateCylinder(n.data.objid + "_disc", {diameter:50, height:1});
        disc.position.y = factionbuildingHeight/2*-1
        disc.parent = box
    const discMat = new BABYLON.StandardMaterial(n.data.objid + "_groundMat");
        discMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/city_disc.png' %}");
        disc.material = discMat; 

        
    box.metadata = n.data
    box.actionManager = new BABYLON.ActionManager(scene);
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function(ev){
        hoverTooltip(box)
    }));
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function(ev){
        dropControlIfExists("uiTooltip")
    }));
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickTrigger, function(ev){
        objectDetails(n.data)
    }));

    // removeCollidingMesh(n.data.objid + "_disc","tree_trunk")
    // removeCollidingMesh(n.data.objid + "_disc","tree_brances")
}

function createPop(n){
    var faction = scene.getMeshByName(n.data.faction.objid+"_box");
    const box = BABYLON.MeshBuilder.CreateBox(n.data.population.objid+"_box", 
        {"height":factionbuildingHeight/2,
        "size":5}
    );
    box.parent = faction
    box.position = new BABYLON.Vector3(n.coord.x + 5, factionbuildingHeight/4*-1, n.coord.z + 5) 
    var phi = Math.random() * 2 * Math.PI; 
    box.rotation.y = phi;

    const boxMat = new BABYLON.StandardMaterial(n.data.population.objid + "_groundMat");
        boxMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/skyscraper_2.png' %}");
        box.material = boxMat; 

    box.metadata = n.data.population
    box.actionManager = new BABYLON.ActionManager(scene);
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function(ev){
        hoverTooltip(box)
    }));
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function(ev){
        dropControlIfExists("uiTooltip")
    }));
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickTrigger, function(ev){
        objectDetails(n.data.population)
    }));
    // removeCollidingMesh(box.name,"tree_trunk")
}


// main - actually loads the content
var guiIter = 0
factions = distinct_list(data.nodes,'faction','objid')

for (let i = 0; i < factions.length; i++) {
    guiIter ++
    f = {}
    f.data = get_specific_node(data.nodes,factions[i])[0]   
    f.iter = guiIter
    pops = filter_nodes_res(data.nodes,'faction','name', f.data.name)
    f.coord = {
        x:f.data.lat*ground_dimensions,
        y:0,
        z:f.data.lat*ground_dimensions
    }
    // console.log(f.coord)
    createFaction(f)

    for (let j = 0; j < pops.length; j++) {
        p = {}
        p.data = pops[j]
        p.coord = pivotLocal((j+5)*-1,(j+5))
        createPop(p)
    }
  }

  
removeCollidingMesh("_disc","tree")
// removeCollidingMesh("_box","tree")
// farm_building = {name:'farm',
//             objtype:'building'}
// // pop = scene.getMeshByName("2065545354087"+"_box")
// pop = scene.getMeshByName("6225371037165"+"_box")
  
// building = render_block(pop,farm_building)
// console.log(building)


// Goals: 
// https://doc.babylonjs.com/features/featuresDeepDive/mesh/creation/set/height_map