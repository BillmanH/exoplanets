// https://doc.babylonjs.com/features/featuresDeepDive/gui/gui


var createButton = function(n) {
    var button = BABYLON.GUI.Button.CreateSimpleButton("btn_" + n.objid, n.name);
        button.width = "150px"
        button.height = "40px"
        button.top = 50 * n.iter
        button.left = 50
        
        button.color = n.gui.buttonColor;
        button.cornerRadius = 10;
        button.background = "black";
        button.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        button.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;

        BABYLON.Tags.AddTagsTo(button, "button_"+n.gui.depth);

        if (n.gui.depth < 1){
            dashboard.addControl(button);
        }
        else {
            ButtonBox.addControl(button)
        }
        button.onPointerUpObservable.add(function() {n.gui.clickButton(n)});

}

var createVisitButton = function(n){
    var button = BABYLON.GUI.Button.CreateSimpleButton("btn_visit_" + n.objid, "visit");
        button.width = "50px"
        button.height = "40px"
        button.top = 50 * n.iter
        button.left = 200  + (150 * n.gui.depth)
        
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

var createRectangle = function(){
        const label = new BABYLON.GUI.Rectangle("Window")
        label.background = 'black'
        label.top = 50 
        label.left = 300 
        
        label.width = "400px"
        label.height = "600px"
        label.alpha = 0.5;

        label.cornerRadius = 5;
        label.thickness = 1;
        label.linkOffsetY = 30;


        label.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        label.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
        dashboard.addControl(label);
        return label
}

var objectDetails = function(d){
    textblock.text = dictToSimpleText(d);
}
// TODO: Things I want to implement later: 
// https://doc.babylonjs.com/features/featuresDeepDive/animation/animation_design