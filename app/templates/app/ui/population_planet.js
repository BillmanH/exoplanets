{% load static %}
{% include "app/ajax/popinfo.js" %}

factionbuildingHeight = 10


faction_control_panel = {top:50,
    left:300,
    width:"400px",
    height:"600px",
    alpha:0.5,
    cornerRadius:5,
    thickness:1,
    linkOffsetY:30,
    close_offset_left:465}

actions_control_panel = {
    name:"action_window", 
    top:50,
    left:720,
    width:"600px",
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
    const box = BABYLON.MeshBuilder.CreateBox(n.data.objid+"_box", 
        {"height":factionbuildingHeight,
        "size":5}
      );
      box.parent = center
      box.position = new BABYLON.Vector3(n.coord.x, factionbuildingHeight/2, n.coord.z) 
      const boxMat = new BABYLON.StandardMaterial(n.data.objid + "_groundMat");
      boxMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/skyscraper.png' %}");
      box.material = boxMat; 
      
    var disc = BABYLON.MeshBuilder.CreateCylinder(n.data.objid + "disc", {diameter:50, height:1});
        disc.position.y = factionbuildingHeight/2*-1
        disc.parent = box
    const discMat = new BABYLON.StandardMaterial(n.data.objid + "_groundMat");
        discMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/city_disc.png' %}");
        disc.material = discMat; 
}

function createPop(n){
    var faction = scene.getMeshByName(n.data.faction.objid+"_box");
    const box = BABYLON.MeshBuilder.CreateBox(n.data.population.objid+"_box", 
        {"height":factionbuildingHeight/2,
        "size":5}
    );
    box.parent = faction
    box.position = new BABYLON.Vector3(n.coord.x + 5, factionbuildingHeight/4*-1, n.coord.z + 5) 
    var phi = Math.random() * 2 * Math.PI; 
    box.rotation.y = phi;

    const boxMat = new BABYLON.StandardMaterial(n.data.population.objid + "_groundMat");
        boxMat.diffuseTexture =  new BABYLON.Texture("{% static 'app/objects/planet/surface/skyscraper_2.png' %}");
        box.material = boxMat; 
}

function GetActionClickbuttion(p){
        console.log(p)
        console.log(p.data.name, p.data.objid, " button was pushed")
        prep_actions(p)
}

function getPopBox(f){
    aw = dashboard.getControlByName("action_window")
    w = dashboard.getControlByName("window")
    if(aw!=undefined){aw.dispose()}
    if(w!=undefined){w.dispose()}
    ButtonBox.dispose()
    ButtonBox = createRectangle(faction_control_panel)
    pops = filter_nodes_res(data.nodes,'faction','name', f.data.name)
    for (let si = 0; si < pops.length; si++) {
        p = {}
        p.data = pops[si].population
        p.iter = si+1
        p.gui = {buttonColor:"white",
            depth:1}
        p.gui.clickButton = function(p) {
            console.log(p.data.name, p.data.objid, " button was pushed")
            objectDetails(p.data)
        };
        createButton(p)
        
        if(p.data.isIdle=="True"){
            p.gui.buttonColor = "green"
            p.gui.buttontext = "get actions"
            p.gui.buttonName = "get_actions_"
            p.gui.returnButton = true
            console.log("p",p)
            actionsButton = createSpecificButton(p)
            // console.log('button',p.data.name,actionsButton)
            ButtonBox.addControl(actionsButton)
            actionsButton.onPointerUpObservable.add(function(p) {
                p.data = pops[si].population
                prep_actions(p)
            });
            }
    }
    ButtonBox.isVisible = true
}

function make_actions_screen(actions){
    aw = dashboard.getControlByName("action_window")
    if(aw!=undefined){aw.dispose()}
    ButtonBox = createRectangle(actions_control_panel)

    var textblock = new BABYLON.GUI.TextBlock("actions_textblock")
        textblock.textHorizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
        textblock.textVerticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP
        textblock.textWrapping = true;
        ButtonBox.addControl(textblock);

        textblock.paddingTop = 10 
        textblock.paddingLeft = 260 
        textblock.fontSize = 18;    
        textblock.background = "black";
        textblock.color = "white";    
        textblock.text = actions.pop.objtype + ": " + actions.pop.name + "\n" + "\n"

    for (let i = 0; i < actions.actions.length; i++) {
        a = {}
        a.gui = {
            buttonColor:"white",
            depth:1,
            returnButton:true,
            width:"200px"}
        a.iter = i+1
        a.data = actions.actions[i]
        button = createButton(a)
        ButtonBox.addControl(button)
        textblock.text += cs(a.data.type) + ": " + a.data.comment + "\n" + "\n"
    }
}

// main - actually loads the content
var guiIter = 0
factions = distinct_list(data.nodes,'faction','objid')

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
        objectDetails(f.data)
    };
    createButton(f)
    for (let j = 0; j < pops.length; j++) {
        p = {}
        p.data = pops[j]
        p.coord = pivotLocal(-15,15)
        createPop(p)
    }
  }



// Goals: 
// https://doc.babylonjs.com/features/featuresDeepDive/mesh/creation/set/height_map