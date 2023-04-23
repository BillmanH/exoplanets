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
        self.isIdle = True
        self.health = 0.5
        self.species = species
        self.isOfSpecies = {
            "node1": self.objid,
            "node2": species.objid,
            "label": "isOf",
        }
        self.faction = None
        self.industry = (self.aggression + self.constitution) / 2
        self.wealth = (self.literacy + self.industry) / 2
        self.factionLoyalty = abs(
            round(maths.np.random.normal(float(self.conformity), 0.2 * (1 - float(self.conformity))), 3)
        )

    def set_faction(self, faction):
        self.faction = faction
        faction.assign_pop_to_faction(self)
        self.name = f"{self.faction.name} {self.make_name(1, 2)}"


    def get_data(self):
        fund = self.get_fundimentals()
        fund["conformity"] = self.conformity
        fund["literacy"] = self.literacy
        fund["aggression"] = self.aggression
        fund["constitution"] = self.constitution
        fund["health"] = self.health
        fund["isInFaction"] = self.faction.objid if hasattr(self.faction, 'objid') else None
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
        self.faction_place = [[0,0]]

    def get_data(self):
        fund = self.get_fundimentals()
        fund['lat'] = self.lat
        fund['long'] = self.long
        fund['pop_loactions'] = str(self.faction_place)
        return fund

    def assign_pop_to_faction(self, pop):
        options = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
        pop.isInFaction = self.objid
        self.pops.append(pop)
        pick = options[maths.np.random.choice([0, 1, 2, 3])]
        while True:
            new_pick = options[maths.np.random.choice([0, 1, 2, 3])]
            pick = maths.np.add(pick, new_pick).tolist()
            if pick not in self.faction_place:
                self.faction_place.append(pick)
                break
   
    def get_pop_edges(self, faction_edges):
        # takes a list and adds to it, so that it can easily run over many factions. 
        [faction_edges.append({"node1": pop.objid, "node2": self.objid, "label": "isIn"}) for pop in self.pops]
        return faction_edges
