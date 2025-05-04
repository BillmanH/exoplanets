# All Celestial objects. Planets, moons, stars, including the base Body class.

from ..functions import maths
from ..functions import language
from ..objects import resource

class System:
    def __init__(self,conf=None):
        self.objid = maths.uuid(n=13)
        self.name = language.make_word(maths.rnd(2, 1))
        self.type = "ordered"
        self.label = "system"
        self.isHomeSystem = True
        self.glat = maths.np.round(maths.np.random.normal(0,30),3)
        self.glon = maths.np.round(maths.np.random.normal(0,30),3)
        self.gelat = maths.np.round(maths.np.random.normal(0,7),3)

    def get_data(self):
        system = {
            "objid": self.objid,
            "name": self.name,
            "label": self.label,
            "class": self.type,
            "isHomeSystem": self.isHomeSystem,
            "glat": self.glat,
            "glon": self.glon,
            "gelat": self.gelat
        }
        return system

    def __repr__(self) -> str:
        return f"<{self.label}: {self.type}; {self.objid}; {self.name}>"

class Body:
    def __init__(self,conf=None):
        self.config = conf

    def set_defaults(self):
        self.objid = maths.uuid(n=13)
        self.type = "celestial body"
        self.label = "body"
        self.name = "unnamed"
        self.atmosphere = None
        self.resources = []
        self.pop_cap = 100 # Natural population cap

    def make_name(self, n1, n2):
        self.name = language.make_word(maths.rnd(n1, n2))

    def get_fundimentals(self):
        fundamental_data = {
            "name": self.name,
            "class": self.type,
            "objid": self.objid,
            "label": self.label,
            "pop_cap": self.pop_cap,
        }
        if self.atmosphere:
            fundamental_data["atmosphere"] = self.atmosphere
        return fundamental_data
    
    def choose_type(self,config):
        # Choose a object type from based on the probabilities in the planet config
        choice = maths.np.random.choice(
                list(config.keys()),
                p=[
                    float(config[t]["prob"]) / sum([config[t]["prob"] for t in config.keys()])
                    for t in config.keys()
                ]
            )
        return config[choice]
    
    def get_orbits_edge(self):
        edge = {
            "node1": self.objid,
            "node2": self.orbiting.objid,
            "label": "orbits",
            "orbit_distance": self.orbitsDistance,
        }
        return edge
    
    def get_in_system_edge(self):
        edge = {
            "node1": self.objid,
            "node2": self.system.objid,
            "label": "isIn",
        }
        return edge        
    
    def scan_body(self):
        if 'resources' in self.config.keys():
            if len(self.resources)>0:
                pass
            else:
                for n in self.config['resources'].keys():
                    self.resources.append(resource.Resource(self.config['resources'][n],self))
            # TODO: add atmosphere from the config. 
        if self.config['has_atmosphere']:
            self.atmosphere = maths.rnd_dist(self.config['atmosphere'])


    def __repr__(self) -> str:
        return f"<{self.label}: {self.type}; {self.objid}; {self.name}>"



class Star(Body):
    def __init__(self,conf, starSystem):
        self.system = starSystem
        self.config = conf
        self.set_defaults()
        self.make_name(1, 1)
        self.label = "star"
        self.type = conf["class"]
        self.radius = conf["radius"]

    def get_data(self):
        fund = self.get_fundimentals()
        fund['radius'] = self.radius
        return fund


class Planet(Body):
    """
    Randomly generates a planet
    Manipulate the config to force specific outcomes.
    Limit the conf dict to specify the type of planet.
    """
    def __init__(self,conf,orbiting):
        self.set_defaults()
        self.make_name(2, 1)
        self.label = "planet"
        t = self.choose_type(conf)
        self.config = t
        self.type = t['name']
        self.radius = maths.rnd(t["radius_mean"], t["radius_std"], min_val=0,type='float')
        self.mass = maths.rnd(t["mass_mean"], t["mass_std"],min_val=0,type='float')
        self.orbitsDistance = maths.np.round(maths.np.random.uniform(t["distance_min"], t["distance_max"]),3)
        self.orbiting = orbiting
        self.isSupportsLife = False
        self.isPopulated = False
        self.isSurveyed = False
        self.system = orbiting.system

    def get_data(self):
        fund = self.get_fundimentals()
        fund["radius"] = self.radius
        fund["mass"] = self.mass
        fund["orbitsDistance"] = self.orbitsDistance
        fund["orbitsId"] = self.orbiting.objid
        fund["orbitsName"] = self.orbiting.name
        fund["isSupportsLife"] = self.isSupportsLife
        fund["isPopulated"] = self.isPopulated
        if hasattr(self, 'isHomeworld'):
            fund["isHomeworld"] = self.isHomeworld
        return fund


class Moon(Body):
    """
    Moon takes a list of planets as an input. 
    To specify the planet, pass a list of size 1.
    """
    def __init__(self,conf,planets):
        self.set_defaults()
        self.make_name(2, 1)
        self.label = "moon"
        t = self.choose_type(conf)
        self.config = t
        self.type = t['name']
        self.orbiting = maths.np.random.choice(planets)
        self.orbitsId = self.orbiting.objid
        self.orbitsDistance = maths.rnd(0.005,0.1,type='float', min_val=.0001)  
        self.mass = abs(maths.np.random.normal(t["mass_mean"], t["mass_std"]))
        self.radius = (
            abs(maths.np.random.normal(t["radius_mean"], t["radius_std"]))
            * self.orbiting.radius
        )
        self.orbitsName = self.orbiting.name
        self.isSupportsLife = False
        self.isPopulated = False
        self.system = self.orbiting.orbiting.system

    def get_data(self):
        fund = self.get_fundimentals()
        fund["orbitsId"] = self.orbitsId
        fund["orbitsName"] = self.orbitsName
        fund["orbitsDistance"] = self.orbitsDistance + self.orbiting.radius
        fund["mass"] = self.mass
        fund["radius"] = self.radius
        fund["isSupportsLife"] = self.isSupportsLife
        fund["isPopulated"] = self.isPopulated
        return fund

class Asteroid(Body):
    def __init__(self,conf):
        self.set_defaults()
        self.make_name(2, 1)
        self.label = "asteroid"
        t = self.choose_type(conf)
        self.config = t
        self.type = t['name']
        self.description = t['description']
        self.orbiting = None
        self.orbitsDistance = maths.np.round(maths.np.random.uniform(t["distance_min"], t["distance_max"]),3)
        self.mass = abs(maths.np.random.normal(t["mass_mean"], t["mass_std"]))
        self.radius = abs(maths.np.random.normal(t["radius_mean"], t["radius_std"]))
        self.isSupportsLife = False
        self.isPopulated = False
        self.system = None

    def get_data(self):
        fund = self.get_fundimentals()
        fund["orbitsDistance"] = self.orbitsDistance
        fund["mass"] = self.mass
        fund["radius"] = self.radius
        fund["isPopulated"] = self.isPopulated
        fund["description"] = self.description
        return fund


def discover_new_body(c, message, configs,logging):
    #TODO: All new discoveries are asteroids for now. Make some variety. 
    conf = configs.get_configurations()
    if message['object'] in ["star", "planet"]:
        new_body = Asteroid(conf['asteroid_config'])
    if message['object'] == "moon":
        new_body = Asteroid(conf['asteroid_config'])
    else:
        new_body = Asteroid(conf['asteroid_config'])
    logging.info(f"EXOADMIN: Creating {message['object']}: {new_body}")
    nodes = [new_body.get_data()]
    edges = [{'node1': new_body.get_data()['objid'],
                'node2':message['system']['objid'],
                'label':'isIn'}]
    data = {'nodes':nodes,'edges':edges}
    c.upload_data(message['system']['userguid'],data)
    logging.info(f"EXOADMIN: Uploading data: {data}")


