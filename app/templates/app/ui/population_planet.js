{% load static %}

factionbuildingHeight = 10
ground_dimensions = 5000
ground_subdivisions = 19
shinyness = 0.05

mapData = []

// light
const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(1, 1, 0));




// redering natural resources
function render_resources(resources, readyMesh){
    if (data.hasOwnProperty('resources')){
        if  (resources.length > 0){
            for (let i = 0; i < resources.length; i++){
                resource = resources[i]
                if(resource.name.toLowerCase()=="organic"){
                    build_organic_resource(resource, readyMesh)
                }
            }
        }
    }
}


function createFaction(n){
    const box = BABYLON.MeshBuilder.CreateBox(n.data.objid+"_nocol_faction", 
        {height:factionbuildingHeight,
        width:10,
        depth:10}
        );


        // console.log("ground for", n.data.lat*ground_dimensions,n.data.long*ground_dimensions,": ", 
        // readyMesh.getHeightAtCoordinates(n.data.lat*ground_dimensions,n.data.long*ground_dimensions),ground.isReady())
            
        const boxMat = new BABYLON.StandardMaterial(n.data.objid + "_groundMat");
            boxMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/skyscraper.png' %}");
            box.material = boxMat; 

        var disc = BABYLON.MeshBuilder.CreateCylinder(n.data.objid + "_disc", {diameter:50, height:1});
            disc.position.y = factionbuildingHeight/2*-1
            disc.parent = box

        const discMat = new BABYLON.StandardMaterial(n.data.objid + "_groundMat");
            discMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/city_disc.png' %}");
            disc.material = discMat; 

    
    
    var faction = BABYLON.Mesh.MergeMeshes([box, disc], true, false, undefined, false, true);
    // faction.position = new BABYLON.Vector3(n.data.lat*ground_dimensions, factionbuildingHeight/2, n.data.long*ground_dimensions)
    var x = n.data.lat*ground_dimensions
    var z = n.data.long*ground_dimensions
    var y = scene.getMeshById("ground").getHeightAtCoordinates(x,z)+(factionbuildingHeight/2)
    // faction.position = new BABYLON.Vector3(x, y+(factionbuildingHeight/2), z)
    faction.position = new BABYLON.Vector3(x, y, z)

    faction.metadata = n.data
    faction.actionManager = new BABYLON.ActionManager(scene);
    faction.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function(ev){
        hoverTooltip(faction)
    }));
    faction.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function(ev){
        dropControlIfExists("uiTooltip")
    }));
    faction.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickTrigger, function(ev){
        objectDetails(n.data)
    }));
    console.log(faction.name, x, y,z)
    console.log(faction.position)


}

function get_address(pop_loactions,iter){
    address = JSON.parse(pop_loactions)[iter+1]
    return address
}

function createPop(n){
    var faction = scene.getMeshByName(n.data.faction.objid+"_nocol_faction_merged");
    const box = BABYLON.MeshBuilder.CreateBox(n.data.population.objid+"_nocol_box", 
        {height:factionbuildingHeight*n.data.population.health,
        width:5,
        depth:5}
    );

    address = get_address(faction.metadata.pop_loactions, n.data.iter)
    n.data.population.address = address.toString()


    box.parent = faction
    box.position = new BABYLON.Vector3(address[0]*5, (factionbuildingHeight/4)*-1, address[1]*5)

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

}




// ground
const ground = BABYLON.MeshBuilder.CreateGround("ground", {height: ground_dimensions, width: ground_dimensions, subdivisions: ground_subdivisions, updatable: true})
var ground_arr = ground.getVerticesData(BABYLON.VertexBuffer.PositionKind);
var altiudes = JSON.parse(data['biome'][0]['grid'])
for (let i=0;i<altiudes.length;i++){ground_arr[(i*3)+1] = altiudes[i]*10}

console.log("altiudes: ",altiudes)
console.log('positions:', ground_arr)
ground.updateVerticesData(BABYLON.VertexBuffer.PositionKind, ground_arr);

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
        p.data.iter = j
        p.coord = pivotLocal((j+5)*-1,(j+5))
        createPop(p)
    }
}

function renderBuildings(){
    for (let i = 0; i < data.buildings.length; i++) {
        d = data.buildings[i]
        if(d.render_type=='block'){
            var owner = scene.getMeshByName(d.owner+'_nocol_box')
            render_block(owner, d)
        }
    }
}

render_resources(data['resources'], ground)
renderBuildings()
        


// ground.optimize(10)

const groundMat = new BABYLON.StandardMaterial("groundMat");
    groundMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/surface_green_2.png' %}");
    ground.material = groundMat; //Place the material property of the ground
    ground.material.specularColor = new BABYLON.Color3(shinyness, shinyness, shinyness);


