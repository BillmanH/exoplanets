import yaml, os
import numpy as np
import pandas as pd
from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError


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


def run_query(query="g.V().count()"):
    c = get_client()
    callback = c.submitAsync(query)
    res = callback.result().all().result()
    c.close()
    return res

def cs(s):
    # Clean String
    s = str(s).replace("'", "")
    return s

def clean_node(x):
    for k in list(x.keys()):
        if len(x[k]) == 1:
            x[k] = x[k][0]
    x["id"] = x["objid"]
    return x

def qtodf (query):
    '''
    Convinience function for getting the results as a dataframe. Assumes `.valueMap()` query.
        * runs `run_query(query)`
        * cleans each node
        * returns pandas dataframe
    '''
    res = run_query(query)
    nodes = [clean_node(n) for n in res]
    return pd.DataFrame(nodes)

def uuid(n=13):
    return "".join([str(i) for i in np.random.choice(range(10), n)])

def create_vertex(node):
    gaddv = f"g.addV('{node['label']}')"
    node['username'] = 'notebook'
    node['objtype'] = node['label']
    properties = [k for k in node.keys() if k != 'label']
    for k in properties:
        substr = f".property('{k}','{cs(node[k])}')"
        gaddv += substr
    if 'objid' not in properties:
        gaddv += f".property('objid','{uuid()}')"
    return gaddv

def create_edge(edge):
    properties = [k for k in edge.keys() if (k != 'label')&('node' not in k)]
    eprop =  ".property('username','notebook')"
    for k in properties:
        eprop += f".property('{k}','{cs(edge[k])}')"
    gadde = f"g.V().has('objid','{edge['node1']}').addE('{cs(edge['label'])}'){eprop}.to(g.V().has('objid','{cs(edge['node2'])}'))"
    return gadde


def upload_data(data,verbose=True): 
    c = get_client()
    for node in data["nodes"]:
        gadv = create_vertex(node)
        callback = c.submitAsync(gadv)
        if verbose:
            print(gadv)
            # print(callback)
    for edge in data["edges"]:
        gadde = create_edge(edge)
        callback = c.submitAsync(gadde)
        if verbose:
            print(gadde)
            # print(callback)
    c.close()
    return