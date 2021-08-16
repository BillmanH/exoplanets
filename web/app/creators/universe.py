import pickle
import numpy as np
import yaml
from numpy import random as r
from datetime import datetime
import os
print(os.listdir())

# Depending on where this is run, it could be back one dir.
try:
    syllables = pickle.load(open("../data/syllables.p", "rb"))
    pdata = yaml.safe_load(open('web/app/creators/specs/planet.yaml'))["planet_types"]
except FileNotFoundError:
    syllables = pickle.load(open("data/syllables.p", "rb"))
    pdata = yaml.safe_load(open('web/app/creators/specs/planet.yaml'))["planet_types"]
    mdata = yaml.safe_load(open('web/app/creators/specs/moon.yaml'))["moon_types"]

# TODO Get some stats on star types
# sdata = {"radius_mean": 109, "radius_std": 1, "class": "G"}
sdata = {"radius": 106, "class": "G"}




#%%
def make_word(n, spaces=True):
    # TODO: Spaces not implemented
    syl = np.random.choice(syllables, n)
    word = "".join(syl)
    return word.capitalize()


def rnd(n, s):
    """
    returns positive int, within normal distribution
    n = mean, s = std
    """
    return int(abs(np.ceil(r.normal(n, s))))


def uuid(n=8):
    return "".join([str(i) for i in np.random.choice(range(10), n)])


def sort_planets(t):
    if t == "terrestrial":
        return rnd(0.39, 1.52)
    if t == "gas":
        return rnd(5.2, 10)
    if t == "ice":
        return rnd(15, 29)
    if t == "dwarf":
        return rnd(30, 50)


def make_star():
    star = sdata
    star["name"] = make_word(rnd(2, 1))
    star["objid"] = uuid(n=13)
    star["label"] = "star"
    return star


def make_planet(t, orbiting):
    planet = {"class": t, "name": make_word(rnd(2, 1))}
    planet["label"] = "planet"
    planet["objid"] = uuid(n=13)
    planet["mass"] = abs(r.normal(pdata[t]["mass_mean"], pdata[t]["mass_std"]))
    planet["radius"] = abs(r.normal(pdata[t]["radius_mean"], pdata[t]["radius_std"]))
    planet["orbitsDistance"] = rnd(pdata[t]["distance_min"], pdata[t]["distance_max"])
    planet["orbitsId"] = orbiting["objid"]
    planet["orbitsName"] = orbiting["name"]
    planet["isSupportsLife"] = False
    planet["isPopulated"] = False
    return planet

def make_homeworld(orbiting, data):
    planet = make_planet("terrestrial", orbiting)
    planet["name"] = data["planet_name"]
    planet["isSupportsLife"] = True
    planet["isPopulated"] = True
    return planet

def make_moon(t, planets):
    moon = {"class": t, "name": make_word(rnd(2, 1))}
    moon["label"] = "moon"
    moon["objid"] = uuid(n=13)
    moon["mass"] = abs(r.normal(mdata[t]["mass_mean"], mdata[t]["mass_std"]))
    moon["radius"] = abs(r.normal(mdata[t]["radius_mean"], mdata[t]["radius_std"]))
    orbiting = r.choice(planets)
    moon["orbitsId"] = orbiting["objid"]
    moon["orbitsDistance"] = .005
    moon["orbitsName"] = orbiting["name"]
    moon["isSupportsLife"] = False
    return moon


def build_homeSystem(data, username):
    accountid = uuid(n=13)
    user = {
        "label": "account",
        "created": datetime.now().strftime("%d-%m-%Y-%H-%M-%S"),
        "objid": accountid,
    }
    systemid = uuid(n=13)
    system = {
        "name": make_word(rnd(2, 1)),
        "label": "system",
        "objid": systemid,
    }
    star = make_star()
    planets = [
        make_planet(
            r.choice(list(pdata.keys()), p=[pdata[t]["prob"] for t in pdata.keys()]),
            star,
        )
        for p in range(int(data["num_planets"])-1)
    ]
    homeworld = make_homeworld(star, data)
    moons = [
        make_moon(
            r.choice(list(mdata.keys()), p=[mdata[t]["prob"] for t in mdata.keys()]),
            planets,
        )
        for p in range(int(data["num_moons"]))
    ]
    nodes = [user] + [system] + [star] + moons + planets + [homeworld]
    system_edges = [
        {"node1": p["objid"], "node2": system["objid"], "label": "isInSystem"}
        for p in nodes
        if p["label"] != "system"
    ]
    orbits = [
        {"node1": p["objid"], "node2": p["orbitsId"], "label": "orbits", "orbit_distance":p["orbitsDistance"]}
        for p in nodes
        if p.get("orbitsId")
    ]
    # TODO: Move account to it's own module
    accountEdge = {
        "node1": systemid,
        "node2": accountid,
        "label": "belongsToUser",
    }
    edges = system_edges + orbits + [accountEdge]
    return nodes, edges
