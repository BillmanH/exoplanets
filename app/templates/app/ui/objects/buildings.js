{% load static %} 

bulding_config = {
    "farm": {texture:"{% static 'app/objects/planet/surface/texture_farm_1.png' %}",
                height: 2,
                size: 30
            }
}


// redering natural resources
function render_block(pop,building){
    var box = BABYLON.MeshBuilder.CreateBox(pop.metadata.objid+"_box", 
    {"height":bulding_config[building.name].height,
        "size":bulding_config[building.name].size}
    );    
    box.parent = pop
    console.log(pop.position)
        box.position = new BABYLON.Vector3(pop.position.x + 10 , pop.position.y, pop.position.z + 10) 
    var boxMat = new BABYLON.StandardMaterial(pop.metadata.objid + "_groundMat");
    boxMat.diffuseTexture =  new BABYLON.Texture(bulding_config[building.name].texture);
    box.material = boxMat; 

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
    }));

    return box
}


