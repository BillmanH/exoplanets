# I generally run this one section at a time, not all at once. 

# Script variables:
$resourceGroupName = "exodestiny-stage"
$location = "West US 2"
# switch to the env that has the local variables
conda activate exoplanets

# start the interactive login
az login
az account set --subscription $Env:subscription
cd $Env:abspath

# # Only need to do this when creating the new resource group:
# az group create -l $location -n $resourceGroupName
# az group delete --name $resourceGroupName

# *_parameters are in the .gitignore 
# Single turnkey resources from template. 
az deployment group create --resource-group $resourceGroupName --template-file "infra/ARM/template.json" --parameters "infra/ARM/parameters.json"


# Open AI is it's own thing as well
az deployment group create --resource-group $resourceGroupName --template-file "infra/ARM/openai_template.json" --parameters "infra/ARM/openai_parameters.json"

