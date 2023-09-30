from .connectors.cmdb_graph import *

def get_galaxy_nodes():
    # TODO: Add Glat and glon to systems when created
    # TODO: Create edge from user that connects to systems that have been discovered
    query="g.V().haslabel('system').valueMap('hostname','objid','disc_facility','glat','glon')"
    c = CosmosdbClient()
    c.run_query(query)
    return c.clean_nodes(c.res)



def get_home_system(username):
    # If they just created a new game, they will only have one system. 
    nodes_query = (
        f"g.V().hasLabel('system').has('username','{username}').in().valueMap()"
    )
    system_query = (
        f"g.V().hasLabel('system').has('username','{username}').has('isHomeSystem','true').valueMap()"
    )
    c = CosmosdbClient()
    c.add_query(nodes_query)
    c.add_query(system_query)
    c.run_queries()   
    nodes = c.res[nodes_query]
    system = c.clean_nodes(c.res[system_query])[0]
    edges = [{"source":i['objid'][0],"target":i['orbitsId'][0],"label":"orbits"} for i in nodes if "orbitsId" in i.keys()]
    system = {"nodes": c.clean_nodes(nodes), "edges": edges, "system":system}
    return system

def get_system(objid,orientation):
    if orientation == 'planet':
        nodes_query = (
            f"g.V().has('objid','{objid}').out('isIn').in().valueMap()"
        )
        system_query = (
            f"g.V().has('objid','{objid}').out('isIn').valueMap()"
        )
    c = CosmosdbClient()
    c.add_query(nodes_query)
    c.add_query(system_query)
    c.run_queries()   
    nodes = c.res[nodes_query]
    system = c.clean_nodes(c.res[system_query])[0]
    edges = [{"source":i['objid'][0],"target":i['orbitsId'][0],"label":"orbits"} for i in nodes if "orbitsId" in i.keys()]
    system = {"nodes": c.clean_nodes(nodes), "edges": edges, "system":system}
    return system


def get_factions(username):
    nodes_query = (
        f"g.V().has('username','{username}').has('label','faction').valuemap()"
    )
    c = CosmosdbClient()
    c.run_query(nodes_query)   
    nodes = c.res
    system = {"nodes": c.clean_nodes(nodes), "edges": []}
    return system


def get_local_population(objid):
    # objid is the id of the object which contains ('inhabits') the population/s
    population_query = (
        f"""g.V().has('objid','{objid}').as('location')
            .in('inhabits').as('population')
            .local(
                union(
                    out('isIn').hasLabel('faction').as('faction'),
                    out('isOf').hasLabel('species').as('species')
                    )
                    .fold()).as('faction','species')
                    .path()
                    .by(unfold().valueMap().fold())"""
    )
    biome_query = f"""
        g.V().has('objid','{objid}').as('planet').in('isOn').haslabel('biome').valueMap()
    """
    resource_query = (
        f"""g.V().has('objid','{objid}').as('location')
            .out('has').haslabel('resource').as('resource').valueMap()
        """
    )
    building_query = (f"""g.V().has('objid','{objid}').as('location')
        .in('inhabits').as('population')
        .in('owns').as('building')
        .path()
            .by(valueMap('objid','name'))
            .by(valueMap('objid','name'))
            .by(valueMap('objid','name','changes','augments_resource','planet_requirements','description','render_type'))
    """)
    c = CosmosdbClient()
    c.add_query(population_query)
    c.add_query(resource_query)
    c.add_query(building_query)
    c.add_query(biome_query)
    c.run_queries()   
    nodes = c.reduce_res(c.res[population_query])
    resources = c.clean_nodes(c.res[resource_query])
    biome = c.clean_nodes(c.res[biome_query])
    buildings = []
    for iter, item in enumerate(c.res[building_query]):
        build = c.clean_node(item["objects"][2])
        owner = c.clean_node(item["objects"][1])
        build.update({"owner": owner["objid"]})
        buildings.append(build)
    buildings
    data = {"nodes": nodes, "edges": [], "resources":resources,"buildings":buildings, "biome":biome}
    return data
