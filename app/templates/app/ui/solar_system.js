// const planet = BABYLON.SceneLoader.Append("static/app/objects/", "planet.gltf", scene, function (scene) { });
// https://doc.babylonjs.com/typedoc/classes/BABYLON.SceneLoader#Append
{% load static %}

sphere_textures = {
    "G":"{% static 'app/objects/planet/star_g.png' %}",
    "terrestrial":"{% static 'app/objects/planet/terrestrial_oceanic.png' %}",
    "dwarf":"{% static 'app/objects/planet/dwarf.png' %}",
    "gas":"{% static 'app/objects/planet/gas_giant_blue.png' %}",
    "ice":"{% static 'app/objects/planet/ice.png' %}",
}

star_base = 100
shinyness = 0.05

function createStar(n){
    const star = BABYLON.MeshBuilder.CreateSphere(n.name, {diameter: star_base});
    var sunlight = new BABYLON.PointLight("sunlight", new BABYLON.Vector3(0, 0, 0));
    const surface = new BABYLON.StandardMaterial("surface");
    surface.diffuseTexture =  new BABYLON.Texture(sphere_textures[n.class]);
    
    // light coming of sun
    surface.emissiveColor = new BABYLON.Color3(0, 1, 1);
    sunlight.diffuse = new BABYLON.Color3(0, 1, 1);
    sunlight.specular = new BABYLON.Color3(0, 1, 1);

    star.material = surface

    return star
}

function createPlanet(n){
    const planet = BABYLON.MeshBuilder.CreateSphere(n.name,  {diameter: scale_radius(n.radius)});
    planet.position = new BABYLON.Vector3(scale_distance(Math.random()),0,scale_distance(n.orbitsDistance));

    // texture
    const surface = new BABYLON.StandardMaterial("surface");
    surface.diffuseTexture =  new BABYLON.Texture(sphere_textures[n.class]);
    planet.material = surface
    planet.material.specularColor = new BABYLON.Color3(shinyness, shinyness, shinyness);

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


