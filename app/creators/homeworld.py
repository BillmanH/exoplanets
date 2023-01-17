# Doc taken from
# notebooks/People/Generating Population

import pandas as pd
from numpy import interp, linspace, random
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from . import baseobjects

# Setup Params:
n_steps = 6  # max factions
meta = ["uuid", "name", "label", "isIdle"]
starting_attributes = ["conformity", "literacy", "aggression", "constitution"]


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
        self.consumes = "organic"
        self.effuses = "organic waste"
        self.viral_resilience = 0.7
        self.habitat_resilience = 0.2
        self.pop_std = 0.2 * (1 - float(self.conformity))
        self.name = self.make_name(1, 2)

    def get_data(self):
        fund = self.get_fundimentals()
        fund["consumes"] = self.consumes
        fund["effuses"] = self.effuses
        fund["viral_resilience"] = self.viral_resilience
        fund["habitat_resilience"] = self.habitat_resilience
        return fund


class Pop(Creature):
    def __init__(self, species):
        super().__init__()
        self.conformity = abs(
            round(random.normal(float(species.conformity), species.pop_std), 3)
        )
        self.literacy = abs(
            round(random.normal(float(species.literacy), species.pop_std), 3)
        )
        self.aggression = abs(
            round(random.normal(float(species.aggression), species.pop_std), 3)
        )
        self.constitution = abs(
            round(random.normal(float(species.constitution), species.pop_std), 3)
        )
        self.label = "pop"
        self.type = "pop"
        self.isIdle = "True"
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
            round(random.normal(float(self.conformity), 0.2 * (1 - float(self.conformity))), 3)
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

    def get_data(self):
        fund = self.get_fundimentals()
        return fund

    def assign_pop_to_faction(self, pop):
        pop.isInFaction = self.objid
        self.pops.append(pop.objid)

        

    def get_faction_pop_edge(self):
        return [
            {"node1": pop, "node2": self.objid, "label": "isInFaction"}
            for pop in self.pops
        ]



def compare_values(values, gr1, gr2):
    distance = []
    for v in values:
        distance.append(abs(gr1.get(v, 0) - gr2.get(v, 0)))
    return sum(distance) / len(distance)


def get_faction_loyalty(x, pops, factions):
    g1 = pops.loc[x].to_dict()
    f2 = factions.loc[int(g1["faction_no"])].to_dict()
    return compare_values(starting_attributes, g1, f2)


def get_n_factions(n_steps, conf):
    x = interp((1 - conf), linspace(0, 1, num=n_steps), [i for i in range(n_steps)])
    return int(round(x))


def get_faction_objid(df, faction_no):
    objid = df[df["faction_no"] == faction_no]["objid"].values[0]
    return objid


def build_people(data):
    # Get the Species
    species = Species()
    species.build_attr(data)

    # Build the populations (note that pops is a DataFrame)
    pops = [Pop(species) for i in range(int(data["starting_pop"]))]

    # Build the factions based on Kmeans Clustering
    pops_df = pd.DataFrame([p.get_data() for p in pops])
    n_factions = get_n_factions(n_steps, float(data["conformity"]))
    kmeans = KMeans(n_clusters=n_factions).fit(
        pops_df[[c for c in pops_df.columns if c in starting_attributes]]
    )

    factions = [Faction(i) for i in range(kmeans.n_clusters)]

    # Assign the pop to that faction number, not yet matched to an ID.
    for i, n in enumerate(kmeans.labels_):
        pops[i].set_faction(n)

    # Set the name of the population to comply with the faction it is in.
    for p in pops:
        faction = [i for i in factions if i.faction_no == p.factionNo][0]
        if p.name == '':
            p.name = p.make_name(2,2)
        p.set_pop_name(faction)
        faction.assign_pop_to_faction(p)

    # using PCA to set populations on map:
    for f in factions:
        faction_stats = pd.DataFrame([
            [
                [{'faction':f.name,d:p.get_data()[d]} 
                    for d in list(p.get_data().keys()) if d in starting_attributes
                    ] 
                        for p in pops if p.objid in f.pops] 
                            for f in factions
                        ])
                            
        # PCA Part
        pca = PCA(n_components=2)
        X_r = pca.fit(faction_stats).transform(faction_stats)
        f.pca_explained_variance_ratio = pca.explained_variance_ratio_
        f.pca_X_r = X_r        


    # sum up the nodes and edges for return
    isOfSpecies = [p.isOfSpecies for p in pops]
    isInFaction = []
    for f in factions:
        isInFaction+= f.get_faction_pop_edge()
        

    nodes = [species.get_data()] + [pop.get_data() for pop in pops] + [f.get_data() for f in factions]
    edges = isInFaction + isOfSpecies
    
    return nodes, edges


def attach_people_to_world(homeworld_nodes, homeworld):
    # in the beginning there should only be one homeworld
    pops = [p for p in homeworld_nodes if p.get("label") == "pop"]
    edges = [
        {"node1": p["objid"], "node2": homeworld["objid"], "label": "enhabits"}
        for p in pops
    ]
    return edges


def get_desire(x):
    # Marginal return on base attribute
    n = 2
    return round(((float(x) + 1) ** (1 - n) - 1) / (1 - n), 3)


def get_pop_desires(pops, objectives):
    edges = []
    for p in pops:
        for o in objectives:
            edge = {
                "label": "desires",
                "node1": p["objid"],
                "node2": o["objid"],
                "desire": o["type"],
                "weight": get_desire(p[o["leadingAttribute"]]),
            }
            edges.append(edge)
    return edges


def validate_pop_action(p, a):
    # will validate that a given pop (p) meets the requirement needed to take an action (a)
    if "requires_attr" in a.keys():
        n = 2  # requirements are lists of 2 (propperty and value)
        r = a["requires_attr"].split(";")
        r = [r[i : i + n] for i in range(0, len(r), n)]
        for ri in r:
            if ri[0] not in p.keys():
                return False  # pop doesn't have the reqired propperty
            if float(ri[1]) > 0:
                if p[ri[0]] < float(ri[1]):
                    return False  # pop doesn't have the sufficient level of propperty
            if float(ri[1]) < 0:
                if p[ri[0]] > (float(ri[1]) * -1):
                    return False  # pop has too high level of propperty

    # upon failing to in-validate, return true
    return True


def get_pop_actions(pops, actions):
    edges = []
    for p in pops:
        for a in actions:
            if validate_pop_action(p, a):
                edge = {
                    "label": "hasAction",
                    "node1": p["objid"],
                    "node2": a["objid"],
                    "desire": a["type"],
                }
                edges.append(edge)
    return edges


# An example `data` set:
# data = {
#     "planet_name": "Earth",
#     "num_planets": "6",
#     "num_moons": "24",
#     "home_has_moons": "on",
#     "starting_pop": "7",
#     "conformity": "0.3",
#     "literacy": "0.7",
#     "aggression": "0.5",
#     "constitution": "0.5",
#     "name": "form",
#     "objid": "4864559553238",
#     "username": "Billmanh",
#     "objtype": "form",
#     "id": "4864559553238",
# }

