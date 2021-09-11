import yaml, os
import numpy as np
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
    return gaddv

def create_edge(edge):
    properties = [k for k in edge.keys() if (k != 'label')&('node' not in k)]
    eprop =  ".property('username','notebook')"
    for k in properties:
        eprop += f".property('{k}','{cs(edge[k])}')"
    gadde = f"g.V().has('objid','{edge['node1']}').addE('{cs(edge['label'])}'){eprop}.to(g.V().has('objid','{cs(edge['node2'])}'))"
    return gadde


def upload_data(data): 
    c = get_client()
    for node in data["nodes"]:
        callback = c.submitAsync(create_vertex(node))
    for edge in data["edges"]:
        callback = c.submitAsync(create_edge(edge))
    c.close()
    return