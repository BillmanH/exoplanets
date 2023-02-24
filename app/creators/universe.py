import yaml
from numpy import random as r
import os

from . import maths
from . import language


pdata = yaml.safe_load(open(os.path.join(os.getenv("abspath"),"app/configurations/planet.yaml")))["planet_types"]
mdata = yaml.safe_load(open(os.path.join(os.getenv("abspath"),"app/configurations/moon.yaml")))["moon_types"]
sdata = yaml.safe_load(open(os.path.join(os.getenv("abspath"),"app/configurations/star.yaml")))

class Resource:
    def __init__(self, conf):
        self.objid = maths.uuid(n=13)
        self.label = "resource"
        self.conf = conf
        self.name = conf["name"]
        self.description = conf["description"]
        self.volume = maths.rnd(conf["mean"],conf["std"], min_val=0)
        if conf.get('replenish_rate'):
            self.replenish_rate = conf['replenish_rate']
    def get_data(self):
        return {
            "name": self.name,
            "objid": self.objid,
            "label": self.label,
            "volume": self.volume,
            "description": self.description
        }
    def __repr__(self) -> str:
        return f"<{self.label}: {self.objid}; {self.name}>"  

class Body:
    def __init__(self):
        self.objid = maths.uuid(n=13)
        self.type = "celestial body"
        self.label = "body"
        self.name = "unnamed"
        self.resources = []

    def make_name(self, n1, n2):
        self.name = language.make_word(maths.rnd(n1, n2))

    def get_fundimentals(self):
        return {
            "name": self.name,
            "class": self.type,
            "objid": self.objid,
            "label": self.label,
        }
    
    def scan_body(self):
        for n in pdata[self.type]['resources'].keys():
            self.resources.append(Resource(pdata[self.type]['resources'][n]))

    def __repr__(self) -> str:
        return f"<{self.label}: {self.type}; {self.objid}; {self.name}>"


class Star(Body):
    def build_attr(self, sdata):
        self.make_name(1, 1)
        self.label = "star"
        self.type = sdata["class"]
        self.radius = sdata["radius"]

    def get_data(self):
        fund = self.get_fundimentals()
        fund["radius"] = self.radius
        return fund


class Planet(Body):
    def build_attr(self, t, orbiting):
        self.make_name(2, 1)
        self.label = "planet"
        self.type = t
        self.radius = maths.rnd(pdata[t]["radius_mean"], pdata[t]["radius_std"], min_val=0,type='float')
        self.mass = maths.rnd(pdata[t]["mass_mean"], pdata[t]["mass_std"],min_val=0,type='float')
        self.orbitsDistance = maths.rnd(
            pdata[t]["distance_min"], pdata[t]["distance_max"]
        )
        self.orbitsId = orbiting["objid"]
        self.orbitsName = orbiting["name"]
        self.isSupportsLife = False
        self.isPopulated = False
        self.isSurveyed = False


    def get_data(self):
        fund = self.get_fundimentals()
        fund["radius"] = self.radius
        fund["mass"] = self.mass
        fund["orbitsDistance"] = self.orbitsDistance
        fund["orbitsId"] = self.orbitsId
        fund["orbitsName"] = self.orbitsName
        fund["isSupportsLife"] = self.isSupportsLife
        fund["isPopulated"] = self.isPopulated
        fund["type"] = self.type
        return fund


class Moon(Body):
    def build_attr(self, t, planets):
        self.make_name(2, 1)
        self.label = "moon"
        self.type = t
        self.orbiting = r.choice(planets)
        self.orbitsId = self.orbiting["objid"]
        self.distance = 0.005  # TODO: Make dynamic moon distance
        self.mass = abs(r.normal(mdata[t]["mass_mean"], mdata[t]["mass_std"]))
        self.radius = (
            abs(r.normal(mdata[t]["radius_mean"], mdata[t]["radius_std"]))
            * self.orbiting["radius"]
        )
        self.orbitsName = self.orbiting["name"]
        self.isSupportsLife = False
        self.isPopulated = False

    def get_data(self):
        fund = self.get_fundimentals()
        fund["orbitsId"] = self.orbitsId
        fund["orbitsName"] = self.orbitsName
        fund["orbitsDistance"] = self.distance
        fund["mass"] = self.mass
        fund["radius"] = self.radius
        fund["isSupportsLife"] = self.isSupportsLife
        fund["isPopulated"] = self.isPopulated
        fund["class"] = self.type
        return fund


def make_star():
    s = Star()
    s.build_attr(sdata)
    return s.get_data()


def make_planet(t, orbiting):
    p = Planet()
    p.build_attr(t, orbiting)
    return p.get_data()


def make_homeworld(orbiting, data):
    p = Planet()
    p.build_attr("terrestrial", orbiting)
    # p.scan_body()
    planet = p.get_data()
    if "planet_name" in data.keys():
        planet["name"] = data["planet_name"]
    planet["isSupportsLife"] = True
    planet["isPopulated"] = True
    planet["isHomeworld"] = True
    p.scan_body()
    homeworld_nodes = [r.get_data() for r in p.resources] 
    homeworld_edges = [
        {"node1": p.objid, "node2": r.objid, "label": "hasResource"} for r in p.resources
    ]
    return planet, homeworld_nodes, homeworld_edges


def make_moon(t, planets):
    m = Moon()
    m.build_attr(t, planets)
    return m.get_data()


def build_homeSystem(data, username):

    systemid = maths.uuid(n=13)
    system = {
        "name": language.make_word(maths.rnd(2, 1)),
        "label": "system",
        "isHomeSystem":"true",
        "objid": systemid,
    }
    star = make_star()
    planets = [
        make_planet(
            r.choice(list(pdata.keys()), p=[pdata[t]["prob"] for t in pdata.keys()]),
            star,
        )
        for p in range(int(data["num_planets"]) - 1)
    ]
    homeworld, homeworld_nodes,homeworld_edges = make_homeworld(star, data)
    planets.append(homeworld)
    moons = [
        make_moon(
            r.choice(list(mdata.keys()), p=[mdata[t]["prob"] for t in mdata.keys()]),
            planets,
        )
        for p in range(int(data["num_moons"]))
    ]
    nodes = [data] + [system] + [star] + moons + planets + homeworld_nodes
    system_edges = [
        {"node1": p["objid"], "node2": system["objid"], "label": "isInSystem"}
        for p in nodes
        if p["label"] != "system"
    ]
    orbits = [
        {
            "node1": p["objid"],
            "node2": p["orbitsId"],
            "label": "orbits",
            "orbit_distance": p["orbitsDistance"],
        }
        for p in nodes
        if p.get("orbitsId")
    ]

    formEdge = {
        "node1": systemid,
        "node2": data["objid"],
        "label": "created_from_form",
    }
    accountEdge = {
        "node1": data["accountid"],
        "node2": data["objid"],
        "label": "submitted",
    }
    edges = system_edges + orbits + [formEdge] + homeworld_edges + [accountEdge]
    return nodes, edges

