{% load static %} 

bulding_config = {
    "farmland": {box_texture:"{% static 'app/objects/planet/surface/texture_farm_1.png' %}",
                decal_texture:"{% static 'app/objects/planet/surface/texture_farm_1.png' %}",
                box_height: 2,
                decal_size: 20,
                box_size: 10,
                box_height_from_ground:-1
            },
    "solar_panel": {box_texture:"{% static 'app/objects/planet/surface/solar_panels.png' %}",
        box_height: 3,
        box_size: 10,
        box_height_from_ground:-1
    },
    "concrete_slab": {box_texture:"{% static 'app/objects/planet/surface/concrete_slab.png' %}",
        box_height: 3,
        box_size: 10,
        box_height_from_ground:-1
    },
    "oil_well": {box_texture:"{% static 'app/objects/planet/surface/concrete_slab.png' %}",
        box_height: 3,
        box_size: 10,
        box_height_from_ground:-1,
        cone_height: 5,
        cone_color: "black",
        cone_diameter: 2
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


function render_building(pop,building){
    console.log("render_building: ", pop, building)
    if(building.type in bulding_config==false){
        conf = bulding_config["concrete_slab"]
        console.log("building type not found: ", building.type)
    } else {
        conf = bulding_config[building.type]
    }
    pop_decal = pop.metadata.objid + "_decal"
    if(scene.getMeshByName(pop_decal)){
        scene.getMeshByName(pop_decal).dispose()
    }
    // get the altitude of the pop
    y = scene.getMeshById("ground").getHeightAtCoordinates(pop.position.x,pop.position.z)

    // box component
    var box = BABYLON.MeshBuilder.CreateBox(pop.metadata.objid+"bld_nocol_box", 
    {"height":conf.box_height,
        "size":conf.box_size}
    );    
    box.position = new BABYLON.Vector3(pop.position.x, y + conf.box_height_from_ground, pop.position.z) 

    var boxMat = new BABYLON.StandardMaterial(pop.metadata.objid + "bld_groundMat");
    boxMat.diffuseTexture =  new BABYLON.Texture(conf.box_texture);
    box.material = boxMat; 

    // ground decal component
    if (conf.decal_texture != undefined){
        createGroundDecal(pop ,ground,conf.decal_texture, conf.decal_size)
    }

    // cone component
    if (conf.cone_height != undefined){
        var cone = BABYLON.MeshBuilder.CreateCylinder(pop.metadata.objid+"bld_nocol_cone", {height: conf.cone_height, diameter : conf.cone_diameter});
        cone.position = new BABYLON.Vector3(pop.position.x, y, pop.position.z) 
        cone.material = new BABYLON.StandardMaterial(pop.metadata.objid + "bld_groundMat");
        cone.material.diffuseColor = BABYLON.Color3.FromHexString(conf.cone_color)
        console.log("cone: ", cone)
    }


    // metadata and actionmanager   
    box.metadata = {}
    box.metadata.building = building
    box.metadata.pop = pop.metadata

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
        objectDetails(box.metadata.pop)
        animateCameraTargetToObject(camera, camera_pan_speed,200, box.getAbsolutePosition())
        building_controls(box)
    }));
    pop.dispose()

    return box
}

function building_controls(box){
    generic_control = {
        name:"building_window",
        title: "Building: " + box.metadata.building.name,
        top:20,
        left:80,
        width:"400px",
        height:"400px"
    }
    dropAllControls()
    console.log("building_controls: ", box.metadata)
    generic_control.title = "Building: \n" + dictToSimpleText(box.metadata.building)
    current_building_control = createControlBox(generic_control)
    
    f = {}
    f.gui = {buttonColor:"white", depth:0, top: 300}
    f.metadata = box.metadata.building
    f.data = {name:"remove", "objid":box.metadata.building.objid}
    f.iter = 4
    f.gui.clickButton = function(f) {building_remove(box.metadata.building)};
    addButtonToBox(f,current_building_control)

    if (box.metadata.building.actions != undefined){
        for(let i = 0; i < box.metadata.building.actions.length; i++){
            f = {}
            f.gui = {buttonColor:"white", depth:0, top: 300}
            f.metadata = box.metadata.building
            f.data = box.metadata.building.actions[i]
            f.iter = 4
            f.gui.clickButton = function(f) {

            }
            addButtonToBox(f,current_building_control)
        }
    }
}
