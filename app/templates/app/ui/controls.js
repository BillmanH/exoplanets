// https://doc.babylonjs.com/features/featuresDeepDive/gui/gui

generic_control_panel = {top:50,
                left:300,
                width:"400px",
                height:"600px",
                alpha:0.5,
                cornerRadius:5,
                thickness:1,
                linkOffsetY:30,
                close_offset_left:75}


// for buttons creatd dynamically, for example the children of an item
var createButton = function(n) {
    var button = BABYLON.GUI.Button.CreateSimpleButton("btn_" + n.data.objid, n.data.name);
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

// for buttons created with a specific use case, like get actions. 
var createSpecificButton = function(n,window){
    // TODO
    var button = BABYLON.GUI.Button.CreateSimpleButton("btn_visit_" + n.data.objid, n.gui.buttontext);
    button.width = "100px"
    button.height = "40px"
    button.top = 50 * n.iter
    button.left = 200  + n.gui.depth
    
    button.color = n.gui.buttonColor;
    button.cornerRadius = 10;
    button.background = "black";
    button.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
    button.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;

    window.addControl(button);
    return button
}

// button that visits a local pop. 
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
            pleaseWaiter(dashboard)
            console.log(n.name, n.objid, " visit button was pushed")
            window.location.href = '/popuilocal' + '?objid=' + n.data.objid;
        });
}

function createRectangle(control_panel){
        const label = new BABYLON.GUI.Rectangle("Window")
            label.background = 'black'
            label.top = control_panel.top 
            label.left = control_panel.left 
            
            label.width = control_panel.width
            label.height = control_panel.height
            label.alpha = control_panel.alpha

            label.cornerRadius = control_panel.cornerRadius
            label.thickness = control_panel.thickness
            label.linkOffsetY = control_panel.linkOffsetY

        label.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        label.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
        dashboard.addControl(label);

        var closeButton = BABYLON.GUI.Button.CreateSimpleButton("btn_close", "X");
            closeButton.background = 'black'
            closeButton.top = control_panel.top - 45
            closeButton.left = control_panel.left + control_panel.close_offset_left
            closeButton.width = "20px"
            closeButton.height = "20px"
            closeButton.color = "white"
            closeButton.cornerRadius = control_panel.cornerRadius
            closeButton.thickness = control_panel.thickness
            closeButton.linkOffsetY = control_panel.linkOffsetY

            closeButton.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
            closeButton.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;

        label.addControl(closeButton);

        closeButton.onPointerUpObservable.add(function() {
            dashboard.getControlByName("Window").dispose()
        });

        return label
}


var objectDetails = function(d){
    textblock.text = dictToSimpleText(d);
}

ButtonBox = createRectangle(generic_control_panel)
ButtonBox.isVisible = false
dashboard.getControlByName("btn_close").isVisible = false


// TODO: Things I want to implement later: 
// https://doc.babylonjs.com/features/featuresDeepDive/animation/animation_design