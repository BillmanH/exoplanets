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
# I'm creating a client object and using that connection to query the graph
# The backend is all about the query string


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

def clean_node(x):
    for k in list(x.keys()):
        if len(x[k]) == 1:
            x[k] = x[k][0]
    x["id"] = x["objid"]
    return x

def clean_nodes(nodes):
    return [clean_node(n) for n in nodes]

