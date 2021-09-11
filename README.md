# Django / CosmosDB web app framework

A Gremlin Graph database driven Dajngo App.  Useful as a template for other applications that use Django and Graph Databases. 

![Alt text](/docs/img/solar_system.png?raw=true "solar system")

* Django Web Server
* Azure Cosmos DB (Gremlin)
* D3.js for visualization

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

You can confirm the environments are there with: 
```
conda env config vars list
```
When the app runs, if you see `"env vars not set"` in your error messages it meas that the os.env variables aren't set. 

### Running the web app from the root directory. 
```
python web/manage.py runserver
```

You can also access the DB in `notebooks` with the DB helper tools.

# Contributing
Pretty early in the design right now, however I might invite collaborators later.

Make sure to update the `environment.yaml` if you add python packages:
```
conda env export --name exoplanets --from-history > environment.yaml
```