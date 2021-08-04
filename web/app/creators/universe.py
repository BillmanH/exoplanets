import pickle
import numpy as np
from numpy import random as r
from datetime import datetime

# Depending on where this is run, it could be back one dir. 
try:
    syllables = pickle.load(open("../data/syllables.p", "rb"))
except:
    syllables = pickle.load(open("data/syllables.p", "rb"))


pdata = {
    "dwarf": {
        "count": 6.0,
        "prob": 0.42857142857142855,
        "mass_mean": 0.0011061666666666668,
        "mass_std": 0.0011102811205576121,
        "radius_mean": 0.129,
        "radius_std": 0.04591683787021923,
    },
    "gas": {
        "count": 2.0,
        "prob": 0.14285714285714285,
        "mass_mean": 206.49599999999998,
        "mass_std": 157.45005275324613,
        "radius_mean": 10.055,
        "radius_std": 1.2940054095713813,
    },
    "ice": {
        "count": 2.0,
        "prob": 0.14285714285714285,
        "mass_mean": 15.8415,
        "mass_std": 1.846255805678074,
        "radius_mean": 3.923,
        "radius_std": 0.08202438661763928,
    },
    "terrestrial": {
        "count": 4.0,
        "prob": 0.2857142857142857,
        "mass_mean": 0.49432499999999996,
        "mass_std": 0.4834953524423305,
        "radius_mean": 0.7162,
        "radius_std": 0.3056014070648236,
    },
}

mdata = {
    "moon": {
        "count": 13.0,
        "prob": 0.8125,
        "mass_mean": 0.005513153846153847,
        "mass_std": 0.009417033882333949,
        "radius_mean": 0.17966153846153846,
        "radius_std": 0.12918538706358867,
    },
    "terrestrial": {
        "count": 3.0,
        "prob": 0.1875,
        "mass_mean": 0.011778333333333333,
        "mass_std": 0.0035116816959020257,
        "radius_mean": 0.26786666666666664,
        "radius_std": 0.020873987001369262,
    },
}

#%%
def make_word(n):
    syl = np.random.choice(syllables, n)
    word = "".join(syl)
    return word


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
        return 1
    if t == "gas":
        return 2
    if t == "ice":
        return 3
    if t == "dwarf":
        return 4


def make_planet(t, orbiting):
    planet = {"class": t, "name": make_word(rnd(2, 1))}
    planet["label"] = "planet"
    planet["objid"] = uuid(n=13)
    planet["mass"] = abs(r.normal(pdata[t]["mass_mean"], pdata[t]["mass_std"]))
    planet["radius"] = abs(r.normal(pdata[t]["radius_mean"], pdata[t]["radius_std"]))
    planet["order"] = sort_planets(t)
    planet["orbitsId"] = orbiting["objid"]
    planet["orbitsName"] = orbiting["name"]
    return planet


def make_moon(t, planets):
    moon = {"class": t, "name": make_word(rnd(2, 1))}
    moon["label"] = "moon"
    moon["objid"] = uuid(n=13)
    moon["mass"] = abs(r.normal(mdata[t]["mass_mean"], mdata[t]["mass_std"]))
    moon["radius"] = abs(r.normal(mdata[t]["radius_mean"], mdata[t]["radius_std"]))
    orbiting = r.choice(planets)
    moon["orbitsId"] = orbiting["objid"]
    moon["orbitsName"] = orbiting["name"]
    return moon


def build_homeSystem(data, username):
    accountid = uuid(n=13)
    user = {
        "label": "account",
        "username": "account",
        "created": datetime.now().strftime("%d-%m-%Y-%H-%M-%S"),
        "objid": accountid,
    }
    systemid = uuid(n=13)
    system = {
        "name": make_word(rnd(2, 1)),
        "label": "system",
        "objid": systemid,
    }
    star = {
        "name": make_word(rnd(2, 1)),
        "label": "star",
        #TODO: Create some star classes
        "class": "G",
        "objid": uuid(n=13),
    }
    planets = [
        make_planet(
            r.choice(list(pdata.keys()), p=[pdata[t]["prob"] for t in pdata.keys()]),
            star,
        )
        for p in range(int(data["num_planets"]))
    ]
    moons = [
        make_moon(
            r.choice(list(mdata.keys()), p=[mdata[t]["prob"] for t in mdata.keys()]),
            planets,
        )
        for p in range(int(data["num_moons"]))
    ]
    nodes = [user] + [system] + [star] + moons + planets
    system_edges = [
        {"node1": p["objid"], "node2": system["objid"], "label": "isInSystem"}
        for p in nodes
        if p["label"] != "system"
    ]
    orbits = [
        {"node1": p["objid"], "node2": p["orbitsId"], "label": "orbits"}
        for p in nodes
        if p.get("orbitsId")
    ]
    accountEdge = {
        "node1": systemid,
        "node2": accountid,
        "label": "belongsToUser",
    }
    edges = system_edges + orbits + [accountEdge]
    return nodes, edges