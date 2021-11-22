# Notes on setting up the environment variables for the web app service. 
* Locally I'm using conda environments because I'll do a lot of things with notebooks and such that wouldn't be used in the production env. 
* The web app service has some Azure CLI commands that I'm using to deploy the webapp there. I run these **line by line** in order to ensure that they all get deployed.

```
az webapp config show --resource-group <resource-group-name> --name <app-name> --query linuxFxVersion
```

set the vars in the App service with:
```
az webapp config appsettings set --name <app-name> --resource-group <resource-group-name> --settings @infra/env-vars.json
```

## Creating the RBAC role that communicates with GitHub and manages that deployment. 
```
az ad sp create-for-rbac --name "exodestinyAppAction" --role contributor \
                        --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
                        --sdk-auth \
                        --output json
```
* Replace {subscription-id}, {resource-group} with the subscription, resource group details

The command should output a JSON object similar to this:
This is what you put into github. 
```
{
  "clientId": "<GUID>",
  "clientSecret": "<GUID>",
  "subscriptionId": "<GUID>",
  "tenantId": "<GUID>",
  (...)
}
```