# Exodestiny

[![Live web game deployment](https://github.com/BillmanH/exoplanets/actions/workflows/main_exodestiny.yml/badge.svg)](https://github.com/BillmanH/exoplanets/actions/workflows/main_exodestiny.yml)
[![Azure Function deployment](https://github.com/BillmanH/exoplanets/actions/workflows/main_exo_functions.yml/badge.svg)](https://github.com/BillmanH/exoplanets/actions/workflows/main_exo_functions.yml)


![Alt text](/docs/img/3dscene.png?raw=true "solar system")

## [Play the open beta game here](https://exodestiny.azurewebsites.net/)

The process will guide you through creating an account. 

The game is now in **OPEN BETA** Meaning I've still got a long way to go, but the game is playable enough where I can start opening it up to users. [How to create an account](docs/creating_a_new_account.md)

The **STAGING Enviroment** is [here](exodestiny-stage-guepbuc0bmcudnbh.westus2-01.azurewebsites.net) this should mirror the production site, but be one step ahead so that I can test things. You log into both tenants in the same way. 

# What is left to do, and when to do it:
The `dev` branch has the more current workload. Unless I get too busy with other things I'll pull those changes into `main` every month (depending on how much time I have to spend on it). 


## **BETA - RELEASE** - Should be playable, but will still have a lot to go.

## April
* Planetary observation
    - Building the planetary observation building should enable you to scan the skies to find new celestial bodies. 
* Ship Building
    - Should be able to build ships and store ships in a shipyard

## May
* Launching ships - being able to launch ships into space
* Tracking space voyages and destinations
* Being able to view worlds that have been 'observed'



Exoplanets is a real-time, multi-player, online game where you manage a civilization and its people. Starting at the moment where your technology makes it possible to launch an individual into outer space, you must make choices that guide your people on its journey to the stars. This game was built at a very slow pace over the course of several years.

At the start of the game, your civilization is growing rapidly. It is also consuming organic resources at a rate faster than the planet can restore. In time the resources will diminish and your people will starve and die. Your goal is to build infrastructure and technology to stabilize this.

![Alt text](/docs/img/cityview.png?raw=true "local view")

The game is a simulation platform first, with some interaction that influences the running simulation. Your civilization is growing, consuming resources, fighting wars without your interaction. Your goal is to nudge them into a sustainable future. 

![Alt text](/docs/img/solar_system.png?raw=true "solar system")

The game is about simulation, systems-thinking and collective progress. The only adversary is the erosion of your own cosmic destiny. 

![Alt text](/docs/img/PopGrowthSystem.png?raw=true "pop growth system")


## Making your own game
I built this game so that I could clone it and create different versions. You should be able to clone the repo and run it on your own machine or in the cloud of your choice. Some assembly is required as this application uses a lot of tools. I'm working to keep the costs of the game down to ~$20 a month. 

![Alt text](/docs/img/Infra.png?raw=true "Architecture")
    

Of course, you can also just clone it on your local machine and run for free. Feel free to create an issue and I'll address them as I'm able. 

### Docs:
| Document |
| ----------- |
| [Building the Azure infrastructure](docs/readme.md) | 
| [Building the Local (dev) infrastructure](docs/local_setup.md) | 
| [Standards and Conventions](docs/Standards%20and%20Conventions.md) | 

| The graph has lots of core elements that need to be set up for the game to function. All of that is in the notebooks. |
| the `docs` and `infra` folders contain everything else that you would need to know |


# Contributing
I designed this game as a good project for a junior developer. This might be a bit much if you've never done any programming at all, but if you know basic data transformations and logic then this game should be a good project for you. [Feel free to reach out](mailto:william.jeffrey.harding@gmail.com) or just fork the `dev` branch and make a PR. I'll test everything in `dev` before pulling it into the website, so any PRs should go to the `dev` or new `feature` branch.  

Pretty early in the design right now as I have a lot to do before I have a legit game. Also feel free to make suggestions in the `issues`. I'm so early in this concept that there are lots of design decisions remaining. 

Make sure to update the `environment.yaml` if you add python packages:
```
conda env export --name exoplanets --from-history > environment.yaml
``` 