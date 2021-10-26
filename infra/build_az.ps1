# Script variables:
$resourceGroupName = "exodestiny"
$location = "West US 2"
# swithc to the env that has the local variables
conda activate exoplanets

# start the interactive login
az login
az account set --subscription $Env:subscription
cd $Env:abspath


# az group create -l $location -n $resourceGroupName
# az group delete --name $resourceGroupName


# *_parameters are in the .gitignore 
# Graph database
az deployment group create --resource-group $resourceGroupName --template-file "infra/ARM/cosmos_db_template.json" --parameters "infra/ARM/cosmos_db_parameters.json"

# Web App
az deployment group create --subscription $Env:subscription --resource-group $resourceGroupName --template-file "infra/ARM/webapp_template.json" --parameters "infra/ARM/webapp_parameters.json"