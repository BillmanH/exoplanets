from ..connectors.cmdb_graph import *

def get_foreign_systems(request, data):
    userguid = request.identity_context_data._id_token_claims['oid']
    if 'system' in data.keys():
        if userguid != data['system']['userguid']:
            data['system']['hascontrol'] = "False"
            new_data = {'system':data['system'],
                        'nodes':[],
                        'edges':[]
                        }
        else:
            data['system']['hascontrol'] = "True"
            new_data = data
    if 'location' in data.keys():
        if userguid != data['location']['userguid']:
            data['location']['hascontrol'] = "False"
            new_data = {'location':{
                        'objid':data['location']['objid'],
                        'hascontrol':data['location']['hascontrol'],
            },
                        'time':data['time'],
                        'nodes':[],
                        'buildings':[],
                        'resources':[]
                        }
            
        else:
            userguid = data['location']['hascontrol'] = "True"
            new_data = data
    return new_data

def get_object_by_id(objid):
    query=f"g.V().has('objid','{objid}').valueMap()"
    c = CosmosdbClient()
    c.run_query(query)
    return c.clean_nodes(c.res)

def get_star_systems():
    # TODO: Create edge from user that connects to systems that have been discovered
    query="g.V().haslabel('system').has('name').valueMap('name','type','objid','glat','glon', 'gelat')"
    c = CosmosdbClient()
    c.run_query(query)
    return c.clean_nodes(c.res)

def get_time():
    query = "g.V().hasLabel('time').valueMap()"
    c = CosmosdbClient()
    c.run_query(query)
    time = c.clean_nodes(c.res)[0] #should only be one time
    return time

def get_home_system(userguid):
    # If they just created a new game, they will only have one system. 
    nodes_query = (
        f"g.V().hasLabel('system').has('userguid','{userguid}').in().valueMap()"
    )
    system_query = (
        f"g.V().hasLabel('system').has('userguid','{userguid}').has('isHomeSystem','true').valueMap()"
    )
    c = CosmosdbClient()
    c.add_query(nodes_query)
    c.add_query(system_query)
    c.run_queries()   
    nodes = c.res[nodes_query]
    if c.res[system_query]==[]:
        system = "No home system found"
        return system
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


def get_factions(userguid):
    nodes_query = (
        f"g.V().has('userguid','{userguid}').has('label','faction').valuemap()"
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
        .out('owns').as('building')
        .path()
            .by(valueMap('objid','name'))
            .by(valueMap('objid','name'))
            .by(valueMap('objid','type','name','changes','faction_augments','renews_faction_resource','renews_location_resource','planet_requirements','description','render_type','has_buttons','current_design'))
    """)
    location_query = f"g.V().has('objid','{objid}').valueMap()"

    c = CosmosdbClient()
    c.add_query(population_query)
    c.add_query(resource_query)
    c.add_query(building_query)
    c.add_query(biome_query)
    c.add_query(location_query)
    c.run_queries()   
    nodes = c.reduce_res(c.res[population_query])
    resources = c.clean_nodes(c.res[resource_query])
    biome = c.clean_nodes(c.res[biome_query])
    location = c.clean_nodes(c.res[location_query])[0] # should only be one location.
    buildings = []
    for iter, item in enumerate(c.res[building_query]):
        build = c.clean_node(item["objects"][2])
        owner = c.clean_node(item["objects"][1])
        build.update({"owner": owner["objid"]})
        buildings.append(build)
    buildings
    data = {"nodes": nodes, "edges": [], "resources":resources,"buildings":buildings, "biome":biome, "location":location}
    return data
