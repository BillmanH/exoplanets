from ..functions import maths

from ..objects import species
from ..objects import baseobjects

class Pop(species.Creature):
    def __init__(self, species):
        super().__init__()
        self.conformity = abs(
            round(maths.np.random.normal(float(species.conformity), species.pop_std), 3)
        )
        self.literacy = abs(
            round(maths.np.random.normal(float(species.literacy), species.pop_std), 3)
        )
        self.aggression = abs(
            round(maths.np.random.normal(float(species.aggression), species.pop_std), 3)
        )
        self.constitution = abs(
            round(maths.np.random.normal(float(species.constitution), species.pop_std), 3)
        )
        self.label = "pop"
        self.type = "pop"
        self.isIdle = "true"
        self.health = 0.5
        self.isOfSpecies = {
            "node1": self.objid,
            "node2": species.objid,
            "label": "isOfSpecies",
        }
        self.factionNo = None
        self.isInFaction = None
        self.industry = (self.aggression + self.constitution) / 2
        self.wealth = (self.literacy + self.industry) / 2
        self.factionLoyalty = abs(
            round(maths.np.random.normal(float(self.conformity), 0.2 * (1 - float(self.conformity))), 3)
        )

    def set_faction(self, n):
        self.factionNo = n

    def set_pop_name(self, faction):
        # the pop name is the faction name plus an extra syllable.
        self.name = f"{faction.name} {self.make_name(1, 2)}"

    def get_data(self):
        fund = self.get_fundimentals()
        fund["conformity"] = self.conformity
        fund["literacy"] = self.literacy
        fund["aggression"] = self.aggression
        fund["constitution"] = self.constitution
        fund["health"] = self.health
        fund["isInFaction"] = self.isInFaction
        fund["industry"] = self.industry
        fund["wealth"] = self.wealth
        fund["factionLoyalty"] = self.factionLoyalty
        fund["isIdle"] = self.isIdle
        return fund

class Faction(baseobjects.Baseobject):
    def __init__(self, i):
        super().__init__()
        self.name = self.make_name(2, 2)
        self.label = "faction"
        self.faction_no = i
        self.pops = []
        self.lat = 0
        self.long = 0

    def get_data(self):
        fund = self.get_fundimentals()
        fund['lat'] = self.lat
        fund['long'] = self.long
        return fund

    def assign_pop_to_faction(self, pop):
        pop.isInFaction = self.objid
        self.pops.append(pop.objid)

    def get_faction_pop_edge(self):
        return [
            {"node1": pop, "node2": self.objid, "label": "isInFaction"}
            for pop in self.pops
        ]
