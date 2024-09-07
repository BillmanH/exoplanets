{% load static %}

console.log('starmap.js loaded')
// Star
function createStar(n){
    n.diameter = 1
    n.x = 0 + n.glon
    n.y = 0 + n.gelat
    n.z = 0 + n.glat

    const star = BABYLON.MeshBuilder.CreateSphere(n.objid, {diameter: n.diameter});
    star.position = new BABYLON.Vector3(n.x, n.y, n.z);

    // light coming of star
    var sunlight = new BABYLON.PointLight("sunlight", new BABYLON.Vector3(n.x, n.y, n.z));
    const surface = new BABYLON.StandardMaterial("surface");
    surface.emissiveColor = new BABYLON.Color3(1, 1, 0);
    sunlight.diffuse = new BABYLON.Color3(0, 1, 1);
    sunlight.specular = new BABYLON.Color3(0, 1, 1);
    star.material = surface
    star.metadata = n

    star.actionManager = new BABYLON.ActionManager(scene);

    if(interactive){
        star.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function(ev){
            hoverTooltip(star)
        }));
        star.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function(ev){
            dropControlIfExists("uiTooltip")
        }));
    }
    return star
}

function createprimry_bodies(stars){
    for (let i = 0; i < stars.length; i++) {
        // console.log('star', stars[i])
        if (stars[i].hasOwnProperty('glat')){
            createStar(stars[i])
        }
    }
}

createprimry_bodies(stars)