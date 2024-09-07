from ..functions import maths
from ..functions import language

from ..objects import species
from ..objects import baseobjects

import yaml 

class Pop(species.Creature):
    def __init__(self, species):
        self.child_youth_mod = .6
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
        if 'objid' in species.config['defaults']:
            self.objid = maths.uuid()
            self.childOf = {"node1": self.objid, "node2": species.config['defaults']['objid'], "label": "childOf"}
        self.label = "pop"
        self.type = "pop"
        self.isIdle = True
        self.health = species.config['defaults']['health']
        self.species = species
        self.isOfSpecies = {
            "node1": self.objid,
            "node2": species.objid,
            "label": "isOf",
        }
        self.faction = None
        self.isInEdge = self.get_isInFaction()
        self.industry = (self.aggression + self.constitution) / 2
        self.wealth = (self.literacy + self.industry) / 2
        self.factionLoyalty = abs(
            round(maths.np.random.normal(float(self.conformity), 0.2 * (1 - float(self.conformity))), 3)
        )

    def get_isInFaction(self):
        try:
            edge = {
                "node1": self.objid,
                "node2": self.isIn,
                "label": "isIn",
            }
        except:
            edge = {
                "node1": self.objid,
                "node2": 'None',
                "label": "isIn",
            }
        return edge

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
        fund["isIn"] = self.faction.objid if hasattr(self.faction, 'objid') else None
        fund["industry"] = self.industry
        fund["wealth"] = self.wealth
        fund["factionLoyalty"] = self.factionLoyalty
        fund["isIdle"] = self.isIdle
        if 'uesrguid' in self.species.config.keys():
            fund["uesrguid"] = self.species.config['uesrguid']
        return fund

class Faction(baseobjects.Baseobject):
    def __init__(self, i):
        super().__init__()
        if type(i)==dict:
            self.name = i['name']
            self.objid = i['objid']
            self.label = "faction"
            self.faction_no = None
            self.pops = []
            self.lat = i['lat']
            self.long = i['long']
            self.wealth = i.get('wealth', 0)
            self.infrastructure = i.get('infrastructure', 0)
        else:
            self.name = self.make_name(2, 2)
            self.label = "faction"
            self.faction_no = i
            self.pops = []
            self.lat = 0
            self.long = 0
            self.wealth = 2 # default wealth.
            self.infrastructure = 0


    def get_data(self):
        fund = self.get_fundimentals()
        fund['lat'] = self.lat
        fund['long'] = self.long
        fund['wealth'] = self.wealth
        fund['infrastructure'] = self.infrastructure
        return fund

    def assign_pop_to_faction(self, pop):
        pop.isIn = self.objid
        pop.faction = self
        self.pops.append(pop)

   
    def get_pop_edges(self, faction_edges):
        # takes a list and adds to it, so that it can easily run over many factions. 
        [faction_edges.append({"node1": pop.objid, "node2": self.objid, "label": "isIn"}) for pop in self.pops]
        return faction_edges


class Global_Pop_Manager():
    """
    See `Population Growth.ipynb` for info on how the population manager works. 
        It's a controller for populations and species. 
    """
    def __init__(self,params,c) -> None:
        self.params = params
        self.c = c
        self.data = None
        # used in creating new populations, which require a species. 
        self.species_dict = {}
        

    def get_pop_health(self):
        pop_health_requirement = self.params['pop_health_requirement']
        healthy_pops_query = f"""
        g.V().has('label','pop')
            .has('health',gt({pop_health_requirement})).as('pop')
            .local(
                union(
                    out('inhabits').as('location'),
                    out('isOf').as('species'),
                    out('isIn').as('faction')
                    )
                    .fold()).as('location','species','faction')
                .path()
                .by(unfold().valueMap().fold())
        """
        self.c.run_query(healthy_pops_query)
        self.data = self.c.reduce_res(self.c.res)


    def population_growth_event(self,parent,location,child):
        node = {
            'objid':maths.uuid(),
            'name':'population growth',
            'label':'event',
            'text': f"The population ({parent['name']}) inhabiting {location['name']} has grown to produce the population: {child.name}.",
            'visibleTo':parent['uesrguid'],
            'time':self.params['currentTime'],
            'uesrguid':'event'
        }
        return node


