{% load static %}

icons = {
    planets:"{% static 'app/objects/icons/planet_icon_1.png' %}",
    resources:"{% static 'app/objects/icons/resource_icon_1.png' %}"
}

planet_control_panel = {
    name:"planets_window",
    title: "The known planets in this system",
    top:20,
    left:70,
    width:"400px",
    height:"100px"
}

resources_control_panel = {
    name:"resources_window",
    title: "These are the resources known to be avalable in this system",
    top:20,
    left:70,
    width:"400px",
    height:"100px"
}

var planets_icon = create_icon({name:'planets_icon',image:icons.planets,top:20})
dashboard.addControl(planets_icon);

// var resource_icon = create_icon({name:'resource_icon',image:icons.resources,top:90})
// dashboard.addControl(resource_icon);


planets_icon.onPointerClickObservable.add(function () {
    dropAllControls()
    data = get_values(solar_system.nodes, 'objid', 'planet')
    // console.log(data)
    planet_control_panel.height = (100 * data.length).toString() + "px"
    planet_control = createControlBox(planet_control_panel)
    for (let i = 0; i < data.length; i++){
        // console.log(get_node(solar_system.nodes,data[i]).name)
        p = {}
        p.data = get_node(solar_system.nodes,data[i])
        p.iter = i+1
        p.gui = {buttonColor:"white"}
        p.gui.clickButton = function(p) {
            console.log(p.data.name, p.data.objid, " button was pushed")
            // getPopBox(p)
            planet = scene.getMeshByName(p.data.objid);
            console.log(planet)
            camera.setTarget(new BABYLON.Vector3(planet.metadata.x, planet.metadata.y, planet.metadata.z));
            camera.radius = planet.metadata.diameter + 25  
            objectDetails(p.data)
        }
        addButtonToBox(p,planet_control)
        if(p.data.isSupportsLife.toLowerCase()=="true"){
            p.gui.buttonColor = "green"
            p.gui.buttontext = "visit"
            p.gui.buttonName = "visit_"
            p.gui.width = "60px"
            p.gui.visitButton = function(p) {
                pleaseWaiter(dashboard)
                console.log(p.data.name, p.data.objid, " visit button was pushed")
                window.location.href = '/popuilocal' + '?objid=' + p.data.objid;
            };
            addButtonToBox(p,planet_control)
        };
    }
});

// resource_icon.onPointerClickObservable.add(function () {
//     dropAllControls()
//     resource_control = createControlBox(resources_control_panel)
// });