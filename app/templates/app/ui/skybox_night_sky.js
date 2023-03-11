{% load static %}

var skybox = BABYLON.Mesh.CreateBox('skybox', 10000);
var skyboxMaterial = new BABYLON.StandardMaterial('skyboxMat');

skyboxMaterial.backFaceCulling = false;
skyboxMaterial.infiniteDistance = true;

skyboxMaterial.diffuseColor = new BABYLON.Color3(0,0,0)
skyboxMaterial.specularColor = new BABYLON.Color3(0,0,0)

//texture of six sides
skyboxMaterial.reflectionTexture = new BABYLON.CubeTexture("{% static 'app/objects/skybox/pixel_stars/hudf_hst' %}");
skyboxMaterial.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE; 

skybox.material = skyboxMaterial;