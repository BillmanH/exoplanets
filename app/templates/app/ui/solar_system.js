// const planet = BABYLON.SceneLoader.Append("static/app/objects/", "planet.gltf", scene, function (scene) { });
// https://doc.babylonjs.com/typedoc/classes/BABYLON.SceneLoader#Append

function createStar(n){
    const star = BABYLON.MeshBuilder.CreateSphere(n.name, {diameter: (n.radius+n.radius)}, scene);
    star.scaling = new BABYLON.Vector3(n.radius,n.radius,n.radius);
    return star
}

function createPlanet(n){
    const planet = BABYLON.MeshBuilder.CreateSphere(n.name, {diameter: (n.radius+n.radius)}, scene);
    planet.position = new BABYLON.Vector3(0,n.orbitsDistance,n.orbitsDistance);
    return planet
}

for (let i = 0; i < solar_system.nodes.length; i++) {
    n = solar_system["nodes"][i]
    if (n["objtype"]=="star"){
        createStar(n)
        console.log("star created")
    }
    if (n["objtype"]=="planet"){
        console.log("planet created: " + n.name)
        createPlanet(n)
    }
  }



// // GUI gonna come back to it. 
// var advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI");
   
// var button1 = BABYLON.GUI.Button.CreateSimpleButton("but1", "Click Me");
// button1.width = "150px"
// button1.height = "40px";
// button1.position.y
// button1.color = "white";
// button1.cornerRadius = 10;
// button1.background = "black";
// button1.onPointerUpObservable.add(function() {
//     alert("you did it!");
// });

// advancedTexture.addControl(button1);