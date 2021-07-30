# exoplanets
side project for exploring exoplanet data

# APP
Exoplanet Game is a strategy game I've been thinking about. Super small design phase right now, but it's a solid side project. 

## Working views now: 
* `/systemmap`


## Dataset
Exoplanet data Data is gathered from here. 
### Important Links
* [Dataset column definitions](https://exoplanetarchive.ipac.caltech.edu/applications/DocSet/index.html?doctree=/docs/docmenu.xml&startdoc=item_1_01)
* [Data from this table](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS)

### Our solar system data
* [List of Solar System objects](https://en.wikipedia.org/wiki/List_of_Solar_System_objects_by_size#:~:text=Larger%20than%20400%20km%20%20%20%20Body,%20%202004%20%2013%20more%20rows%20)

* uploading that data to cosmos (once parsed) with `python scripts/upload_systems.py`

### Database (Cosmos DB)
The connection info is in the `configure.yaml` and looks like this. It is in `.gitignore` so you will need to add that file. 
```
# Web location of the cosmos DB:
endpoint: wss://<the domain of your instance>:443/

# Login Info:
username: /dbs/<dbname>/colls/<coll name>
password: <Password string from the azure portal>
```
You can test your connection with `python scripts/test_connection.py`.


## App

### Building the environment
I'm using anaconda so you should be able to build the environemnt in any system with: 
```
conda env create --file=environment.yaml
```

and update it using:
```
conda env update --name exoplanets --file=environment.yaml --prune
```

### Running the web app from the root directory. 
```
python web/manage.py runserver
```
`models.py` has two functions, one that takes a request, and another that runs a query. `run_query` takes the query text string as an imput, with a default of `"g.V().count()"`


# Contributing
Pretty early in the design right now, however I might invite collaborators later.

Make sure to update the `environment.yaml` if you add python packages:
```
conda env export --name exoplanets --from-history > environment.yaml
```