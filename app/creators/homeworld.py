# Doc taken from
# notebooks/People/Generating Population

import pandas as pd
from numpy import interp, linspace
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA



from ..objects import species
from ..objects import population


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


def get_n_factions(n_steps, conf):
    x = interp((1 - conf), linspace(0, 1, num=n_steps), [i for i in range(n_steps)])
    return int(round(x))


def get_faction_objid(df, faction_no):
    objid = df[df["faction_no"] == faction_no]["objid"].values[0]
    return objid


def build_people(data):
    # Get the Species
    spec = species.Species()
    spec.build_attr(data)

    # Build the populations (note that pops is a DataFrame)
    pops = [population.Pop(spec) for i in range(int(data["starting_pop"]))]

    # Build the factions based on Kmeans Clustering
    pops_df = pd.DataFrame([p.get_data() for p in pops])
    n_factions = get_n_factions(n_steps, float(data["conformity"]))
    kmeans = KMeans(n_clusters=n_factions).fit(
        pops_df[[c for c in pops_df.columns if c in starting_attributes]]
    )

    factions = [population.Faction(i) for i in range(kmeans.n_clusters)]

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
                            
    # PCA Part
    pca = PCA(n_components=2)
    X_r = pca.fit(kmeans.cluster_centers_).transform(kmeans.cluster_centers_)
    for i,f in enumerate(factions):
        f.pca_explained_variance_ratio = pca.explained_variance_ratio_
        f.lat = X_r[i][0]
        f.long = X_r[i][1]


    # sum up the nodes and edges for return
    isOfSpecies = [p.isOfSpecies for p in pops]
    isInFaction = []
    for f in factions:
        isInFaction+= f.get_faction_pop_edge()
        

    nodes = [spec.get_data()] + [pop.get_data() for pop in pops] + [f.get_data() for f in factions]
    edges = isInFaction + isOfSpecies
    
    return nodes, edges


def attach_people_to_world(homeworld_nodes, homeworld):
    # in the beginning there should only be one homeworld
    pops = [p for p in homeworld_nodes if p.get("label") == "pop"]
    edges = [
        {"node1": p["objid"], "node2": homeworld["objid"], "label": "inhabits"}
        for p in pops
    ]
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

