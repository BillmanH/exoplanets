{% load static %} 
{% include "app/ajax/building_action.js" %}

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
    bottom_of_controls = 200
    generic_control = {
        name:"building_window",
        title: "Building: " + box.metadata.building.name,
        top:20,
        left:80,
        width:"400px",
        height:"400px"
    }
    dropAllControls()
    console. log("building_controls: ", box.metadata)
    generic_control.title = "Building: \n" + dictToSimpleText(box.metadata.building)
    current_building_control = createControlBox(generic_control)
    
    // Remove button is always available
    f = {}
    f.gui = {buttonColor:"white", depth:0, top: bottom_of_controls}
    f.metadata = box.metadata.building
    f.data = {name:"remove", "objid":box.metadata.building.objid}
    f.iter = 4
    f.gui.clickButton = function(f) {building_remove(box.metadata.building)};
    addButtonToBox(f,current_building_control)

    if(box.metadata.building.has_buttons != undefined){
        building_buttons = box.metadata.building.has_buttons.slice(1, -1).split(",");
        console.log("building_buttons: ", building_buttons)
        for(let i = 0; i < building_buttons.length; i++){
            f = {}
            f.gui = {buttonColor:"white", depth:0, top: bottom_of_controls+(i+1)*40}
            f.data = {}
            f.data['name'] = stringCleaner(building_buttons[i])
            f.gui['buttonName'] = stringCleaner(building_buttons[i])
            f.iter = i
            f.gui.clickButton = function(f) {
                building_take_action(box.metadata.building, building_buttons[i])
                console.log("building button clicked: ", f) 
            }
            addButtonToBox(f,current_building_control)
        }

    }
}

function show_inventory(building,inventory){
    console.log("show_inventory: ", building, inventory)
    dropAllControls()
    generic_control = {
        name:"inventory_window",
        title: "Inventory: " + building['name'],
        top:20,
        left:80,
        width:"400px",
        height:"400px"
    }
    current_building_control = createControlBox(generic_control)
    for (let i = 0; i < inventory.length; i++) {
        f = {}
        f.data = inventory[i]
        f.gui = {buttonColor:"white",
            depth:1}
        f.iter = i+1
        f.gui.text_button = true
        f.gui.displayed_values = ["objtype","type","name","speed"]
        f.gui.clickButton = function(f) {
            console.log(f.data.type, " button was pushed")
            objectDetails(f.data)
            //TODO: take action on inventory item
        };
        addButtonToBox(f,current_building_control)
    }
}
