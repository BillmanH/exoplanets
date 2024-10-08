# exoplanets
A Gremlin Graph database driven strategy game. Get your civilization out into space. 

![Alt text](/docs/img/Infra.png?raw=true "infra")

* Django Web Server
* Azure App Service for Hosting
* Azure Functions for local hosting
* Azure Entra ID for login/identity management
* Azure Cosmos DB (Gremlin)
* D3.js for charts and 2d viz
* Babylon.js for 3d viz

## Dataset
Exoplanet data Data is gathered from here. 
### Important Links
* [Dataset column definitions](https://exoplanetarchive.ipac.caltech.edu/applications/DocSet/index.html?doctree=/docs/docmenu.xml&startdoc=item_1_01)
* [Data from this table](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS)

### Our solar system data
* [List of Solar System objects](https://en.wikipedia.org/wiki/List_of_Solar_System_objects_by_size#:~:text=Larger%20than%20400%20km%20%20%20%20Body,%20%202004%20%2013%20more%20rows%20)

* uploading that data to cosmos (once parsed) with `python scripts/upload_systems.py`

### Database (Cosmos DB)
The connection info is in the `configure.yaml` and looks like this. It is in `.gitignore` so you will need to add that file. The format of of `configure.yaml` is as follows:
```
# Web location of the cosmos DB:
endpoint: wss://<the domain of your instance>:443/

# Login Info:
username: /dbs/<dbname>/colls/<coll name>
password: <Password string from the azure portal>
```
You can test your connection with `python scripts/test_connection.py`.

**NOTE:** while the game uses the graph database, the AUTH credentials are stored separately in the local `db.sqlite3`

## Making your own game
I built this game so that I could clone it and create different versions. You should be able to clone the repo and run it on your own machine or in the cloud of your choice. Some assembly required as this application uses a lot of tools. I'm working to keep the costs of the game down to <$20 a month. 

Note that the Azure Entra ID, Cosmos DB, and some of the components require some customization. Feel free to reach out if you are having trouble getting it running. 

* see the docs in the **infra** folder for production deployment. 

### Building the local testing environment
You can run the application on your local machine without cloud resources. I'm using anaconda so you should be able to build the environment in any system with: 
```
conda env create --file=environment.yaml
``` 

and update it using:
```
conda env update --name exoplanets --file=environment.yaml --prune
```

To access the cosmos DB, you'll need to setup the environment variables. 
```
conda env config vars set endpoint=<copy paste from azure portal>
```
you'll need to add the variables one at a time. I don't have a script for this but the format is simple. 

**NOTE** I created a ps script that syncs between local and cloud. Have a look at `setting_local-env_vars.ps1` in the _infra_ folder. 

### Variables for the base Django
| Syntax | Description | Notes |
| ----------- | ----------- | ----------- |
| stage | (`dev` or `prod` affects how the `settings.py` file will be used.) | |
| SECRET_KEY | django web key used for dev | |
| ALLOWED_HOSTS | djengo settings, for specifying endpoint | it's a pipe-delimited string eg. `192.168.0.1\|mywebsite.com` |
| abspath | absolute path of your project (for resolving relative path loading issues (like using jupyter)) | |

#### Variables for the gremlin graph
| Syntax | Description | Notes |
| ----------- | ----------- | ----------- |
| endpoint | web endpoint of your gremlin graph |  |
| dbusername | graph login username | |
| dbkey | copy paste from azure portal | |

#### Azure Resources (ARM etc.)
| Syntax | Description | Notes |
| ----------- | ----------- | ----------- |
| subscription | azure subscription id (for building resources) | |

#### Azure Storage
| Syntax | Description | Notes |
| ----------- | ----------- | ----------- |
| AZURE_STORAGE_KEY | From the portal | |
| AZURE_ACCOUNT_NAME | From the portal |  |
| AZURE_STATIC_CONTAINER | From the portal |  |

#### Azure Event Hub
| Syntax | Description | Notes |
| ----------- | ----------- | ----------- |
| EVENT_HUB_FULLY_QUALIFIED_NAMESPACE | From the portal | |
| EVENT_HUB_NAME | From the portal |  |
| EVENT_HUB_CONNECTION_STR | From the portal |  |

### Azure Entra ID
| Syntax | Description | Notes |
| ----------- | ----------- | ----------- |
| AAD_CLIENT_CREDENTIAL | From the portal | |
| AAD_TENANT_ID | From the portal |  |
| AAD_CLIENT_CREDENTIAL | From the portal |  |


I'm always importing modules from different places, so to compensate to multiple relative scopes for static resources (like city names and planet configuration.yaml files) I pass the _full path_ as an os env so that I can retrieve it.  for example on my local machine it's set to:"
```
conda env config vars set abspath="C:\Users\william.harding\Documents\repos\exoplanets"
```

You can confirm the environments are there with: 
```
conda env config vars list
```
When the app runs, if you see `"env vars not set"` in your error messages it meas that the os.env variables aren't set. 

You will need the `settings.py` file. Copy it from the `TEMPLATESETTINGS.py` and change to suit your purpose. 

### Running the web app from the root directory. 
**Most** of this is in the django docs. 

```
python manage.py runserver
```
If this is your first time building the application, you will need to update the login data using:
```
python manage.py makemigrations
python manage.py migrate
```

**NOTE** You can also access the DB in `notebooks` with the DB helper tools.

### Migrating Static to Azure
To host static files in Azure you'll need to create a public blob (recommended). In the portal, create a new container, and change it's `Public access level` to `blob`. In my version both the local dev and could use the blob and not locally hosted files. 

# Contributing
Pretty early in the design right now, however I might invite collaborators later. Feel free to open an issue if you want to chat about contributing, or just make a PR. 

Make sure to update the `environment.yaml` if you add python packages:
```
conda env export --name exoplanets --from-history > environment.yaml
```