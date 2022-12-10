// const planet = BABYLON.SceneLoader.Append("static/app/objects/", "planet.gltf", scene, function (scene) { });
// https://doc.babylonjs.com/typedoc/classes/BABYLON.SceneLoader#Append
{% load static %}

star_base = 10

function createStar(n){
    const star = BABYLON.MeshBuilder.CreateSphere(n.name, {diameter: star_base});
    const surface = new BABYLON.StandardMaterial("{% static 'app/objects/star.jpg' %}");
    star.material = surface
    return star
}

function createPlanet(n){
    const planet = BABYLON.MeshBuilder.CreateSphere(n.name,  {diameter: scale_radius(n.radius)});
    planet.position = new BABYLON.Vector3(scale_distance(Math.random()),0,scale_distance(n.orbitsDistance));

    // GUI
    var advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI");
    advancedTexture.idealWidth = 600;
    
    var rect1 = new BABYLON.GUI.Rectangle();
        rect1.width = .06;
        rect1.height = .03;
        rect1.cornerRadius = 10;
        rect1.color = "white";
        rect1.thickness = 4;
        rect1.background = "black";
        advancedTexture.addControl(rect1);
        rect1.linkWithMesh(planet);   
        rect1.linkOffsetY = -15;

    var label = new BABYLON.GUI.TextBlock();
        label.text = n.name;
        rect1.addControl(label);    
}

for (let i = 0; i < solar_system.nodes.length; i++) {
    n = solar_system["nodes"][i]
    if (n["objtype"]=="star"){
        createStar(n)
    }
    if (n["objtype"]=="planet"){
        createPlanet(n)
    }
  }


