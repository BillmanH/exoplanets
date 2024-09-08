{% load static %}

factionbuildingHeight = 10
factionbuildingWidth = 10
ground_dimensions = 5000
ground_subdivisions = 19
shinyness = 0.05
camera_pan_speed = 200

mapData = []

// light
const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(1, 1, 0));



// redering natural resources
function render_resources(resources, readyMesh){
    if (data.hasOwnProperty('resources')){
        if  (resources.length > 0){
            for (let i = 0; i < resources.length; i++){
                resource = resources[i]
                if(resource.name.toLowerCase()=="organics"){
                    build_organic_resource(resource, readyMesh)
                }
            }
        }
    }
}


function createFaction(n){
    const box = BABYLON.MeshBuilder.CreateBox(n.data.objid+"_nocol_faction", 
        {height:factionbuildingHeight,
        width:factionbuildingWidth,
        depth:factionbuildingWidth}
        );


        // console.log("ground for", n.data.lat*ground_dimensions,n.data.long*ground_dimensions,": ", 
        // readyMesh.getHeightAtCoordinates(n.data.lat*ground_dimensions,n.data.long*ground_dimensions),ground.isReady())
            
    const boxMat = new BABYLON.StandardMaterial(n.data.objid + "_groundMat");
        boxMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/skyscraper.png' %}");
        box.material = boxMat; 

    var faction = BABYLON.Mesh.MergeMeshes([box], true, false, undefined, false, true);
    var x = n.data.lat*ground_dimensions
    var z = n.data.long*ground_dimensions
    var y = scene.getMeshById("ground").getHeightAtCoordinates(x,z)+(factionbuildingHeight/2)   
    n.position = new BABYLON.Vector3(x, y, z)
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
        dropAllControls()
        // console.log(faction.position)
        objectDetails(n.data)
        pops = getObjectChildren(n.data.objid,'faction')
        console.log(pops)
        animateCameraTargetToObject(camera, camera_pan_speed,200, faction.getAbsolutePosition())
        make_faction_ui(n.data)
    }));

}



function createPop(n){
    // console.log('pop:', n)
    var faction = scene.getMeshByName(n.data.faction.objid+"_nocol_faction_merged");
    var trueBuildHeight = (factionbuildingHeight*n.data.population.health)
    const box = BABYLON.MeshBuilder.CreateBox(n.data.population.objid+"_nocol_box", 
        {height:trueBuildHeight,
        width:4,
        depth:4}
    );

    // box.parent = faction
    n.data.population.x = faction.position.x + n.coord.x 
    n.data.population.z = faction.position.z + n.coord.z
    n.data.population.y = scene.getMeshById("ground").getHeightAtCoordinates(n.data.population.x,n.data.population.z) + (trueBuildHeight/2)
    
    n.position = new BABYLON.Vector3(n.data.population.x,n.data.population.y, n.data.population.z)

    box.position = n.position
    const boxMat = new BABYLON.StandardMaterial(n.data.population.objid + "_groundMat");
        boxMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/skyscraper_2.png' %}");
        if (n.data.population.isIdle=='false'){
            boxMat.diffuseColor = new BABYLON.Color3(.9,0,.1)
        }
        box.material = boxMat; 

    box.metadata = n.data.population
    box.metadata.coords = [n.data.population.x,n.data.population.y, n.data.population.z].toString()
    box.actionManager = new BABYLON.ActionManager(scene);
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function(ev){
        hoverTooltip(box)
    }));
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function(ev){
        dropControlIfExists("uiTooltip")
    }));
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickTrigger, function(ev){
        console.log("clicked population: ",n.data.population)
        objectDetails(n.data.population)
        animateCameraTargetToObject(camera, camera_pan_speed,200, box.getAbsolutePosition())
        if (n.data.population['isIdle']=='false'){
            console.log(n.data.population['objid'], ' is not idle')
            action = get_current_action(n.data.population)
            console.log(action)
        } else {
            get_available_controls(box,n.data.population)
        }
    }));

}




// ground
const ground = BABYLON.MeshBuilder.CreateGround("ground", {height: ground_dimensions, width: ground_dimensions, subdivisions: ground_subdivisions, updatable: true})
var ground_arr = ground.getVerticesData(BABYLON.VertexBuffer.PositionKind);
var altiudes = JSON.parse(data['biome'][0]['grid'])
for (let i=0;i<altiudes.length;i++){ground_arr[(i*3)+1] = altiudes[i]*10}

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
        x:(f.data.lat*ground_dimensions), 
        y:0,
        z:(f.data.lat*ground_dimensions) + (factionbuildingWidth/2)
    }
    // console.log(faction,f.coord)
    createFaction(f)
    createGroundDecal(f,ground,"{% static 'app/objects/planet/surface/planet_city_decal.png' %}",25)
    for (let j = 0; j < pops.length; j++) {
        p = {}
        p.data = pops[j]
        p.data.iter = j
        var pop_margin = 5
        var pop_spread = (((j+pops.length)/2) + pop_margin)
        p.coord = pivotLocal(pop_spread*-1,pop_spread, pop_margin)
        createPop(p)
        createGroundDecal(p,ground,"{% static 'app/objects/planet/surface/planet_city_decal.png' %}", 20 * p.data.population.industry)
    }
}

function renderBuildings(ground){
    // Buildings attached to pops, not pops themselves. 
    for (let i = 0; i < data.buildings.length; i++) {
        d = data.buildings[i]
        if(d.render_type=='block'){
            var owner = scene.getMeshByName(d.owner+'_nocol_box')
            render_block(owner, d)
        } else if(d.render_type=='mesh'){
            render_mesh(owner, d,)
        }
    }
}

render_resources(data['resources'], ground)
renderBuildings(ground)
        


// ground.optimize(10)

const groundMat = new BABYLON.StandardMaterial("groundMat");
    groundMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/surface_green_2.png' %}");
    ground.material = groundMat; //Place the material property of the ground
    ground.material.specularColor = new BABYLON.Color3(shinyness, shinyness, shinyness);


