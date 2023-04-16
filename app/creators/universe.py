
from numpy import random as r


from ..functions import maths
from ..functions import language
from ..functions import configurations

from ..objects import celestials

conf = configurations.get_configurations()


def make_homeworld(orbiting, data):
    terrestrial_config = {"terrestrial": conf["planet_config"]["terrestrial"]}
    p = celestials.Planet(conf=terrestrial_config, orbiting=orbiting)
    if "planet_name" in data.keys():
        p.name = data["planet_name"]
    p.isSupportsLife = True
    p.isPopulated = True
    p.isHomeworld = True
    p.scan_body()
    return p


def build_homeSystem(data, username):
    starSystem = celestials.System(data)
    star = celestials.Star(conf["star_config"], starSystem)
    planets = [
        celestials.Planet(conf=conf["planet_config"], orbiting = star)
        for p in range(int(data["num_planets"]) - 1)
    ]
    home_planet = make_homeworld(star, data)
    planets.append(home_planet)
    moons = [
            celestials.Moon(conf['moon_config'], planets) for p in range(int(data["num_moons"]))
        ]
    all_entities = [starSystem] + [star] + moons + planets + [home_planet] + home_planet.resources
    all_nodes = [b.get_data() for b in all_entities] + [data]  # Adding the userform as a freebe

    orbiting_bodies = [home_planet] + planets + moons
    orbiting_edges = [i.get_orbits_edge() for i in orbiting_bodies]

    system_bodies = orbiting_bodies + [star]
    system_edges = [
        {"node1": i.objid, "node2": starSystem.objid, "label": "isInSystem",}
        for i in system_bodies
    ]

    resource_edges = [i.get_location_edge() for i in home_planet.resources]
    formEdge = {
        "node1": starSystem.objid,
        "node2": data["objid"],
        "label": "created_from_form",
    }
    accountEdge = {
        "node1": data["accountid"],
        "node2": data["objid"],
        "label": "submitted",
    }
    edges = orbiting_edges + system_edges + resource_edges + [formEdge] + [accountEdge]

    graph_data = {'nodes':all_nodes, 'edges':edges}
    return graph_data

