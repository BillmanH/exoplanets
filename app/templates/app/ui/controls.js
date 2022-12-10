
// // GUI gonna come back to it. 
var advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI");
var button1 = BABYLON.GUI.Button.CreateSimpleButton("but1", "Click Me");

button1.width = "150px"
button1.height = "40px";

button1.color = "white";
button1.cornerRadius = 10;
button1.background = "black";

// button1.onPointerUpObservable.add(function() {
//     alert("you did it!");
// });

advancedTexture.addControl(button1);