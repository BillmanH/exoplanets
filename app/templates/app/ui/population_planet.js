{% load static %}
{% include "app/ajax/popinfo.js" %}

factionbuildingHeight = 10

faction_control_panel = {top:50,
    left:300,
    width:"800px",
    height:"600px",
    alpha:0.5,
    cornerRadius:5,
    thickness:1,
    linkOffsetY:30,
    close_offset_left:465}


// light
const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(1, 1, 0));

// ground
const ground = BABYLON.MeshBuilder.CreateGround("ground", {width:500, height:500});
const groundMat = new BABYLON.StandardMaterial("groundMat");
    groundMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/surface_green.png' %}");
    ground.material = groundMat; //Place the material property of the ground

// center
const center = BABYLON.MeshBuilder.CreateBox("center", {"height":20,"size":1})
    center.isVisible = false

ButtonBox = createRectangle(faction_control_panel)
ButtonBox.isVisible = false

// pointer 
const pointer = BABYLON.MeshBuilder.CreateSphere("pointer", {diameter: 12});
pointer.position = new BABYLON.Vector3(0,0,0)
pointer.isVisible = false

function createFaction(n){
    const box = BABYLON.MeshBuilder.CreateBox(n.objid+"_box", 
        {"height":factionbuildingHeight,
        "size":5}
      );
      box.parent = center
      box.position = new BABYLON.Vector3(n.coord.x, factionbuildingHeight/2, n.coord.z) 
      const boxMat = new BABYLON.StandardMaterial(n.objid + "_groundMat");
      boxMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/skyscraper.png' %}");
      box.material = boxMat; 
      
    var disc = BABYLON.MeshBuilder.CreateCylinder(n.objid + "disc", {diameter:50, height:1});
        disc.position.y = factionbuildingHeight/2*-1
        disc.parent = box
    const discMat = new BABYLON.StandardMaterial(n.objid + "_groundMat");
        discMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/city_disc.png' %}");
        disc.material = discMat; 
}

function createPop(n,f){
    var faction = scene.getMeshByName(f.objid+"_box");
    const box = BABYLON.MeshBuilder.CreateBox(n.objid+"_box", 
        {"height":factionbuildingHeight/2,
        "size":5}
    );
    box.parent = faction
    box.position = new BABYLON.Vector3(n.coord.x + 5, factionbuildingHeight/4*-1, n.coord.z + 5) 
    var phi = Math.random() * 2 * Math.PI; 
    box.rotation.y = phi;

    const boxMat = new BABYLON.StandardMaterial(n.objid + "_groundMat");
        boxMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/skyscraper_2.png' %}");
        box.material = boxMat; 
}

function getPopBox(f){
    ButtonBox.dispose()
    ButtonBox = createRectangle(faction_control_panel)
    pops = filter_nodes_res(data.nodes,'faction','name', f.data.name)
    console.log(pops)
    var guiIter = 0
    for (let si = 0; si < pops.length; si++) {
        guiIter++
        o = {}
        o.data = pops[si].population
        console.log(si,"pop", o)
        o.iter = guiIter
        o.gui = {buttonColor:"white",
            depth:1}
        o.gui.clickButton = function(o) {
            console.log(o.data.name, o.data.objid, " button was pushed")
            objectDetails(o.data)
        };
        createButton(o)
        if(o.data.isIdle=="True"){
            o.gui.buttonColor = "green"
            o.gui.buttontext = "get actions"
            actionsButton = createSpecificButton(o, ButtonBox)}
            actionsButton.onPointerUpObservable.clear()
            actionsButton.onPointerUpObservable.add(function() {ajax_getActions(o.data)});
        }
    ButtonBox.isVisible = true
}


// main - actually loads the content
var guiIter = 0
factions = distinct_list(data.nodes,'faction','objid')
console.log(factions)
for (let i = 0; i < factions.length; i++) {
    guiIter ++
    f = {}
    f.data = get_specific_node(data.nodes,factions[i])[0]   
    f.iter = guiIter
    pops = filter_nodes_res(data.nodes,'faction','name', f.data.name)
    f.coord = pivotLocal(-150,150)
    createFaction(f)
    f.gui = {buttonColor:"white",
            depth:0}
    f.gui.clickButton = function(f) {
        console.log(f.data.name, f.data.objid, " button was pushed")
        pointer.position = new BABYLON.Vector3(f.coord.x, 100, f.coord.z) 
        pointer.isVisible = true
        getPopBox(f)
        objectDetails(f)
    };
    createButton(f)
    for (let j = 0; j < pops.length; j++) {
        p = pops[j]
        p.coord = pivotLocal(-15,15)
        createPop(p,f)
    }

  }



// Goals: 
// https://doc.babylonjs.com/features/featuresDeepDive/mesh/creation/set/height_map