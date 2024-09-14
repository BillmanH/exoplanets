{% load static %} 

bulding_config = {
    "farmland": {texture:"{% static 'app/objects/planet/surface/texture_farm_1.png' %}",
                decaltexture:"{% static 'app/objects/planet/surface/texture_farm_1.png' %}",
                height: 2,
                decalsize: 20,
                boxsize: 10,
                from_ground:-1
            },
    "solar_panel": {texture:"{% static 'app/objects/planet/surface/solar_panels.png' %}",
        height: 2,
        boxsize: 10,
        from_ground:-1
    },
    "concrete_slab": {texture:"{% static 'app/objects/planet/surface/concrete_slab.png' %}",
        height: 3,
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

function render_mesh(pop,building){
    var metadata = pop.metadata
    if(building.type in bulding_config==false){
        conf = bulding_config["concrete_slab"]
    } else {
        conf = bulding_config[building.type]
    }
    var box = BABYLON.MeshBuilder.CreateBox(metadata.objid+"_nocol_box", 
        {"height":conf.height,
            "size":conf.boxsize}
        );
        y = scene.getMeshById("ground").getHeightAtCoordinates(pop.position.x,pop.position.z)
        box.position = new BABYLON.Vector3(pop.position.x, y + conf.from_ground, pop.position.z) 
        
        var boxMat = new BABYLON.StandardMaterial(metadata.objid + "_groundMat");
        boxMat.diffuseTexture =  new BABYLON.Texture(conf.texture);
        box.material = boxMat; 
        
        box.metadata = building
        box.metadata.ownedBy = metadata.name
        box.metadata.ownedByID = metadata.objid
        box.actionManager = new BABYLON.ActionManager(scene);
        
        createGroundDecal(pop ,ground,conf.decaltexture, conf.decalsize)
        mesh = BABYLON.SceneLoader.ImportMeshAsync("", "{% static 'app/objects/planet/surface/buildings/' %}", "/oil_well.glb");
        console.log("mesh: ", mesh)
        
        box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function(ev){
            hoverTooltip(box)
        }));
        box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function(ev){
            dropControlIfExists("uiTooltip")
        }));
        box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickTrigger, function(ev){
            objectDetails(box.metadata)
            animateCameraTargetToObject(camera, camera_pan_speed,200, box.getAbsolutePosition())
            console.log("box: ", box.position, pop.position)
        }));
        
        pop.dispose()
    return box
}


function render_block(pop,building){
    console.log("bld: ", building.type)
    if(building.type in bulding_config==false){
        conf = bulding_config["concrete_slab"]
    } else {
        conf = bulding_config[building.type]
    }
    pop_decal = pop.metadata.objid + "_decal"
    if(scene.getMeshByName(pop_decal)){
        scene.getMeshByName(pop_decal).dispose()
    }
    var box = BABYLON.MeshBuilder.CreateBox(pop.metadata.objid+"_nocol_box", 
    {"height":conf.height,
        "size":conf.boxsize}
    );    
    // box.parent = pop
    y = scene.getMeshById("ground").getHeightAtCoordinates(pop.position.x,pop.position.z)
    box.position = new BABYLON.Vector3(pop.position.x, y + conf.from_ground, pop.position.z) 

    var boxMat = new BABYLON.StandardMaterial(pop.metadata.objid + "_groundMat");
    boxMat.diffuseTexture =  new BABYLON.Texture(conf.texture);
    box.material = boxMat; 


    createGroundDecal(pop ,ground,conf.decaltexture, conf.decalsize)

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
        dropAllControls()
        animateCameraTargetToObject(camera, camera_pan_speed,200, box.getAbsolutePosition())
        console.log("box: ", box.position, pop.position)
    }));
    pop.dispose()

    return box
}


