// const planet = BABYLON.SceneLoader.Append("static/app/objects/", "planet.gltf", scene, function (scene) { });
// https://doc.babylonjs.com/typedoc/classes/BABYLON.SceneLoader#Append


var scale_radius = d3.scaleLinear()
            .domain(get_values(solar_system["nodes"],"radius", "planet"))
            .range([1,20]);


var scale_distance = d3.scaleLog()
            .domain(get_values(solar_system["nodes"],"orbitsDistance", "planet"))
            .range([20,100]);

function createStar(n){
    const star = BABYLON.MeshBuilder.CreateSphere(n.name, {diameter: scale_radius(n.radius)});
    // const material = new BABYLON.StandardMaterial("app");
    star.ambientColor = new BABYLON.Color3(249, 180, 24);
    return star
}

function createPlanet(n){
    const planet = BABYLON.MeshBuilder.CreateSphere(n.name,  {diameter: scale_radius(n.radius)});
    planet.position = new BABYLON.Vector3(0,0,scale_distance(n.orbitsDistance));

    const torus = BABYLON.MeshBuilder.CreateTorus(n.name+"-ring", {diameter: scale_distance(n.orbitsDistance)});
    return planet
}

for (let i = 0; i < solar_system.nodes.length; i++) {
    n = solar_system["nodes"][i]
    if (n["objtype"]=="star"){
        createStar(n)
        console.log("star: " + n.name +"; radius: "+ n.radius)
    }
    if (n["objtype"]=="planet"){
        console.log("planet: " + n.name +"; radius: "+ n.radius +" ("+scale_radius(n.radius)+")" + "; orbitsDistance: " + n.orbitsDistance )
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