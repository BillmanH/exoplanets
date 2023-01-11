// const planet = BABYLON.SceneLoader.Append("static/app/objects/", "planet.gltf", scene, function (scene) { });
// https://doc.babylonjs.com/typedoc/classes/BABYLON.SceneLoader#Append
{% load static %}

sphere_textures = {
    "G":"{% static 'app/objects/planet/synthetic_star_g.png' %}",
    "terrestrial":"{% static 'app/objects/planet/synthetic_terrestrial.png' %}",
    "dwarf":"{% static 'app/objects/planet/synthetic_dwarf_2.png' %}",
    "gas":"{% static 'app/objects/planet/synthetic_gas_giant.png' %}",
    "ice":"{% static 'app/objects/planet/synthetic_ice.png' %}",
    "rocky":"{% static 'app/objects/planet/synthetic_moon_rocky_2.png' %}"
}

star_base = 100
shinyness = 0.05

// center
const center = BABYLON.MeshBuilder.CreateBox("center", {"height":20,"size":1})
    center.isVisible = false

ButtonBox = createRectangle()
ButtonBox.isVisible = false

// Star
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


// Planet
function createPlanet(n){
    var orbiting = scene.getMeshByName(n.orbitsId);
    n.diameter = scale_radius(n.radius)/2  // should be r*2 but I want smaller plantets. 
    n.x = scale_distance(guiIter)
    n.y = 0
    n.z = scale_distance(n.orbitsDistance)
    const planet = BABYLON.MeshBuilder.CreateSphere(n.objid,  {diameter: n.diameter});
    planet.parent = orbiting
    planet.position = new BABYLON.Vector3(n.x, n.y, n.z);
    var phi = Math.random() * 2 * Math.PI; 
    planet.rotation.y = phi;
    // texture
    const surface = new BABYLON.StandardMaterial("surface");
    surface.diffuseTexture =  new BABYLON.Texture(sphere_textures[n.class]);
    planet.material = surface
    planet.material.specularColor = new BABYLON.Color3(shinyness, shinyness, shinyness);

    var rect1 = new BABYLON.GUI.Rectangle(n.objid+"_nameplate");
        rect1.width = .06;
        rect1.height = .03;
        rect1.cornerRadius = 10;
        rect1.color = "white";
        rect1.thickness = 4;
        rect1.background = "black";
        dashboard.addControl(rect1);
        rect1.linkWithMesh(planet);   
        rect1.linkOffsetY = -15;


    var label = new BABYLON.GUI.TextBlock(n.objid+"_nameplatetext");
        // https://playground.babylonjs.com/#XCPP9Y#121
        label.text = n.name;
        label.height = "40px"
        rect1.addControl(label);   
}

// Moon
function createMoon(n){
    var orbiting = scene.getMeshByName(n.orbitsId);
    var o_n = get_node(solar_system["nodes"], n.orbitsId)
    n.diameter = scale_radius(n.radius)/2  // should be r*2 but I want smaller plantets. 
    n.x = (scale_distance_ln(n.orbitsDistance) + 20) * flipper()
    n.y = (scale_distance_ln(n.orbitsDistance) + 20) * flipper()
    n.z = (scale_distance_ln(n.orbitsDistance) + 20) * flipper()
    if(n.orbitsName=="Earth"){console.log("orbiting", o_n)}
    const moon = BABYLON.MeshBuilder.CreateSphere(n.objid,  {diameter: n.diameter});
    moon.parent = orbiting
    moon.position = new BABYLON.Vector3(n.x, n.y, n.z);
    var phi = Math.random() * 2 * Math.PI; 
    moon.rotation.y = phi;
    // texture
    const surface = new BABYLON.StandardMaterial("surface");
    surface.diffuseTexture =  new BABYLON.Texture(sphere_textures[n.class]);
    moon.material = surface
    moon.material.specularColor = new BABYLON.Color3(shinyness, shinyness, shinyness);
}


// Main -- rendering loops
// Primary objects that don't rely on the relative position
var guiIter = 0
for (let i = 0; i < solar_system.nodes.length; i++) {
    n = solar_system["nodes"][i]
    n.gui = {buttonColor:"white",
            depth:0}
    if (n["objtype"]=="star"){
        n.gui.clickButton = function(n) {
            console.log(n.name, n.objid, " button was pushed")
            camera.setTarget(new BABYLON.Vector3(n.x, n.y, n.z));
            camera.radius = n.diameter + 25  
            label = dashboard.getControlByName(n.objid+"_nameplate")
            if(label){label.isVisible = false}
            objectDetails(n)
        }
        guiIter++
        n.iter = guiIter
        createStar(n)
        createButton(n)
    }
    if (n["objtype"]=="planet"){
        guiIter++
        n.iter = guiIter
        n.gui.clickButton = function(n) {
            console.log(n.name, n.objid, " button was pushed")
            camera.setTarget(new BABYLON.Vector3(n.x, n.y, n.z));
            camera.radius = n.diameter + 25  
            label = dashboard.getControlByName(n.objid+"_nameplate")
            if(label){label.isVisible = false}
            objectDetails(n)
            ButtonBox.dispose()
            ButtonBox = createRectangle()

            satellites = scene.getMeshByName(n.objid).getChildren()
            // console.log(satellites)
            var guiIter = 0
            for (let si = 0; si < satellites.length; si++) {
                guiIter++
                o = get_node(solar_system["nodes"],satellites[si].id)
                o.iter = guiIter
                o.gui = {buttonColor:"white",
                    depth:1}
                o.gui.clickButton = function(o) {
                    console.log(o.name, o.objid, " button was pushed")
                    objectDetails(o)
                };
                if(o.isSupportsLife=="True"){
                    console.log(o.name,o.isPopulated)
                    o.gui.buttonColor = "green"
                }
                createButton(o)
                if(o.isSupportsLife=="True"){createVisitButton(o)}
            }
        }
        createPlanet(n)
        
        if(n.isSupportsLife=="True"){
            console.log(n.name,n.isPopulated)
            n.gui.buttonColor = "green"
        }
        createButton(n)
        if(n.isSupportsLife=="True"){createVisitButton(n)}
    }
  }


// Secondary objects that do rely on a position of something else.
var guiIter = 0
for (let i = 0; i < solar_system.nodes.length; i++) {
    n = solar_system["nodes"][i]
    guiIter++
    n.iter = guiIter
    if (n["objtype"]=="moon"){
        createMoon(n)
    }
}

