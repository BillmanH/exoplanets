# Notes on setting up the environment variables for the web app service. 
* Locally I'm using conda environments because I'll do a lot of things with notebooks and such that wouldn't be used in the production env. 
* The web app service has some Azure CLI commands that I'm using to deploy the webapp there. I run these **line by line** in order to ensure that they all get deployed.
* Some of the build scripts, including the build_az.ps1 are _work in progress_ and may need some fine tuning. 

```
az webapp config show --resource-group <resource-group-name> --name <app-name> --query linuxFxVersion
```

## Setting evnironment variables in Azure App Service
It is important that the environment variables in your local environment match the one you have in the cloud.  
set the vars in the App service with:
```
az webapp config appsettings set --name <app-name> --resource-group <resource-group-name> --settings @infra/env-vars.json
```
That requires that you have a `env-vars.json` file, which is in the gitignore. All of the variables are updated in the root/readme.md but just for formatting, the Json looks like this:
```
{
    "endpoint": "wss://foo.com:443/",
    "dbusername": "/dbs/graphdb/colls/db",
    "dbkey": "longstring",
    "abspath": ".",
    "subscription": "sub",
    "SECRET_KEY": "key",
    "ALLOWED_HOSTS": "site.azurewebsites.net",
    "stage": "prod",
    "sqluser": "admin",
    "sqlpwd": "pwd",
    "sqlserv": "db.database.windows.net",
    "sqlname": "Home",
    "AZURE_STORAGE_KEY": "key",
    "AZURE_ACCOUNT_NAME": "blob",
    "AZURE_STATIC_CONTAINER": "static"
}
```
A good way to know what variables you need is to search for `os.getenv` in the code. In VSCode this is done with `ctrl`+`shft`+`f`

To get the list of local variables (to ensure that local _dev_ and cloud _prod_ match):
```
conda env config vars list
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
This is what you put into github. **The Whole json**
```
{
  "clientId": "<GUID>",
  "clientSecret": "<GUID>",
  "subscriptionId": "<GUID>",
  "tenantId": "<GUID>",
  (...)
}
```
