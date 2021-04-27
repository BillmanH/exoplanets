from django.db import models

from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import yaml, os

#%%
# my Gremlin Model is like Django modesl in name only.


def get_client():
    config = yaml.safe_load(open("./configure.yaml"))
    endpoint = config["endpoint"]
    username = config["username"]
    password = config["password"]
    client_g = client.Client(
        endpoint,
        "g",
        username=username,
        password=password,
        message_serializer=serializer.GraphSONSerializersV2d0(),
    )
    return client_g


def run_query(client, query="g.V().count()"):
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
    return gaddv


def check_vertex(node):
    gaddv = f"g.V().has('objid',{node['objid']})"
    return gaddv


def create_edge(edge, username):
    gadde = f"g.V().has('objid','{edge['node1']}').addE('{cs(edge['label'])}').property('username','{username}').to(g.V().has('objid','{cs(edge['node2'])}'))"
    return gadde


def upload_data(client, username, data):
    for node in data["nodes"]:
        callback = client.submit(create_vertex(node, username))
    for edge in data["edges"]:
        callback = client.submit(create_edge(edge, username))
    ## link system to
    return


def get_galaxy_nodes(client, query="g.V().haslabel('system')"):
    callback = client.submitAsync(query)
    res = callback.result().all().result()
    return res


def get_system(client, username):
    nodes_query = (
        f"g.V().hasLabel('system').has('username','{username}').in().valueMap()"
    )
    node_callback = client.submitAsync(nodes_query)
    nodes = node_callback.result().all().result()
    edges_query = f"g.V().hasLabel('system').has('username','{username}').inE().outV().path().by('objid').by(label())"
    edges_callback = client.submitAsync(edges_query)
    edges = edges_callback.result().all().result()
    return {"nodes": nodes, "edges": edges}
