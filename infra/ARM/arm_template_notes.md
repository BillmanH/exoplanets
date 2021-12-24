# Building the Infrastructure. 
In this case I'm using Azure ARM templates. This makes it easy to store the infrastructure as version control. If I've done everything correctly you should be able to build everything from the command line using `az cli`. I'm building it all form the command line rather than a special build as I don't intend to be building the infrastructure often. 

**You'll need a parameters.json** That has you special keys and resource names. It is in the `.gitignore` here. 

## Steps
Assuming you've already set the local environment variables per the instructions in the `readme.md` you can follow these CLI stepps. Some of the env variables won't be available until you complete the azure build steps, but you should already have the ones required to complete this step. 
```
az login
az account set --subscription $Env:subscription
cd $Env:abspath
```
That should label the subscription and the name. Then you just run the resources. **NOTE** see the `build_az.ps1` for the steps as they are actually run. 
```
az deployment group create --resource-group $resourceGroupName --template-file "infra/ARM/template.json" --parameters "infra/ARM/parameters.json"
```


