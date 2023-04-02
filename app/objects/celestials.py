# All Celestial objects. Planets, moons, stars, including the base Body class.
from ..functions import maths
from ..functions import language
from ..objects import resource

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
            self.resources.append(resource.Resource(pdata[self.type]['resources'][n]))

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
        fund['radius'] = self.radius
        fund['class'] = self.type
        return fund


class Planet(Body):
    def build_attr(self, t, orbiting):
        self.make_name(2, 1)
        self.label = "planet"
        self.type = t
        self.radius = maths.rnd(pdata[t]["radius_mean"], pdata[t]["radius_std"], min_val=0,type='float')
        self.mass = maths.rnd(pdata[t]["mass_mean"], pdata[t]["mass_std"],min_val=0,type='float')
        self.orbitsDistance = maths.np.round(maths.np.random.uniform(pdata[t]["distance_min"], pdata[t]["distance_max"]),3)
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
        self.orbitsDistance = maths.rnd(0.005,0.1,type='float')  
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
        fund["orbitsDistance"] = self.orbitsDistance + self.orbiting['radius']
        fund["mass"] = self.mass
        fund["radius"] = self.radius
        fund["isSupportsLife"] = self.isSupportsLife
        fund["isPopulated"] = self.isPopulated
        fund["class"] = self.type
        return fund
