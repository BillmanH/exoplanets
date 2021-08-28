# Doc taken from
# notebooks/People/Generating Population

import pandas as pd
from numpy import interp, linspace, random, round
from sklearn.cluster import KMeans

from . import language
from . import maths

# Setup Params:
n_steps = 6  # max factions


def build_species(data):
    species = {}
    for attr in [
        "population_conformity",
        "population_literacy",
        "population_aggression",
        "population_constitution",
    ]:
        species[attr] = data[attr]
    species["objid"] = maths.uuid(n=13)
    species["label"] = "species"
    species["name"] = language.make_word(random.choice([1, 2]))
    return species


def vary_pops(species):
    pop_std = 0.2 * (1 - species["population_conformity"])
    pop = {}
    for k in list(species.keys()):
        pop[k] = abs(round(random.normal(species[k], pop_std), 3))
    pop["objid"] = maths.uuid(n=13)
    pop["label"] = "pop"
    return pop


def get_pop_name(df, faction_no):
    # the pop name is the faction name plus an extra syllable.
    name = df[df["id"] == faction_no]["name"].values[0] + " " + language.make_word(1)
    return name


def get_n_factions(n_steps, conf):
    x = interp((1 - conf), linspace(0, 1, num=n_steps), [i for i in range(n_steps)])
    return int(round(x))


def make_factions(kmeans):
    factions = [
        {
            "id": i,
            "name": language.make_word(2),
            "objid": maths.uuid(n=13),
            "label": "faction",
        }
        for i in range(kmeans.n_clusters)
    ]
    return factions


def get_faction_objid(df, faction_no):
    objid = df[df["id"] == faction_no]["objid"].values[0]
    return objid


def build_people(data):
    # Get the Species
    species = build_species(data)
    # Build the populations (note that pops is a DataFrame)
    pops = pd.DataFrame([vary_pops(species) for i in range(data["starting_pop"])])
    # Build the factions
    n_factions = get_n_factions(n_steps, data["population_conformity"])
    kmeans = KMeans(n_clusters=n_factions).fit(pops)
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
        for p in pops
    ]
    isInFaction = [
        {"node1": p["objid"], "node2": p["isInFaction"], "label": "isInFaction"}
        for p in pops
    ]
    nodes = [species] + pops.to_dict("records") + factions
    edges = isInFaction + isOfSpecies
    return nodes, edges
