import os
# Pickle isn't used, but I might use it. 
import pickle

import yaml
from django.db import models
from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError

#Local modules:
from .GraphOperations import account

#%%
# my Gremlin Model is like Django models in name only.
# I'm creating a client object and connecting it to the 


def get_client():
    '''
    c = get_client()
    '''
    endpoint = os.getenv("endpoint","env vars not set")
    username = os.getenv("dbusername","env vars not set")
    password = os.getenv("dbkey","env vars not set")+"=="
    client_g = client.Client(
        endpoint,
        "g",
        username=username,
        password=password,
        message_serializer=serializer.GraphSONSerializersV2d0(),
    )
    return client_g


def run_query(client, query="g.V().count()"):
    """
    run_query(client, query)
    run_query(c, query)
    """
    callback = client.submitAsync(query)
    res = callback.result().all().result()
    return res


def cs(s):
    # Clean String
    s = str(s).replace("'", "")
    return s


def create_vertex(node, username):
    gaddv = f"g.addV('{node['label']}')"
    properties = [k for k in node.keys()]
    for k in properties:
        substr = f".property('{k}','{cs(node[k])}')"
        gaddv += substr
    gaddv += f".property('username','{username}')"
    gaddv += f".property('objtype','{node['label']}')"
    return gaddv


def check_vertex(node):
    gaddv = f"g.V().has('objid',{node['objid']})"
    return gaddv


def create_edge(edge, username):
    gadde = f"g.V().has('objid','{edge['node1']}').addE('{cs(edge['label'])}').property('username','{username}').to(g.V().has('objid','{cs(edge['node2'])}'))"
    return gadde


def upload_data(client, username, data):
    for node in data["nodes"]:
        callback = client.submitAsync(create_vertex(node, username))
    for edge in data["edges"]:
        callback = client.submitAsync(create_edge(edge, username))
    return


def get_galaxy_nodes(client):
    # TODO: Add Glat and glon to systems when created
    # TODO: Create edge from user that connects to systems that have been discovered
    query="g.V().haslabel('system').valueMap('hostname','objid','disc_facility','glat','glon')"
    callback = client.submitAsync(query)
    res = callback.result().all().result()
    return clean_nodes(res)


def clean_node(x):
    for k in list(x.keys()):
        if len(x[k]) == 1:
            x[k] = x[k][0]
    x["id"] = x["objid"]
    return x

def clean_nodes(nodes):
    return [clean_node(n) for n in nodes]

def get_system(client, username):
    # TODO: This process just assumes there is only one system per account. Eventually will need to expand to take 
    # a system parameter to specify which system the user would like to fetch. 
    nodes_query = (
        f"g.V().hasLabel('system').has('username','{username}').in().valueMap()"
    )
    
    node_callback = client.submitAsync(nodes_query)
    nodes = node_callback.result().all().result()
    edges = [{"source":i['objid'][0],"target":i['orbitsId'][0],"label":"orbits"} for i in nodes if "orbitsId" in i.keys()]
    system = {"nodes": clean_nodes(nodes), "edges": edges}

    return system
