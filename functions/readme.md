# Azure Function Containers

Azure functions run the backend of the game. All things happening that aren't controlled by the UI in `app`. All functions do some variation of running a query and then updating the graph. 

| Name | Description | Status |
|---|---|---|
| time | timer function. Some things take time to complete. This checks all of the things that are in process, and resolves them. | not yet live |
| chaos | timer function, this facilitates all of the brownian motion in the universe. It makes random things happen. | not yet live |
| HttpExample | http function. Just keeping it as a template. Not involved in the game. | template |

# Dev Cycle Steps:
**Note** I switched from container to regular az functions as I found them easier to troubleshoot and view logs . 

![Alt text](/docs/img/container_cicd.png?raw=true "docker cicd")

## Creating the local development environment
The Azure Func Tools don't support conda environments, so I'm using a regular python env. This will need to be done anytime `requirements.txt` is updated OR when the environment variables are reset. This is just for the local environment. 
```
python -m venv .venv
.venv\scripts\activate
pip install -r requirements.txt
```

## Updating the environment in the cloud:

to get the settings into your local file:
```
az webapp config appsettings list --name <app-name> --resource-group <group-name> > application_settings.json
```
To update those settings: 
```
az webapp config appsettings set --resource-group <group-name> --name <app-name> --settings @application_settings.json
```

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


## Push it to prod
There isn't a dev environment on the web, so this will push it directly into prod. Test on your local machine. Then the deploy function within VSC is used to push the function into prod. This means that the code for functions is updated differently than the webapp (wich updates on a GH action). I'll add that to the CICD process at some point. 

# More useful docs:

[following the instructions here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?msclkid=c1eb6712ce8311ecbf167992dfbfb6bc&tabs=in-process%2Cbash%2Cazure-cli&pivots=programming-language-python#create-and-test-the-local-functions-project)

[`func` cli tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-core-tools-reference?msclkid=3b9f5557cf4211eca6b47532b3132c61&tabs=v2#func-templates-list)

[chron examples](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=in-process&pivots=programming-language-python#ncrontab-expressions)