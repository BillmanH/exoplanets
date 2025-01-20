{% load static %}
{% include "app/ajax/population_info.js" %}
{% include "app/ajax/resources.js" %}
{% include "app/ajax/events.js" %}

icons = {
    faction:"{% static 'app/objects/icons/pop_icon_2.png' %}",
    resources:"{% static 'app/objects/icons/resource_icon_1.png' %}",
    system:"{% static 'app/objects/icons/system_icon_1.png' %}",
    events:"{% static 'app/objects/icons/events_icon_1.png' %}",
    exit:"{% static 'app/objects/icons/exit_icon.png' %}"
}

pop_control_panel = {
    name:"faction_window",
    title: "These are the factions at this location",
    top:20,
    left:80,
    width:"400px",
    height:"100px"
}

faction_control_panel = {
    title: "These are the populations within the faction",
    top:20,
    left:80,
    width:"400px",
    height:"100px"
}

actions_control_panel = {
    title: "These are the actions available at this time",
    name:"action_window", 
    top:20,
    left:20,
    width:"600px",
    height:"600px"
}

resources_control_panel = {
    name:"resources_window",
    title: "These are the resources known to be avalable in this system",
    top:20,
    left:80,
    width:"600px",
    height:"100px"
}

events_control_panel = {
    name:"events_window",
    title: "Events:",
    top:20,
    left:80,
    width:"600px",
    height:"100px"
}

var system_icon = create_icon({name:'system_icon',image:icons.system,top:getIconTop(0),tooltiptext:"return to the system"})
if (data.nodes.length > 0){
    var faction_icon = create_icon({name:'pop_faction_iconicon',tooltiptext:"factions and populations",image:icons.faction,top:getIconTop(1)})
    faction_icon.onPointerClickObservable.add(function () {
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
                piovtCamera(f.data.objid+"_nocol_faction_merged")
                // getPopBox(f)
                objectDetails(f.data)
                dropAllControls()
            };
            addButtonToBox(f,pop_control)
        }
    });
}
if (data.resources.length > 0) {
    var resource_icon = create_icon({name:'resource_icon',tooltiptext:"resources at this location",image:icons.resources,top:getIconTop(2)})
    resource_icon.onPointerClickObservable.add(function () {
        dropAllControls()
        ajax_get_local_resources({location:data.location.objid}).then(function(response){
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
        dropControlIfExists("loadingpleasewait")
    });
}

if (data.location.hascontrol == "True"){
    var events_icon = create_icon({name:'events_icon',tooltiptext:"Events",image:icons.events,top:getIconTop(3)})
}
var exit_icon = create_icon({name:'quit_icon',tooltiptext:"Quit",image:icons.exit,top:getIconTop(4)})

var piovtCamera = function(name){
    var o = scene.getMeshByName(name);
    camera.setTarget(o.position);
    camera.radius = 100 
}


function popOptionsWindow(pop){
    dropAllControls()
    faction_control_panel.height = (100 * pop.factions.length).toString() + "px"
    faction_control = createControlBox(faction_control_panel)

}

system_icon.onPointerClickObservable.add(function () {
    dropAllControls()
    plz = pleaseWaiter(dashboard)
    dest = '/systemui?objid=' + data.location.objid + '&orientation=planet'
    console.log(dest)
    window.location.href = dest;
});






exit_icon.onPointerClickObservable.add(function () {
    dropAllControls()
    plz = pleaseWaiter(dashboard)
    dest = '/'
    console.log('quit to menu')
    window.location.href = dest;
});

function make_faction_ui(faction){
    faction_control = createControlBox(faction_control_panel)
    console.log("Faction window opened")
}