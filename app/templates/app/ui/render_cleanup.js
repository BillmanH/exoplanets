function list_all_meshes(){
    for (const mesh of scene.meshes) {
        console.log(mesh.name)
    }
}

function removeCollidingMesh(owner,tresspasser){
    // owner = the mesh that is supposed to be there, tresspasser = the mesh that is supposed to go away. 
    // both inputs are strings
    for (const mesh of scene.meshes) {
        if (mesh.name.indexOf(owner) >= 0) {
            for (const mesh2 of scene.meshes) {
                if (mesh2.name.indexOf(tresspasser) >= 0) {

                    if (mesh2.intersectsMesh(mesh)){
                        mesh2.dispose()
                    }
                }
            }
        }
    }
}

removeCollidingMesh("_faction","tree")