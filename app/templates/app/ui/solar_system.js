
    BABYLON.SceneLoader.Append("static/app/objects/", "planet.gltf", scene, function (scene) {


    });


// // var planet;
// // BABYLON.SceneLoader.ImportMesh("", "static/app/objects/", "planet.gltf", scene, function(object) {
// //         planet = object[0];
// //     });
// const sphere = BABYLON.MeshBuilder.CreateSphere("sphere", 
//                 {diameter: 2, segments: 32}, scene);
//             // Move the sphere upward 1/2 its height
//             sphere.position.y = 1;

// const planet = BABYLON.SceneLoader.Append("", "static/app/objects/", "planet.gltf", scene, function (scene){})
// const box = BABYLON.MeshBuilder.CreateBox("box", {});

// planet.position.x = 0.5;
// planet.position.y = 1;

// box.position.x = 0.5;
// box.position.y = 1;

// box.actionManager = new BABYLON.ActionManager(scene);
// box.actionManager.registerAction(new BABYLON.ExecuteCodeAction(
//     BABYLON.ActionManager.OnPickTrigger,
//     function (evt) {
//         const sourceBox = evt.meshUnderPointer;

//         //move the box upright
//         sourceBox.position.x += 0.1;
//         sourceBox.position.y += 0.1;
//     }
// )
// );