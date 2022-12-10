// const planet = BABYLON.SceneLoader.Append("static/app/objects/", "planet.gltf", scene, function (scene) { });
// https://doc.babylonjs.com/typedoc/classes/BABYLON.SceneLoader#Append
{% load static %}

star_base = 10

function createStar(n){
    const star = BABYLON.MeshBuilder.CreateSphere(n.name, {diameter: star_base});
    const surface = new BABYLON.StandardMaterial("{% static 'app/objects/star.jpg' %}");
    star.material = surface
    return star
}

function createPlanet(n){
    const planet = BABYLON.MeshBuilder.CreateSphere(n.name,  {diameter: scale_radius(n.radius)});
    planet.position = new BABYLON.Vector3(0,0,scale_distance(n.orbitsDistance));

    return planet
}

for (let i = 0; i < solar_system.nodes.length; i++) {
    n = solar_system["nodes"][i]
    if (n["objtype"]=="star"){
        createStar(n)
    }
    if (n["objtype"]=="planet"){
        createPlanet(n)
    }
  }


