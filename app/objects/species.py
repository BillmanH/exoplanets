from objects import baseobjects

class Creature(baseobjects.Baseobject):
    def __init__(self):
        super().__init__()
        self.label = "creature"

    def get_fundimentals(self):
        return {"name": self.name, "objid": self.objid, "label": self.label}


class Species(baseobjects.Baseobject):
    def build_attr(self, data):
        self.conformity = data["conformity"]
        self.aggression = data["aggression"]
        self.literacy = data["literacy"]
        self.constitution = data["constitution"]
        self.label = "species"
        self.name = self.make_name(1, 2)
        self.consumes = ["Organic"]
        self.effuses = ["Organic waste","Plastics"]
        self.viral_resilience = 0.7
        self.habitat_resilience = 0.2
        self.pop_std = 0.2 * (1 - float(self.conformity))

    def get_data(self):
        fund = self.get_fundimentals()
        fund["consumes"] = self.consumes
        fund["effuses"] = self.effuses
        fund["viral_resilience"] = self.viral_resilience
        fund["habitat_resilience"] = self.habitat_resilience
        return fund
