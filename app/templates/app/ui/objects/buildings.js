{% load static %} 

bulding_config = {
    "farmland": {texture:"{% static 'app/objects/planet/surface/texture_farm_1.png' %}",
                height: 1,
                decalsize: 20,
                boxsize: 10,
                from_ground:-1
            },
    "solar_panel": {texture:"{% static 'app/objects/planet/surface/solar_panels.png' %}",
        height: 1,
        decalsize: 20,
        boxsize: 10,
        from_ground:-1
    }
}

buildings_control_panel = {
    name:"buildings_window",
    title: "Available Buildings:",
    top:20,
    left:80,
    width:"600px",
    height:"400px"
}

function buildings_window(response){
    dropAllControls()
    var buildings_control = createControlBox(buildings_control_panel)
    for (let i = 0; i < response.buildings.length; i++) {
        f = {}
        f.data = response.buildings[i]
        f.gui = {buttonColor:"white",
            depth:1}
        f.iter = i+1
        f.gui.text_button = true
        f.gui.displayed_values = ["description","effort"]
        f.gui.clickButton = function(f) {
            console.log(f.data.type, " button was pushed")
            objectDetails(f.data)
            takeBuildingAction(response.pop,f.data)
        };
        addButtonToBox(f,buildings_control)
    }
}




function render_block(pop,building,ground){
    var box = BABYLON.MeshBuilder.CreateBox(pop.metadata.objid+"_nocol_box", 
    {"height":bulding_config[building.name].height,
        "size":bulding_config[building.name].boxsize}
    );    
    // box.parent = pop
    y = scene.getMeshById("ground").getHeightAtCoordinates(pop.position.x,pop.position.z)
    box.position = new BABYLON.Vector3(pop.position.x, y + bulding_config[building.name].from_ground, pop.position.z) 

    var boxMat = new BABYLON.StandardMaterial(pop.metadata.objid + "_groundMat");
    boxMat.diffuseTexture =  new BABYLON.Texture(bulding_config[building.name].texture);
    box.material = boxMat; 


    createGroundDecal(pop ,ground,bulding_config[building.name].texture, bulding_config[building.name].decalsize)

    box.metadata = building
    box.metadata.ownedBy = pop.metadata.name
    box.metadata.ownedByID = pop.metadata.objid
    box.actionManager = new BABYLON.ActionManager(scene);
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function(ev){
        hoverTooltip(box)
    }));
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function(ev){
        dropControlIfExists("uiTooltip")
    }));
    box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickTrigger, function(ev){
        objectDetails(box.metadata)
        console.log("box: ", box.position, pop.position)
    }));

    return box
}


