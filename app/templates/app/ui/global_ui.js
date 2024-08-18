
var dashboard = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI");
var icon_config = {padding:70,initial:20} // distance between icons.

//global textbox in upper left corner.
var textblock = new BABYLON.GUI.TextBlock("textblock")
    textblock.textHorizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_RIGHT;
    textblock.textVerticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP
    textblock.fontSize = 24;    
    textblock.background = "black";
    textblock.color = "white";    
    textblock.paddingRight = 20
    textblock.paddingTop = 20

dashboard.addControl(textblock);

var troubleshooter = new BABYLON.GUI.TextBlock("troubleshoot_box")
    troubleshooter.textHorizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_RIGHT;
    troubleshooter.textVerticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_BOTTOM
    troubleshooter.fontSize = 10;    
    troubleshooter.background = "black";
    troubleshooter.color = "white";    
    troubleshooter.paddingRight = 20
    troubleshooter.paddingTop = 20
    var troubleshooting = {"name":"dev","objtype":"window","width":window.screen.width}
    troubleshooter.text = dictToSimpleText(troubleshooting)
    dashboard.addControl(troubleshooter);


function dropControlIfExists(name){
    if(dashboard.getControlByName(name)){
        dashboard.getControlByName(name).dispose()
    }
}

function getIconTop(iter){
    return (iter*icon_config.padding) + icon_config.initial
}

function dropAllControls(){
    dropControlIfExists("events_window")
    dropControlIfExists("action_window")
    dropControlIfExists("faction_window")
    dropControlIfExists("buildings_window")
    dropControlIfExists("window")
    dropControlIfExists("planets_window")
    dropControlIfExists("resources_window")
    dropControlIfExists("loadingpleasewait")
}

var objectDetails = function(d){
    textblock.text = dictToSimpleText(d);
}

function createControlBox(control_panel){
    if (control_panel.hasOwnProperty('name')==false){
        control_panel.name = "window"
    }
    if (control_panel.hasOwnProperty('title')==false){
        control_panel.title = "this text box has no title"
    }
    const label = new BABYLON.GUI.Rectangle(control_panel.name)
        label.background = 'black'
        label.top = control_panel.top 
        label.left = control_panel.left 
        label.width = control_panel.width
        label.height = control_panel.height

        label.alpha = 0.5

        label.cornerRadius = 5
        label.thickness = 1
        label.linkOffsetY = 30

    label.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
    label.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
    dashboard.addControl(label);

    // TODO: Close button not always on screen. 
    var closeButton = BABYLON.GUI.Button.CreateSimpleButton("btn_close", "X");
        closeButton.background = 'black'
        closeButton.top = 5
        closeButton.left = 5
        closeButton.width = "25px"
        closeButton.height = "25px"
        closeButton.color = "white"
        closeButton.cornerRadius = 5
        closeButton.thickness = 1
        closeButton.linkOffsetY = 30

        closeButton.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        closeButton.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;

    label.addControl(closeButton);

    var textblock = new BABYLON.GUI.TextBlock("title_textblock")
        textblock.textHorizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
        textblock.textVerticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP
        textblock.textWrapping = true;
        label.addControl(textblock);

        textblock.paddingTop = 10 
        textblock.paddingLeft = 40 
        textblock.fontSize = 18;    
        textblock.background = "black";
        textblock.color = "white";    
        textblock.text = control_panel.title
        

    closeButton.onPointerUpObservable.add(function() {
        dashboard.getControlByName(control_panel.name).dispose()
    });

    // label.control_metadata = control_panel
    return label
}

var addTextBlockToBox = function(n,box){
    var box_height = n.displayed_values.length * 25
    
    const label = new BABYLON.GUI.Rectangle("text_block")
        label.background = 'black'
        label.top = (box_height * n.iter)
        label.left = 5
        label.width = box.width
        label.height = box_height.toString() + "px"
        label.paddingLeft = 2
        label.paddingRight = 2
        
        label.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        label.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
    box.addControl(label);


    var resourceText = new BABYLON.GUI.TextBlock("resource_text"+n.iter.toString())
        resourceText.textHorizontalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_LEFT;
        resourceText.textVerticalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
        resourceText.paddingTop = 5
        resourceText.paddingLeft = 5 
        resourceText.fontSize = 12;    
        resourceText.background = "black";
        resourceText.color = "white";   
        resourceText.text = dictToSingleLIne(n.data, n.displayed_values)
        resourceText.textWrapping = true
        
        label.addControl(resourceText);
}

// for buttons creatd dynamically, for example the children of an item
var addButtonToBox = function(n,control) {
    var buttonText = "button";
    var buttonName = "btn_";
    if (n.data.hasOwnProperty('name')==false){
        n.data.name = cs(n.data.type)
    }
    if (n.gui.hasOwnProperty('buttonName')==false){
        buttonName = n.gui.buttonName
    }
    if (n.gui.hasOwnProperty('buttontext')){
        buttonText = n.gui.buttontext
    } else {
        buttonText = n.data.name
    }

    var button = BABYLON.GUI.Button.CreateSimpleButton(buttonName + n.data.objid, buttonText);
        if(n.gui.hasOwnProperty('width')){
            button.width = n.gui.width
        } else {button.width = "150px"}
        button.height = "40px"
        button.top = 50 * n.iter
        if(n.gui.buttonColor=="green"){
            button.left = 170
        } else {
            button.left = 20
        }
        
        button.color = n.gui.buttonColor;
        button.cornerRadius = 10;
        button.background = "black";
        button.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
        button.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;


        if(n.gui.hasOwnProperty('text_button')){
            const buttonDescription = new BABYLON.GUI.Rectangle("text_block")
            buttonDescription.background = 'black'
            buttonDescription.top = button.top 
            buttonDescription.left =  pxToNum(button.left) + pxToNum(button.width) + 10
            buttonDescription.width = (pxToNum(control.width)-pxToNum(button.width) - 40 ).toString() + "px"
            buttonDescription.height = button.height
            buttonDescription.paddingLeft = 2
            buttonDescription.paddingRight = 2
            
            buttonDescription.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
            buttonDescription.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;

            var textblock = new BABYLON.GUI.TextBlock("buttonDescription_text")
                textblock.textHorizontalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_CENTER;
                textblock.textVerticalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT
                textblock.background = "black";
                textblock.color = "white";  
                textblock.fontSize = 14; 
                textblock.textWrapping = true; 
                textblock.text = dictToSingleLIne(n.data, n.gui.displayed_values) 
            buttonDescription.addControl(textblock);

            control.addControl(buttonDescription);
            

            textblock.onPointerUpObservable.add(function() {objectDetails(n.data)})
        }

        control.addControl(button)
        switch(n.gui.buttonName){
            case "get_actions_":
                if (n.gui.hasOwnProperty('actionButton')){
                    button.onPointerUpObservable.add(function() {n.gui.actionButton(n)});
                }
            case "visit_":
                if (n.gui.hasOwnProperty('visitButton')){
                    button.onPointerUpObservable.add(function() {n.gui.visitButton(n)});
                }
            default:
                button.onPointerUpObservable.add(function() {n.gui.clickButton(n)});
        }
    }




var addTextToControl = function(n,control){
    // TODO: Missing text for actions
}

function pleaseWaiter(d){
    const label = new BABYLON.GUI.Rectangle("loadingpleasewait")
    label.background = 'black'
    label.top = 50
    label.left = 50
    
    label.width = "600px"
    label.height = "600px"

    label.thickness = 1
    label.linkOffsetY = 30

    label.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_CENTER;
    label.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_CENTER;
    d.addControl(label);

    var textblock = new BABYLON.GUI.TextBlock("loadingpleasewait_text")
        textblock.textHorizontalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_CENTER;
        textblock.textVerticalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_CENTER
        textblock.fontSize = 24;    
        textblock.background = "black";
        textblock.color = "white";   
        
        textblock.text = "Loading please wait ..."
        textblock.text += "\n"
        
    label.addControl(textblock);

    return label
}

function hoverTooltip(obj){
    dropControlIfExists("uiTooltip")
    if(obj.hasOwnProperty('metadata')){
        // console.log(obj.metadata.name)
        var ttheight = 15
        if(obj.metadata.hasOwnProperty("data")){
            var heightmod = Object.keys(obj.metadata.data).length
        } else {
            var heightmod = Object.keys(obj.metadata).length
        }        
        var rect1 = new BABYLON.GUI.Rectangle("uiTooltip");
            dashboard.addControl(rect1);
            rect1.width = "300px";
            rect1.height = (ttheight * heightmod).toString() + "px";
            rect1.thickness = 2;        
            rect1.linkOffsetX = "200px";
            rect1.linkOffsetY = "-100px";
            rect1.background = "black";
            rect1.alpha = 0.7;
            rect1.cornerRadius = 5
            rect1.linkWithMesh(obj);    

        var text1 = new BABYLON.GUI.TextBlock();
        if(obj.metadata.hasOwnProperty("data")){
            text1.text = dictToSimpleText(obj.metadata.data)
        } else {
            text1.text = dictToSimpleText(obj.metadata)
        }
            text1.color = "White";
            text1.fontSize = 14;
            text1.textWrapping = true;
            text1.textVerticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
            text1.textHorizontalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_LEFT;
            text1.background = '#006994'
            rect1.addControl(text1)
            text1.alpha = (1/text1.parent.alpha);
            text1.paddingTop = "20px";
            text1.paddingBottom = "20px";
            text1.paddingLeft = "20px";
            text1.paddingRight = "20px";
    }

}

function create_icon(params){
    var icon = BABYLON.GUI.Button.CreateImageOnlyButton(params.name, params.image);
    icon.width = "60px";
    icon.height = "60px";
    icon.top = params.top
    icon.left = 20
    icon.color = "white";
    icon.stretch = BABYLON.GUI.Image.STRETCH_EXTEND;
    icon.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
    icon.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
    dashboard.addControl(icon)
    return icon
}


// One off small functions
function pxToNum(px){
    var i = parseInt(px.replace(/px/g, ""))
    return i
}

function removeCollidingMesh(owner,tresspasser){
    // owner = the mesh that is supposed to be there, tresspasser = the mesh that is supposed to go away. 
    // both inputs are strings
    for (const mesh of scene.meshes) {
        if (mesh.name.indexOf(owner) >= 0) {

            console.log('ownermesh: ',mesh.name)
            for (const mesh2 of scene.meshes) {
                if (mesh2.name.indexOf(tresspasser) >= 0) {

                    if (mesh2.intersectsMesh(mesh)){

                        mesh2.material = new BABYLON.StandardMaterial("matBallon");
                        mesh2.material.emissiveColor = new BABYLON.Color3(1, 0, 0);
                        console.log(mesh2.name,' collides with ',mesh.name, " at ", mesh2.position.x, mesh.position.x)
                    }
                }
            }
        }
    }
}

function removeSingleCollsion(obj,toCheck){
    for (const mesh of scene.meshes) {
        if ((mesh.name.indexOf(toCheck) >= 0)){
            if (mesh.intersectsMesh(mesh,true)){
                mesh.dispose()
                console.log(mesh.name,' collides with ',mesh2.name )
            }
        }
    }
}

scene.onKeyboardObservable.add((kbInfo) => {
    switch (kbInfo.type) {
        case BABYLON.KeyboardEventTypes.KEYDOWN:
        switch (kbInfo.event.key) {
        case "x":
        case "X":
            dropAllControls()
        break
        }
        break;
        }
    }); 


function get_clicked_mesh(){
    var pickResult = scene.pick(scene.pointerX, scene.pointerY);
    if (pickResult.hit) {
        console.log(pickResult.pickedMesh.name)
    }
    return pickResult.pickedMesh
}