# Azure Function Containers

Azure functions run the backend of the game. All things happening that aren't controlled by the UI in `app`. All functions do some variation of running a query and then updating the graph. 

| Name | Description | Status |
|---|---|---|
| time | timer function. Some things take time to complete. This checks all of the things that are in process, and resolves them. | not yet live |
| chaos | timer function, this facilitates all of the brownian motion in the universe. It makes random things happen. | not yet live |

# Dev Cycle Steps:

## Creating a new function
You can get a list of the templates from: `func templates list`
```
func new --name <name> --template "from the template list" [--authlevel "anonymous"]
```

## Test the function locally
```
func start
```
then test it at this url: `http://localhost:7071/api/HttpExample?name=Functions`

## Test the completed container (publish)

build it
```
docker build --tag <registry>.azurecr.io/exodestiny:v1.0.0 .
```
docker build --tag <registry>.azurecr.io/exodestiny:v1.0.0 .

run it
```
docker run -p 8080:80 -it <registry>.azurecr.io/exodestiny:v1.0.0
```
then test it at this url: `http://localhost:8080/api/HttpExample?name=Functions`

## Push it to prod
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

# More useful docs:

[following the instructions here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?msclkid=c1eb6712ce8311ecbf167992dfbfb6bc&tabs=in-process%2Cbash%2Cazure-cli&pivots=programming-language-python#create-and-test-the-local-functions-project)

[`func` cli tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-core-tools-reference?msclkid=3b9f5557cf4211eca6b47532b3132c61&tabs=v2#func-templates-list)

[chron examples](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=in-process&pivots=programming-language-python#ncrontab-expressions)