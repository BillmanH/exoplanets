# Building the Infrastructure. 
In this case I'm using Azure ARM templates. This makes it easy to store the infrastructure as version control. If I've done everything correctly you should be able to build everything from the command line using `az cli`. I'm building it all form the command line rather than a special build as I don't intend to be building the infrastructure often. 

**You'll need a parameters.json** That has you special keys and resource names. It is in the `.gitignore` here. 

## Steps
Assuming you've already set the local environment variables per the instructions in the `readme.md` you can follow these CLI steps. Some of the env variables won't be available until you complete the azure build steps, but you should already have the ones required to complete this step. 
```
az login
az account set --subscription $Env:subscription
cd $Env:abspath
```
That should label the subscription and the name. Then you just run the resources. **NOTE** see the `build_az.ps1` for the steps as they are actually run. When I run that script, I don't run the entire thing. I copy/paste chunks into repl and run them individually to test things out. The comments in the script should walk you through the process. 
```
az deployment group create --resource-group $resourceGroupName --template-file "infra/ARM/template.json" --parameters "infra/ARM/parameters.json"
```
**NOTE** you will need to provide the `parameters.json` yourself. It's where the secrets are and is in the gitignore. 

## Open AI
While I'm testing out the chatGPT components, I'm beginning to create a branch around this. Because the componets are just being tested the infrastructure for them is held separately. The goal is to loop them into a single deployment. 
```
az deployment create --resource-group $resourceGroupName --template-file "infra/ARM/openai_template.json" --parameters "infra/ARM/openai_parameters.json"
```


## Keys and passwords
For rback roles and env vars there is a `.key` file that is in the gitignore. It is json shaped. 


