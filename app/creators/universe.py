
from numpy import random as r


from ..functions import maths
from ..functions import language
from ..functions import configurations

from objects import celestials

conf = configurations.get_configurations()


def make_system():
    systemid = maths.uuid(n=13)
    system = {
        "name": language.make_word(maths.rnd(2, 1)),
        "label": "system",
        "isHomeSystem":"true",
        "objid": systemid,
        "glat": maths.np.round(r.normal(0,20),3),
        "glon": maths.np.round(r.normal(0,20),3),
        "gelat": maths.np.round(r.normal(0,5),3)
    }
    return system


def make_star():
    s = celestials.Star(conf=conf["star_config"])
    s.build_attr(conf['star_config'])
    return s.get_data()


def make_planet(t, orbiting):
    p = celestials.Planet(conf=conf["planet_config"])
    p.build_attr(t, orbiting)
    return p.get_data()


def make_homeworld(orbiting, data):
    p = celestials.Planet(conf=conf["planet_config"])
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
    m = celestials.Moon()
    m.build_attr(t, planets)
    return m.get_data()


def build_homeSystem(data, username):

    system = make_system()
    star = make_star()
    planets = [
        make_planet(
            r.choice(list(conf['planet_config'].keys()), p=[conf['planet_config'][t]["prob"] for t in conf['planet_config'].keys()]),
            star,
        )
        for p in range(int(data["num_planets"]) - 1)
    ]
    homeworld, homeworld_nodes,homeworld_edges = make_homeworld(star, data)
    planets.append(homeworld)
    moons = [
        make_moon(
            r.choice(list(conf['moon_config'].keys()), p=[conf['moon_config'][t]["prob"] for t in conf['moon_config'].keys()]),
            planets,
        )
        for p in range(int(data["num_moons"]))
    ]
    nodes = [data] + [system] + [star] + moons + planets + homeworld_nodes
    system_edges = [
        {"node1": p["objid"], "node2": system["objid"], "label": "isInSystem"}
        for p in nodes
        if p["label"] not in ["system","resource","form"]
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
        "node1": system['objid'],
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

