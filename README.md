# Exoplanets

[![Live web game deployment](https://github.com/BillmanH/exoplanets/actions/workflows/main_exodestiny.yml/badge.svg)](https://github.com/BillmanH/exoplanets/actions/workflows/main_exodestiny.yml)
[![Azure Function deployment](https://github.com/BillmanH/exoplanets/actions/workflows/main_exo_functions.yml/badge.svg)](https://github.com/BillmanH/exoplanets/actions/workflows/main_exo_functions.yml)


![Alt text](/docs/img/3dscene.png?raw=true "solar system")


[The work-in-progress game is here.](http://exodestiny.azurewebsites.net/), however I won't be granting access until I've completed:
* testing costs of eventhub functions running with throughput limite
* entra ID groups to manage access and subscription levels
* cost testing for consumption plans make sure I won't go broke
* resources are duplicated in a testing environment (current process is just local->prod)


Exoplanets is a real-time, multi-player, online game where you manage a civilization and its people. Starting at the moment where your technology makes it possible to launch an individual into outer space, you must make choices that guide your people on its journey to the stars.

At the start of the game, your civilization is growing rapidly. It is also consuming organic resources at a rate faster than the planet can restore. In time the resources will diminish and your people will starve and die. Your goal is to build infrastructure and technology to stabilize this.


![Alt text](/docs/img/cityview.png?raw=true "solar system")

The game is a simulation platform first, with some interaction that influences the running simulation. Your civilization is growing, consuming resources, fighting wars without your interaction. Your goal is to nudge them into a sustainable future. 

![Alt text](/docs/img/solar_system.png?raw=true "solar system")

The game is about simulation, systems-thinking and collective progress. The only adversary is the erosion of your own cosmic destiny. 

![Alt text](/docs/img/PopGrowthSystem.png?raw=true "solar system")


## Making your own game
I built this game so that I could clone it and create different versions. You should be able to clone the repo and run it on your own machine or in the cloud of your choice. Some assembly is required as this application uses a lot of tools. I'm working to keep the costs of the game down to <$20 a month. 

Of course, you can also just clone it on your local machine and run for free. Feel free to create an issue and I'll address them as I'm able. 

### Docs:
| Document |
| ----------- |
| [Building the Azure infrastructure](docs/readme.md) | 
| [Managing Azure Functions](az-functions/readme.md) | 
| [Building the Local (dev) infrastructure](docs/Local_setup.md) | 
| [Standards and Conventions](docs/Standards%20and%20Conventions.md) | 
| [Encription and password management](notebooks/Encryption_and_storage_of_passwords.ipynb) |

| The graph has lots of core elements that need to be set up for the game to function. All of that is in the notebooks. |
| the `docs` and `infra` folders contain everything else that you would need to know |


# Contributing
I designed this game as a good project for a junior developer. This might be a bit much if you've never done any programming at all, but if you know basic data transformations and logic then this game should be a good project for you. [Feel free to reach out](mailto:william.jeffrey.harding@gmail.com) or just fork the `dev` branch and make a PR. I'll test everything in `dev` before pulling it into the website, so any PRs should go to the `dev` or new `feature` branch.  

Pretty early in the design right now as I have a lot to do before I have a legit game. Also feel free to make suggestions in the `issues`. I'm so early in this concept that there are lots of design decisions remaining. 

Make sure to update the `environment.yaml` if you add python packages:
```
conda env export --name exoplanets --from-history > environment.yaml
``` 