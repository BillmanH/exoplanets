// https://doc.babylonjs.com/features/featuresDeepDive/gui/gui


var createButton = function(n) {
    var button = BABYLON.GUI.Button.CreateSimpleButton("btn" + toString(n.iter), n.name);
        button.width = "150px"
        button.height = "40px"
        button.top = 50 * n.iter
        button.left = 50
        
        button.color = n.gui.buttonColor;
        button.cornerRadius = 10;
        button.background = "black";
        button.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        button.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
        
        dashboard.addControl(button);
        button.onPointerUpObservable.add(function() {n.gui.clickButton(n)});

}

var createVisitButton = function(n){
    console.log("visit button")
    var button = BABYLON.GUI.Button.CreateSimpleButton("btn_v" + toString(n.iter), "visit");
        button.width = "50px"
        button.height = "40px"
        button.top = 50 * n.iter
        button.left = 200  
        
        button.color = n.gui.buttonColor;
        button.cornerRadius = 10;
        button.background = "black";
        button.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        button.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
        dashboard.addControl(button);

        button.onPointerUpObservable.add(function() {
            console.log(n.name, n.objid, " visit button was pushed")
            window.location.href = '/popuilocal' + '?objid=' + n.objid;
        });
}


var objectDetails = function(d){
    textblock.text = dictToSimpleText(d);
}
// TODO: Things I want to implement later: 
// https://doc.babylonjs.com/features/featuresDeepDive/animation/animation_design