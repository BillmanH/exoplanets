# exoplanets
A Gremlin Graph database driven strategy game. Get your civilization out into space. 

![Alt text](/docs/img/solar_system.png?raw=true "solar system")

* Django Web Server
* Azure Cosmos DB (Gremlin)
* D3.js for visualization

## DEV
Check out the Dev Branch for what I'm currently working on. This project flow is just working in DEV and pulling into MAIN. 

# APP
Exoplanet Game is a strategy game I've been thinking about. Super small design phase right now, but it's a solid side project. 

## Features thus far:
* [Solar systems with stars, planets and moons](/notebooks/Analysis%20-%20planet%20summary%20stats.ipynb)
* [Populations (pops) with factions, and spiecies attributes](/notebooks/People/Generating%20Populations.ipynb)

## Working views now: 
* `/systemmap` <- look at your system
* `/new` < - create a new system


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


## Getting Started.

### Building the environment
I'm using anaconda so you should be able to build the environemnt in any system with: 
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
conda env config vars set dbusername=<copy paste from azure portal>
conda env config vars set dbkey=<copy paste from azure portal>
```

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
```
python web/manage.py runserver
```
If this is your first time building the application, you will need to update the login data using:
`python manage.py makemigrations`


**NOTE** You can also access the DB in `notebooks` with the DB helper tools.

# Contributing
Pretty early in the design right now, however I might invite collaborators later.

Make sure to update the `environment.yaml` if you add python packages:
```
conda env export --name exoplanets --from-history > environment.yaml
```