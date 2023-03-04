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


// Star
function createStar(n){
    n.diameter = star_base
    n.x = 0
    n.y = 0
    n.z = 0
    const star = BABYLON.MeshBuilder.CreateSphere(n.data.objid, {diameter: n.diameter});
    var sunlight = new BABYLON.PointLight("sunlight", new BABYLON.Vector3(n.x, n.y, n.z));
    const surface = new BABYLON.StandardMaterial("surface");
    surface.diffuseTexture =  new BABYLON.Texture(sphere_textures[n.data.class]);
    
    // light coming of sun
    surface.emissiveColor = new BABYLON.Color3(0, 1, 1);
    sunlight.diffuse = new BABYLON.Color3(0, 1, 1);
    sunlight.specular = new BABYLON.Color3(0, 1, 1);
    star.material = surface
    star.metadata = n

    star.actionManager = new BABYLON.ActionManager(scene);
    star.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function(ev){
        hoverTooltip(star)
    }));
    star.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function(ev){
        dropControlIfExists("uiTooltip")
    }));

    return star
}


// Planet
function createPlanet(n){
    var orbiting = scene.getMeshByName(n.data.orbitsId);
    n.diameter = scale_radius(n.data.radius)/2  // should be r*2 but I want smaller plantets. 
    n.x = scale_distance(n.iter)
    n.y = 0
    n.z = scale_distance(n.data.orbitsDistance)
    const planet = BABYLON.MeshBuilder.CreateSphere(n.data.objid,  {diameter: n.diameter});
    planet.parent = orbiting
    planet.position = new BABYLON.Vector3(n.x, n.y, n.z);
    var phi = Math.random() * 2 * Math.PI; 
    planet.rotation.y = phi;
    // texture
    const surface = new BABYLON.StandardMaterial("surface");
    surface.diffuseTexture =  new BABYLON.Texture(sphere_textures[n.data.class]);
    planet.material = surface
    planet.material.specularColor = new BABYLON.Color3(shinyness, shinyness, shinyness);
    planet.metadata = n
    var rect1 = new BABYLON.GUI.Rectangle(n.data.objid+"_nameplate");
        rect1.width = .06;
        rect1.height = .03;
        rect1.cornerRadius = 10;
        rect1.color = "white";
        rect1.thickness = 4;
        rect1.background = "black";
        dashboard.addControl(rect1);
        rect1.linkWithMesh(planet);   
        rect1.linkOffsetY = -15;


    var label = new BABYLON.GUI.TextBlock(n.data.objid+"_nameplatetext");
        // https://playground.babylonjs.com/#XCPP9Y#121
        label.text = n.data.name;
        label.height = "40px"
        rect1.addControl(label);    

    planet.actionManager = new BABYLON.ActionManager(scene);
    planet.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function(ev){
        hoverTooltip(planet)
    }));
    planet.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function(ev){
        dropControlIfExists("uiTooltip")
    }));

    return planet
}

// Moon
function createMoon(n){
    var orbiting = scene.getMeshByName(n.data.orbitsId);

    n.diameter = scale_radius(n.data.radius)/2  // should be r*2 but I want smaller plantets. 
    n.x = (scale_distance_ln(n.data.orbitsDistance) + 20) * flipper()
    n.y = (scale_distance_ln(n.data.orbitsDistance) + 20) * flipper()
    n.z = (scale_distance_ln(n.data.orbitsDistance) + 20) * flipper()

    const moon = BABYLON.MeshBuilder.CreateSphere(n.data.objid,  {diameter: n.diameter});
    moon.parent = orbiting
    moon.position = new BABYLON.Vector3(n.x, n.y, n.z);
    var phi = Math.random() * 2 * Math.PI; 
    moon.rotation.y = phi;
    // texture
    const surface = new BABYLON.StandardMaterial("surface");
        surface.diffuseTexture =  new BABYLON.Texture(sphere_textures[n.data.class]);
        moon.material = surface
        moon.material.specularColor = new BABYLON.Color3(shinyness, shinyness, shinyness);

    moon.metadata = n
    moon.actionManager = new BABYLON.ActionManager(scene);
    moon.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function(ev){
        hoverTooltip(moon)
    }));
    moon.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function(ev){
        dropControlIfExists("uiTooltip")
    }));
}


// Main -- rendering loops
// Primary objects that don't rely on the relative position
var guiIter = 0
for (let i = 0; i < solar_system.nodes.length; i++) {
    n = {}
    n.data = solar_system["nodes"][i]
    n.gui = {buttonColor:"white",
            depth:0}
    if (n.data.objtype=="star"){
        n.gui.clickButton = function(n) {
            console.log(n.data.name, n.data.objid, " button was pushed")
            camera.setTarget(new BABYLON.Vector3(n.x, n.y, n.z));
            camera.radius = n.diameter + 25  
            label = dashboard.getControlByName(n.data.objid+"_nameplate")
            if(label){label.isVisible = false}
            objectDetails(n.data)
        }
        guiIter++
        n.iter = guiIter
        createStar(n)
    }
    if (n.data.objtype=="planet"){
        guiIter++
        n.iter = guiIter
        n.gui.clickButton = function(n) {
            console.log(n.data.name, n.data.objid, " button was pushed")
            camera.setTarget(new BABYLON.Vector3(n.x, n.y, n.z));
            camera.radius = n.diameter + 25  
            label = dashboard.getControlByName(n.data.objid+"_nameplate")
            if(label){label.isVisible = false}
            objectDetails(n.data)

            satellites = scene.getMeshByName(n.data.objid).getChildren()
            // console.log(satellites)
            var guiIter = 0
            for (let si = 0; si < satellites.length; si++) {
                o = {}
                o.data = get_node(solar_system["nodes"],satellites[si].id)
                console.log(o)
                o.iter = si+1
                o.gui = {buttonColor:"white",
                    depth:1}
                o.gui.clickButton = function(o) {
                    console.log(o)
                    console.log(o.data.name, o.data.objid, " button was pushed")
                    objectDetails(o.data)

                };
                if(o.isSupportsLife.toLowerCase()=="true"){
                    o.gui.buttonColor = "green"
                }
                if(o.data.isSupportsLife.toLowerCase()=="true"){createVisitButton(o)}
            }
        }
        createPlanet(n)

    }
  }


// Secondary objects that do rely on a position of something else.
var guiIter = 0
for (let i = 0; i < solar_system.nodes.length; i++) {
    n = {}
    n.data = solar_system["nodes"][i]
    guiIter++
    n.iter = guiIter
    if (n.data.objtype=="moon"){
        createMoon(n)
    }
}

