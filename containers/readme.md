# Azure Function Containers

[following the instructions here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?msclkid=c1eb6712ce8311ecbf167992dfbfb6bc&tabs=in-process%2Cbash%2Cazure-cli&pivots=programming-language-python#create-and-test-the-local-functions-project)


## Dev Cycle Steps:


### Test the function locally
```
func start
```
then test it at this url: `http://localhost:7071/api/HttpExample?name=Functions`

### Test the completed container (publish)

build it
```
docker build --tag <registry>.azurecr.io/exodestiny:v1.0.0 .
```
run it
```
docker run -p 8080:80 -it <registry>.azurecr.io/exodestiny:v1.0.0
```
then test it at this url: `http://localhost:8080/api/HttpExample?name=Functions`

### Push it to prod
There isn't a dev environment on the web, so this will push it directly into prod. Test on your local machine. 

```
docker login <registry>.azurecr.io
```
If you are using the Azure CLI, it should just grab your creds. If not, the credentials are in the `parameters_func.json` that was used to create the resource. They are .gitignore so they won't be in the repo.

Push the container:
```
docker push <registry>.azurecr.io/exodestiny:v1.0.0
```
From there, the webhook should push it to the azure functions. This happens in real time. 

