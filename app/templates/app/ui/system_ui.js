{% load static %}

icons = {
    "planets":"{% static 'app/objects/icons/planet_icon_1.png' %}"
}

planet_control_panel = {
    name:"planets_window",
    title: "The known planets in this system",
    top:20,
    left:70,
    width:"400px",
    height:"100px"
}

var planets_icon = BABYLON.GUI.Button.CreateImageOnlyButton("pop_icon", icons["planets"]);
    planets_icon.width = "40px";
    planets_icon.height = "40px";
    planets_icon.top = 20
    planets_icon.left = 20
    planets_icon.color = "white";
    planets_icon.stretch = BABYLON.GUI.Image.STRETCH_EXTEND;
    planets_icon.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
    planets_icon.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
    dashboard.addControl(planets_icon);

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
            if(p.data.isSupportsLife=="True"){
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
