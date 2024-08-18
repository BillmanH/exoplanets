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
camera_pan_speed = 100

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
    star.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickTrigger, function(ev){
        objectDetails(star.metadata.data)
        pickedMesh = get_clicked_mesh(star)
        console.log(pickedMesh)
        animateCameraTargetToObject(camera, camera_pan_speed, 200, star.getAbsolutePosition())
    }));
    
    return star
}


// Planet
function createPlanet(n){
    var orbiting = scene.getMeshByName(n.data.orbitsId);
    n.diameter = scale_radius(n.data.radius)  // should be r*2 but I want smaller planets. 
    n.x = scale_distance(n.iter)
    
    n.y = 0
    n.z = scale_distance(n.data.orbitsDistance)
    n.data.rendered_radius = n.diameter
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

    planet.actionManager = new BABYLON.ActionManager(scene);
    planet.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function(ev){
        hoverTooltip(planet)
    }));
    planet.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function(ev){
        dropControlIfExists("uiTooltip")
    }));
    planet.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickTrigger, function(ev){
        objectDetails(planet.metadata.data)
        pickedMesh = get_clicked_mesh(planet)
        console.log(pickedMesh)
        animateCameraTargetToObject(camera, camera_pan_speed, 200, planet.getAbsolutePosition())
    }));

    return planet
}

// Moon
function createMoon(n){
    var orbiting = scene.getMeshByName(n.data.orbitsId);

    n.diameter = scale_radius(n.data.radius)  // should be r*2 but I want smaller moons.  
    // n.diameter = 1
    const moon = BABYLON.MeshBuilder.CreateSphere(n.data.objid,  {diameter: n.diameter});
    moon.parent = orbiting
    moon.position = new BABYLON.Vector3(orbiting.position);
    orbiting_translation(moon, orbiting.metadata.data.rendered_radius)
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
    moon.actionManager.registerAction(new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickTrigger, function(ev){
        objectDetails(moon.metadata.data)
        pickedMesh = get_clicked_mesh(moon)
        console.log(pickedMesh)
        animateCameraTargetToObject(camera, camera_pan_speed, 200, moon.getAbsolutePosition())
    }));
}

function orbiting_translation(obj,dist){
    const translateX = BABYLON.Scalar.RandomRange((30 + dist)*-1, 30 + dist);
    const translateY = BABYLON.Scalar.RandomRange((30 + dist)*-1, 30 + dist);
    const translateZ = BABYLON.Scalar.RandomRange((30 + dist)*-1, 30 + dist);

    const translationMatrix = BABYLON.Matrix.Translation(translateX, translateY, translateZ);
    translationMatrix.decomposeToTransformNode(obj);
}


// Main -- rendering loops
// Primary objects that don't rely on the relative position
function createprimry_bodies(pdata){
    var guiIter = 0
    for (let i = 0; i < data.nodes.length; i++) {
        n = {}
        n.data = data["nodes"][i]
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
                    o.data = get_node(data["nodes"],satellites[si].id)
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
}

function createMoons(pdata){
    // Secondary objects that do rely on a position of something else.
    var guiIter = 0
    for (let i = 0; i < pdata.length; i++) {
        n = {}
        n.data = pdata[i]
        guiIter++
        n.iter = guiIter
        if (n.data.objtype=="moon"){
            createMoon(n)
        }
    }
}

createprimry_bodies(filter_nodes_list(data["nodes"],'objtype','planet'))
createMoons(filter_nodes_list(data["nodes"],'objtype','moon'))