import yaml
from numpy import random as r

from . import maths
from . import language
from . import account

pdata = yaml.safe_load(open('notebooks/planets/planet.yaml'))["planet_types"]
mdata = yaml.safe_load(open('notebooks/planets/moon.yaml'))["moon_types"]
sdata = yaml.safe_load(open('notebooks/planets/star.yaml'))

class Body:
    def __init__(self):
        self.objid = maths.uuid(n=13)
        self.type = "celestial body"
        self.label = "body"
        self.name = "unnamed"
    def make_name(self,n1,n2):
        return language.make_word(maths.rnd(n1, n2))
    def get_fundimentals(self):
        return {
            "name":self.name,
            "class":self.type,
            "objid":self.objid,
            "label":self.label
        }
    def __repr__(self) -> str:
        return f"<{self.label}: {self.type}; {self.objid}; {self.name}>"


class Star(Body):
    def build_attr(self,sdata):
        self.name = self.make_name(1,1)
        self.label = "star"
        self.type = sdata["class"]
        self.radius = sdata["radius"]

    def get_data(self):
        fund = self.get_fundimentals()
        fund["radius"] = self.radius
        return fund
    
class Planet(Body):
    def build_attr(self,t,orbiting):
        self.name = self.make_name(2,1)
        self.label = "planet"
        self.type = t
        self.radius = abs(r.normal(pdata[t]["radius_mean"], pdata[t]["radius_std"]))
        self.mass = abs(r.normal(pdata[t]["mass_mean"], pdata[t]["mass_std"]))
        self.orbitsDistance = maths.rnd(pdata[t]["distance_min"], pdata[t]["distance_max"])
        self.orbitsId = orbiting["objid"]
        self.orbitsName = orbiting["name"]
        self.isSupportsLife = False
        self.isPopulated = False

    def get_data(self):
        fund = self.get_fundimentals()
        fund["radius"] = self.radius
        fund["mass"] = self.mass
        fund["orbitsDistance"] = self.orbitsDistance
        fund["orbitsId"] = self.orbitsId
        fund["orbitsName"] = self.orbitsName
        fund["isSupportsLife"] = self.isSupportsLife
        fund["isPopulated"] = self.isPopulated
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
    planet = make_planet("terrestrial", orbiting)
    planet["name"] = data["planet_name"]
    planet["isSupportsLife"] = True
    planet["isPopulated"] = True
    planet["isHomeworld"] = True
    return planet

def make_moon(t, planets):
    moon = {"class": t, "name": language.make_word(maths.rnd(2, 1))}
    moon["label"] = "moon"
    moon["objid"] = maths.uuid(n=13)
    moon["mass"] = abs(r.normal(mdata[t]["mass_mean"], mdata[t]["mass_std"]))
    moon["radius"] = abs(r.normal(mdata[t]["radius_mean"], mdata[t]["radius_std"]))
    orbiting = r.choice(planets)
    moon["orbitsId"] = orbiting["objid"]
    moon["orbitsDistance"] = .005
    moon["orbitsName"] = orbiting["name"]
    moon["isSupportsLife"] = False
    moon["isPopulated"] = False
    return moon


def build_homeSystem(data, username):
    user = account.create_account(username)

    systemid = maths.uuid(n=13)
    system = {
        "name": language.make_word(maths.rnd(2, 1)),
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
        "node2": user['objid'],
        "label": "belongsToUser",
    }
    edges = system_edges + orbits + [accountEdge]
    return nodes, edges

