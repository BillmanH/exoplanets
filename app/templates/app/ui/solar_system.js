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
    n.diameter = star_base
    n.x = 0
    n.y = 0
    n.z = 0
    const star = BABYLON.MeshBuilder.CreateSphere(n.objid, {diameter: n.diameter});
    var sunlight = new BABYLON.PointLight("sunlight", new BABYLON.Vector3(n.x, n.y, n.z));
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
    n.diameter = scale_radius(n.radius)/2  // should be r*2 but I want smaller plantets. 
    n.x = scale_distance(guiIter)
    n.y = 0
    n.z = scale_distance(n.orbitsDistance)
    const planet = BABYLON.MeshBuilder.CreateSphere(n.name,  {diameter: n.diameter});
    planet.position = new BABYLON.Vector3(n.x, n.y, n.z);

    // texture
    const surface = new BABYLON.StandardMaterial("surface");
    surface.diffuseTexture =  new BABYLON.Texture(sphere_textures[n.class]);
    planet.material = surface
    planet.material.specularColor = new BABYLON.Color3(shinyness, shinyness, shinyness);


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

    var label = new BABYLON.GUI.TextBlock(n.name+"nameplate");
        // https://playground.babylonjs.com/#XCPP9Y#121
        label.text = n.name;
        label.height = "40px"
        rect1.addControl(label);   
}
// scene.getMeshByName("bloom").isVisible = false;

var guiIter = 0
for (let i = 0; i < solar_system.nodes.length; i++) {
    n = solar_system["nodes"][i]
    if (n["objtype"]=="star"){
        guiIter++
        n.iter = guiIter
        createStar(n)
        createButton(n, guiIter)
    }
    if (n["objtype"]=="planet"){
        guiIter++
        n.iter = guiIter
        createPlanet(n)
        createButton(n, guiIter)
        // console.log(n.name, i)
    }
  }


