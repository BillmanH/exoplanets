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
    if (n.data.hasOwnProperty('name')==false){
        n.data.name = cs(n.data.type)
    }
    var button = BABYLON.GUI.Button.CreateSimpleButton("btn_" + n.data.objid, n.data.name);
        if(n.gui.hasOwnProperty('width')){
            button.width = n.gui.width
        } else {button.width = "150px"}
        button.height = "40px"
        button.top = 50 * n.iter
        button.left = 50
        
        button.color = n.gui.buttonColor;
        button.cornerRadius = 10;
        button.background = "black";
        button.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        button.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;

        
        if (n.gui.returnButton){
            return button
        }
        else {
            if (n.gui.depth < 1){
                dashboard.addControl(button);
            }
            else {
                ButtonBox.addControl(button)
            }
            button.onPointerUpObservable.add(function() {n.gui.clickButton(n)});
        }
}

// for buttons created with a specific use case, like get actions. 
var createSpecificButton = function(n){
    var button = BABYLON.GUI.Button.CreateSimpleButton(n.gui.buttonName + n.data.objid, n.gui.buttontext);
    button.width = "100px"
    button.height = "40px"
    button.top = 50 * n.iter
    button.left = 200  + n.gui.depth
    
    button.color = n.gui.buttonColor;
    button.cornerRadius = 10;
    button.background = "black";
    button.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
    button.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
    // console.log(n.gui.returnButton)
    if (n.gui.returnButton){
        return button
    }
    else {
        if (n.gui.depth < 1){
            dashboard.addControl(button);
        }
        else {
            ButtonBox.addControl(button)
        }
    }
}

// button that visits a local pop. 
var createVisitButton = function(n){
    var button = BABYLON.GUI.Button.CreateSimpleButton("btn_visit_" + n.objid, "visit");
    // TODO cleanup, I found you don't need to put the "50px" as a string. 
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
        if (control_panel.hasOwnProperty('name')==false){
            control_panel.name = "window"
        }
        const label = new BABYLON.GUI.Rectangle(control_panel.name)
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