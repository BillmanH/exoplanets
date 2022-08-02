import yaml, os
import numpy as np
import pandas as pd
from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError

# Don't convert these to floats
notFloats = ['id','objid','orbitsId','isSupportsLife','isPopulated','label']
# Nodes must have expected values
expectedProperties = ['label','objid','name']

class GraphFormatError(Exception):
    """exodestiny data structure error graph error message for cosmos/gremlin checks"""
    pass

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


def create_vertex(node, username):
    if (len(
        [i for i in expectedProperties 
            if i in list(node.keys())]
            )>len(expectedProperties)
        ):
        raise GraphFormatError
    gaddv = f"g.addV('{node['label']}')"
    properties = [k for k in node.keys() if k not in expectedProperties]
    for k in properties:
        # try to convert objects that aren't ids
        if k not in notFloats:
            #first try to upload it as a float.
            try:
                rounded = np.round_(node[k],4)
                substr = f".property('{k}',{rounded})"
            except:
                substr = f".property('{k}','{cs(node[k])}')"
        else:
            substr = f".property('{k}','{cs(node[k])}')"
        gaddv += substr
    gaddv += f".property('username','{username}')"
    gaddv += f".property('objtype','{node['label']}')"
    gaddv += f".property('objid','{uuid(n=13)}')"
    return gaddv


def create_edge(edge, username):
    gadde = f"g.V().has('objid','{edge['node1']}').addE('{cs(edge['label'])}').property('username','{username}')"
    for i in [j for j in edge.keys() if j not in ['label','node1','node2']]:
        if i == 'weight':
            gadde += f".property('{i}',{edge[i]})"
        else:
            gadde += f".property('{i}','{edge[i]}')"
    gadde_fin = f".to(g.V().has('objid','{cs(edge['node2'])}'))"
    return gadde + gadde_fin


def upload_data(c,data,verbose=True): 
    for node in data["nodes"]:
        gadv = create_vertex(node, "notebook")
        callback = c.submitAsync(gadv)
        if verbose:
            print(gadv)
            print(callback)
    for edge in data["edges"]:
        gadde = create_edge(edge)
        callback = c.submitAsync(gadde)
        if verbose:
            print(gadde)
            print(callback)
    return

c = get_client()