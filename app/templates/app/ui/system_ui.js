{% load static %}

icons = {
    planets:"{% static 'app/objects/icons/planet_icon_1.png' %}",
    galaxy:"{% static 'app/objects/icons/galaxy_icon.png' %}",    
    exit:"{% static 'app/objects/icons/exit_icon.png' %}"
}

planet_control_panel = {
    name:"planets_window",
    title: "The known planets in this system",
    top:20,
    left:70,
    width:"400px",
    height:"100px"
}


var planets_icon = create_icon({name:'planets_icon',image:icons.planets,top:getIconTop(0)})
dashboard.addControl(planets_icon);

var galaxy_icon = create_icon({name:'galaxy_icon',image:icons.galaxy,top:getIconTop(1)})
dashboard.addControl(galaxy_icon);

var exit_icon = create_icon({name:'exit_icon',image:icons.exit,top:getIconTop(2)})
dashboard.addControl(exit_icon);



planets_icon.onPointerClickObservable.add(function () {
    dropAllControls()
    var planet_ids = get_values(data.nodes, 'objid', 'planet')
    planet_control_panel.height = (100 * planet_ids.length).toString() + "px"
    planet_control = createControlBox(planet_control_panel)
    for (let i = 0; i < planet_ids.length; i++){
        p = {}
        p.data = get_node(data.nodes,planet_ids[i])
        p.iter = i+1
        p.gui = {buttonColor:"white"}
        p.gui.clickButton = function(p) {
            console.log(p.data.name, p.data.objid, " button was pushed")
            planet = scene.getMeshByName(p.data.objid);
            console.log(planet)
            camera.setTarget(new BABYLON.Vector3(planet.metadata.x, planet.metadata.y, planet.metadata.z));
            camera.radius = planet.metadata.diameter + 25  
            objectDetails(p.data)
            dropAllControls()
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

exit_icon.onPointerClickObservable.add(function () {
    dropAllControls()
    plz = pleaseWaiter(dashboard)
    dest = '/'
    console.log('quit to menu')
    window.location.href = dest;
});

galaxy_icon.onPointerClickObservable.add(function () {
    dropAllControls()
    plz = pleaseWaiter(dashboard)
    dest = '/galaxymap'
    console.log('off to galaxy')
    window.location.href = dest;
});


object_to_console = function(o){
    console.log(o)
}
