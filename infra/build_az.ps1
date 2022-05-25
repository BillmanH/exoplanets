# I generally run this one section at a time, not all at once. 

# Script variables:
$resourceGroupName = "exodestiny"
$location = "West US 2"
# swithc to the env that has the local variables
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


# Creating the azure functions separately until I get it figured out. 
az deployment group create --resource-group $resourceGroupName --template-file "infra/ARM/template_func.json" --parameters "infra/ARM/parameters_func.json"

