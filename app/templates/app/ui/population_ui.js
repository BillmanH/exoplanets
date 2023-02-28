{% load static %}
{% include "app/ajax/population_info.js" %}
{% include "app/ajax/resources.js" %}

icons = {
    pop:"{% static 'app/objects/icons/pop_icon_2.png' %}",
    resources:"{% static 'app/objects/icons/resource_icon_1.png' %}",
    system:"{% static 'app/objects/icons/system_icon_1.png' %}"
}

pop_control_panel = {
    name:"faction_window",
    title: "These are the factions at this location",
    top:20,
    left:70,
    width:"400px",
    height:"100px"
}

faction_control_panel = {
    title: "These are the populations within the faction",
    top:20,
    left:500,
    width:"400px",
    height:"100px"
}

actions_control_panel = {
    title: "These are the actions available at this time",
    name:"action_window", 
    top:20,
    left:920,
    width:"600px",
    height:"600px"
}

resources_control_panel = {
    name:"resources_window",
    title: "These are the resources known to be avalable in this system",
    top:20,
    left:70,
    width:"600px",
    height:"100px"
}

var system_icon = create_icon({name:'system_icon',image:icons.system,top:20,tooltiptext:"return to the system"})
var pop_icon = create_icon({name:'pop_icon',tooltiptext:"factions and populations",image:icons.pop,top:90})
var resource_icon = create_icon({name:'resource_icon',tooltiptext:"resources at this location",image:icons.resources,top:160})




// pointer 
const pointer = BABYLON.MeshBuilder.CreateSphere("pointer", {diameter: 12});
    pointer.position = new BABYLON.Vector3(0,0,0)
    pointer.isVisible = false

function getPopBox(f){
    dropControlIfExists("window")
    dropControlIfExists("action_window")
    pops = filter_nodes_res(data.nodes,'faction','name', f.data.name)
    faction_control_panel.height = (100 * pops.length).toString() + "px"
    faction_pops_control = createControlBox(faction_control_panel)
    for (let si = 0; si < pops.length; si++) {
        p = {}
        p.data = pops[si].population
        p.iter = si+1
        p.gui = {buttonColor:"white"}
        p.gui.clickButton = function(p) {
            console.log(p.data.name, p.data.objid, " button was pushed")
            objectDetails(p.data)
        };
        pop_button = addButtonToBox(p,faction_pops_control)
        // console.log(p.data.isIdle)
        if(p.data.isIdle.toLowerCase()=="true"){
            p.gui.buttonColor = "green"
            p.gui.buttontext = "get actions"
            p.gui.buttonName = "get_actions_"
            p.gui.width = "60px"
            p.gui.actionButton = function(p) {
                console.log(p.data.name, p.data.objid, " button was pushed")
                objectDetails(p.data)
                p.data = pops[si].population
                prep_actions(p)
            };
            addButtonToBox(p,faction_pops_control)
            }
    }
}



pop_icon.onPointerClickObservable.add(function () {
    dropAllControls()

    factions = distinct_list(data.nodes,'faction','objid')
    pop_control_panel.height = (100 * factions.length).toString() + "px"
    pop_control = createControlBox(pop_control_panel)
    var guiIter = 0
    for (let i = 0; i < factions.length; i++){
        guiIter ++
        f = {}
        f.data = get_specific_node(data.nodes,factions[i])[0]
        f.iter = guiIter
        f.gui = {buttonColor:"white",
        depth:0}
        f.coord = {
            x:f.data.lat*ground_dimensions,
            y:0,
            z:f.data.lat*ground_dimensions
        }
        f.gui.clickButton = function(f) {
            console.log(f.data.name, f.data.objid, " button was pushed")
            pointer.position = new BABYLON.Vector3(f.coord.x, 100, f.coord.z) 
            pointer.isVisible = true
            getPopBox(f)
            objectDetails(f.data)
        };
        addButtonToBox(f,pop_control)
    }
});

resource_icon.onPointerClickObservable.add(function () {
    dropAllControls()
    ajax_get_local_resources({location:global_location}).then(function(response){
        const resources = response.resources
        resources_control_panel.height = (100 * resources.length).toString() + "px"
        resource_control = createControlBox(resources_control_panel)
        for (let i = 0; i < resources.length; i++){
            n = {}
            n.iter = i+1
            n.displayed_values = ["name","description","volume"]
            n.data = resources[i]
            addTextBlockToBox(n,resource_control)
        }
    })
});

function make_actions_box(actions){
    dropControlIfExists("action_window")
    if(actions.hasOwnProperty('actions')){
        actions_control_panel.height = (100 * actions.actions.length).toString() + "px"
        
        actions_control_panel.title = actions.pop.objtype + ": " + actions.pop.name + ". Has these actions"
        actions_control = createControlBox(actions_control_panel)
        for (let i = 0; i < actions.actions.length; i++) {
            a = {}
            a.gui = {
                buttonColor:"white",
                depth:1,
                returnButton:true,
                width:"200px"}
                a.iter = i+1
                a.data = actions.actions[i]
                a.gui.clickButton = function(a) {
                    console.log(actions.pop.name,": ", a.type, " button was pushed")
                    console.log("action", a)
                    takeAction(actions.pop,a.data)
                };
                // textblock.text += cs(a.data.type) + ": " + a.data.comment + "\n" + "\n"
                addButtonToBox(a,actions_control)
            }
            
    } else {
        actions_control_panel.title = "This population has no actions available to it as this time"
        ActionBox = createControlBox(actions_control_panel)
    }
}


system_icon.onPointerClickObservable.add(function () {
    dropAllControls()
    plz = pleaseWaiter(dashboard)
    dest = '/systemui?objid=' + global_location + '&orientation=planet'
    console.log(dest)
    window.location.href = dest;
});