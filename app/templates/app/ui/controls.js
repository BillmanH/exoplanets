// https://doc.babylonjs.com/features/featuresDeepDive/gui/gui


var createButton = function(n,i) {
    // n = name of the planet
    // i = iteration #
    // console.log(n.name, i)
    var button = BABYLON.GUI.Button.CreateSimpleButton("btn" + toString(i), n.name);
    button.width = "150px"
    button.height = "40px"
    button.top = 50 * i
    button.left = 50
    
    button.color = "white";
    button.cornerRadius = 10;
    button.background = "black";
    button.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
    dashboard.addControl(button);

    button.onPointerUpObservable.add(function() {
        console.log(n.name, n.objid, " button was pushed")
        camera.setTarget(new BABYLON.Vector3(n.x, n.y, n.z));
        camera.radius = n.diameter + 25  
        label = dashboard.getControlByName(n.objid+"nameplate")
        if(label){label.isVisible = false}
    });

}

