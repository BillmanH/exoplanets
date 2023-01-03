// https://doc.babylonjs.com/features/featuresDeepDive/gui/gui


var createButton = function(n) {
    var button = BABYLON.GUI.Button.CreateSimpleButton("btn" + toString(n.iter), n.name);
        button.width = "150px"
        button.height = "40px"
        button.top = 50 * n.iter
        button.left = 50
        
        button.color = "white";
        button.cornerRadius = 10;
        button.background = "black";
        button.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        button.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
        
        dashboard.addControl(button);
        button.onPointerUpObservable.add(function() {
            console.log(n.name, n.objid, " button was pushed")
            camera.setTarget(new BABYLON.Vector3(n.x, n.y, n.z));
            camera.radius = n.diameter + 25  
            label = dashboard.getControlByName(n.objid+"_nameplate")
            if(label){label.isVisible = false}
            objectDetails(n)
    });

}


var objectDetails = function(d){
    textblock.text = dictToSimpleText(d);
}
// TODO: Things I want to implement later: 
// https://doc.babylonjs.com/features/featuresDeepDive/animation/animation_design