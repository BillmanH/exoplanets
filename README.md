# Exodestiny

[![Live web game deployment](https://github.com/BillmanH/exoplanets/actions/workflows/main_exodestiny.yml/badge.svg)](https://github.com/BillmanH/exoplanets/actions/workflows/main_exodestiny.yml)
[![Azure Function deployment](https://github.com/BillmanH/exoplanets/actions/workflows/main_exo_functions.yml/badge.svg)](https://github.com/BillmanH/exoplanets/actions/workflows/main_exo_functions.yml)


![Alt text](/docs/img/3dscene.png?raw=true "solar system")

## [Play the open beta game here](https://exodestiny.azurewebsites.net/)

The process will guide you through creating an account. 

The game is now in **OPEN BETA**, meaning I've still got a long way to go, but the game is playable enough where I can start opening it up to users. [How to create an account](docs/creating_a_new_account.md)

The **STAGING Environment** is [here](exodestiny-stage-guepbuc0bmcudnbh.westus2-01.azurewebsites.net). This should mirror the production site but be one step ahead so that I can test things. You log into both tenants in the same way. 

# What is left to do, and when to do it:
The `dev` branch has the more current workload. Unless I get too busy with other things, I'll pull those changes into `main` every month (depending on how much time I have to spend on it). 


## **BETA - RELEASE** - Should be playable, but will still have a lot to go.

[What's been completed recently is in the Pull Requests](https://github.com/BillmanH/exoplanets/pulls?q=is%3Apr+is%3Aclosed+base%3Amain)

## May
* Launching ships - being able to launch ships into space.
  * The full path of being able to take a ship from inventory, fill it with fuel, map a trajectory and create a `job` with a resoultion date will finish that component. 
* Tracking space voyages and destinations.
  * You'll need to see the voyage in the `system` view. I'm hoping for a triange, with a trajectory arc that shows where the spaceship is. 
* Being able to view worlds that have been 'observed'.
  * Currently the only ship is the probe, when it reaches it's destiny it should be able to `.scan_body()` on that planet to reveil what kinds of resources the planet has. 

## June
* The colony ship
  * takes a cargo of one `pop` and launches it towards a destination.
  * this will create a new faction, where the pop `isIn` that faction. 
  * once it gets there the pop will starve because there is no food.



Exoplanets is a real-time, multiplayer, online game where you manage a civilization and its people. Starting at the moment where your technology makes it possible to launch an individual into outer space, you must make choices that guide your people on their journey to the stars. This game was built at a very slow pace over the course of several years.

At the start of the game, your civilization is growing rapidly. It is also consuming organic resources at a rate faster than the planet can restore. In time, the resources will diminish, and your people will starve and die. Your goal is to build infrastructure and technology to stabilize this.

![Alt text](/docs/img/cityview.png?raw=true "local view")

The game is a simulation platform first, with some interaction that influences the running simulation. Your civilization is growing, consuming resources, and fighting wars without your interaction. Your goal is to nudge them into a sustainable future. 

![Alt text](/docs/img/solar_system.png?raw=true "solar system")

The game is about simulation, systems thinking, and collective progress. The only adversary is the erosion of your own cosmic destiny. 

![Alt text](/docs/img/PopGrowthSystem.png?raw=true "pop growth system")


## Making your own game
I built this game so that I could clone it and create different versions. You should be able to clone the repo and run it on your own machine or in the cloud of your choice. Some assembly is required as this application uses a lot of tools. I'm working to keep the costs of the game down to ~$20 a month. 

![Alt text](/docs/img/Infra.png?raw=true "Architecture")
    

Of course, you can also just clone it on your local machine and run it for free. Feel free to create an issue, and I'll address them as I'm able. 

### Docs:
| Document |
| ----------- |
| [Building the Azure infrastructure](docs/readme.md) | 
| [Building the Local (dev) infrastructure](docs/local_setup.md) | 
| [Standards and Conventions](docs/Standards%20and%20Conventions.md) | 

| The graph has lots of core elements that need to be set up for the game to function. All of that is in the notebooks. |
| The `docs` and `infra` folders contain everything else that you would need to know |


# Contributing
I designed this game as a good project for a junior developer. This might be a bit much if you've never done any programming at all, but if you know basic data transformations and logic, then this game should be a good project for you. [Feel free to reach out](mailto:william.jeffrey.harding@gmail.com) or just fork the `dev` branch and make a PR. I'll test everything in `dev` before pulling it into the website, so any PRs should go to the `dev` or new `feature` branch.  

Pretty early in the design right now as I have a lot to do before I have a legit game. Also, feel free to make suggestions in the `issues`. I'm so early in this concept that there are lots of design decisions remaining. 

