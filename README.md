# Exoplanets
Exoplanets is a real-time, multi-player, online game where you manage a civilization and it's people. Starting at the moment where your technology makes it possible to launch an individual into outer space, you must make choices that guide your people on it's journey to the stars.

The game is procedurally generated based on public datasets regarding space exploration. The back end is built to rely on open source tools that are common to the data science stack such as d3.js and Jupyter. Also, the goal is to make the platform easy to clone and extend into other games. 

[![Build and deploy Python app to Azure Web App - exodestiny](https://github.com/BillmanH/exoplanets/actions/workflows/build_and_deploy.yaml/badge.svg)](https://github.com/BillmanH/exoplanets/actions/workflows/build_and_deploy.yaml)

![Alt text](/docs/img/solar_system.png?raw=true "solar system")

* Azure App Service
* Django Web Server
* Azure App Service for Hosting
* Azure Cosmos DB (Gremlin)
* D3.js for visualization


## Dataset
Exoplanet data Data is gathered from here. 
### Important Links
* [Dataset column definitions](https://exoplanetarchive.ipac.caltech.edu/applications/DocSet/index.html?doctree=/docs/docmenu.xml&startdoc=item_1_01)
* [Data from this table](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS)

### Our solar system data
* [List of Solar System objects](https://en.wikipedia.org/wiki/List_of_Solar_System_objects_by_size#:~:text=Larger%20than%20400%20km%20%20%20%20Body,%20%202004%20%2013%20more%20rows%20)

* uploading that data to cosmos (once parsed) with `python scripts/upload_systems.py`


## Making your own game
I built this game so that I could clone it and create different versions. You should be able to clone the repo and run it on your own machine or in the cloud of your choice. Some assembly required as this application uses a lot of tools. I'm working to keep the costs of the game down to <$20 a month. 

of course, you can also just clone it on your local machine and run for free. Feel free to create an issue and I'll address them as I'm able. 

### Docs:
| Document |
| ----------- |
| [Building the Azure infrastructure](docs/Technical%20Architecture.md) | 
| [Building the Local (dev) infrastructure](docs/Technical%20Architecture.md) | 
| The graph has lots of core elements that need to be set up for the game to function. All of that is in the notebooks. |
| the `docs` and `infra` folders contain everything else that you would need to know |


# Contributing
Pretty early in the design right now, but feel free to make a PR and I'll review. Also feel free to make suggestions in the `issues`. I'm so early in this concept that there are lots of design decisions still remaining. 

Make sure to update the `environment.yaml` if you add python packages:
```
conda env export --name exoplanets --from-history > environment.yaml
```