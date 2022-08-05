# Doc taken from
# notebooks/People/Generating Population

import pandas as pd
from numpy import interp, linspace, random, round
from sklearn.cluster import KMeans

from . import language
from . import maths

# Setup Params:
n_steps = 6  # max factions
meta = ["uuid", "name", "label", "isIdle"]
starting_attributes = ["conformity", "literacy", "aggression", "constitution"]


def compare_values(values, gr1, gr2):
    distance = []
    for v in values:
        distance.append(abs(gr1.get(v, 0) - gr2.get(v, 0)))
    return sum(distance) / len(distance)


def get_faction_loyalty(x, pops, factions):
    g1 = pops.loc[x].to_dict()
    f2 = factions.loc[int(g1["faction_no"])].to_dict()
    return compare_values(starting_attributes, g1, f2)


def build_species(data):
    # TODO: Replace attributes with something more meaninful, like what kinds of resources they consume
    species = {}
    # pulling out the parts of the genesis-form that are specific to species
    [
        species.update({attr: data[attr]})
        for attr in ["conformity", "literacy", "aggression", "constitution",]
    ]
    species["objid"] = maths.uuid(n=13)
    species["label"] = "species"
    species["name"] = language.make_dist_word(random.choice([1, 2]))
    return species


def vary_pops(species):
    # population attributes vary in accordance with the species['conformity']
    pop_std = 0.2 * (1 - float(species["conformity"]))
    pop = {}
    for k in list(species.keys()):
        if k in meta:
            continue
        pop[k] = abs(round(random.normal(float(species[k]), pop_std), 3))
    pop["objid"] = maths.uuid(n=13)
    pop["label"] = "pop"
    pop['isIdle'] = "True"
    pop['health'] = .5
    return pop


def get_pop_name(df, faction_no):
    # the pop name is the faction name plus an extra syllable.
    name = (
        df[df["faction_no"] == faction_no]["name"].values[0]
        + " "
        + language.make_dist_word(random.choice([1, 2]))
    )
    return name


def get_n_factions(n_steps, conf):
    x = interp((1 - conf), linspace(0, 1, num=n_steps), [i for i in range(n_steps)])
    return int(round(x))


def make_factions(kmeans):
    factions = [
        {
            "name": language.make_dist_word(2),
            "objid": maths.uuid(n=13),
            "label": "faction",
            "faction_no": i,
        }
        for i in range(kmeans.n_clusters)
    ]
    return factions


def get_faction_objid(df, faction_no):
    objid = df[df["faction_no"] == faction_no]["objid"].values[0]
    return objid


def build_people(data):
    # Get the Species
    species = build_species(data)
    # Build the populations (note that pops is a DataFrame)
    pops = pd.DataFrame([vary_pops(species) for i in range(int(data["starting_pop"]))])
    # Build the factions
    n_factions = get_n_factions(n_steps, float(data["conformity"]))
    kmeans = KMeans(n_clusters=n_factions).fit(
        pops[[c for c in pops.columns if c not in meta]]
    )
    pops["faction_no"] = kmeans.labels_
    factions = make_factions(kmeans)
    factions_df = pd.DataFrame(factions)
    pops["name"] = pops["faction_no"].apply(lambda x: get_pop_name(factions_df, x))
    pops["isInFaction"] = pops["faction_no"].apply(
        lambda x: get_faction_objid(factions_df, x)
    )
    # sum up the nodes and edges for return
    isOfSpecies = [
        {"node1": p["objid"], "node2": species["objid"], "label": "isOfSpecies"}
        for p in pops.to_dict("records")
    ]
    isInFaction = [
        {"node1": p["objid"], "node2": p["isInFaction"], "label": "isInFaction"}
        for p in pops.to_dict("records")
    ]
    pops["industry"] = (pops["aggression"] + pops["constitution"]) / 2
    pops["wealth"] = (pops["literacy"] + pops["industry"]) / 2
    pops["faction_loyalty"] = [
        (1 - get_faction_loyalty(i, pops, factions_df)) for i in pops.index
    ]

    nodes = [species] + pops.to_dict("records") + factions
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
            edge = {'label':'desires',
                    'node1':p['objid'],
                    'node2':o['objid'],
                    'desire':o['type'],
                    'weight':get_desire(p[o['leadingAttribute']])}
            edges.append(edge)
    return edges

def validate_pop_action(p,a):
    # will validate that a given pop (p) meets the requirement needed to take an action (a)
    if "requires_attr" in a.keys():
        n=2  # requirements are lists of 2 (propperty and value)
        r = a["requires_attr"].split(";")
        r=[r[i:i + n] for i in range(0, len(r), n)]
        for ri in r:
            if ri[0] not in p.keys():
                return False # pop doesn't have the reqired propperty
            if float(ri[1]) > 0:
                if p[ri[0]] < float(ri[1]):
                    return False # pop doesn't have the sufficient level of propperty
            if float(ri[1]) < 0:
                if p[ri[0]] > (float(ri[1])*-1):
                    return False # pop has too high level of propperty
            
    # upon failing to in-validate, return true
    return True

def get_pop_actions(pops, actions):
    edges = []
    for p in pops:
        for a in actions:
            if validate_pop_action(p,a):
                edge = {'label':'hasAction',
                        'node1':p['objid'],
                        'node2':a['objid'],
                        'desire':a['type']}
                edges.append(edge)
    return edges

