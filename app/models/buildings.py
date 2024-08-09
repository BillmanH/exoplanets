from ..connectors.cmdb_graph import *


def get_faction():
    query="g.V().haslabel('system').has('name').valueMap('name','type','objid','glat','glon', 'gelat')"
    c = CosmosdbClient()
    c.run_query(query)
    return c.clean_nodes(c.res)

def get_population():
    query="g.V().haslabel('system').has('name').valueMap('name','type','objid','glat','glon', 'gelat')"
    c = CosmosdbClient()
    c.run_query(query)
    return c.clean_nodes(c.res)