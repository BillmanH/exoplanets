import os
# Pickle isn't used, but I might use it. 
import pickle

import yaml
import numpy as np
import pandas as pd
from django.db import models
from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError


#Local modules:
from .GraphOperations import account

# ASSERTIONS: 

# Nodes must have expected values
expectedProperties = ['label','objid','name']

# Don't convert these to floats
notFloats = ['id','objid','orbitsId','isSupportsLife','isPopulated','label']


class GraphFormatError(Exception):
    """exodestiny data structure error graph error message for cosmos/gremlin checks"""
    pass

#%%
# my Gremlin Model is like Django models in name only.
# I'm creating a client object and connecting it to the 

# NOTE: in order not to delay load times, try making small queries to populate the page first, 
# then handle additional queries in `axajviews`. This will be better for the clint in the long run. 

class CosmosdbClient():
    """
    cb = CosmosdbClient()
    cb.add_query()
    cb.run_queries()
    """
    def __init__(self) -> None:
        self.endpoint = os.getenv("endpoint","env vars not set")
        self.username = os.getenv("dbusername","env vars not set")
        self.password = os.getenv("dbkey","env vars not set")+"=="
        self.c = None
        self.res = "no query"
        self.stack = []
        self.res_stack = {}

    ## Managing the client
    def open_client(self):
            self.c = client.Client(
                self.endpoint,
                "g",
                username=self.username,
                password=self.password,
                message_serializer=serializer.GraphSONSerializersV2d0(),
            )
            
    def close_client(self):
        self.c.close()

    ## Managing the queries
    def run_query(self, query="g.V().count()"):
        self.open_client()
        callback = self.c.submitAsync(query)
        res = callback.result().all().result()
        self.close_client()
        self.res = res

    def run_query_from_list(self, query="g.V().count()"):
        callback = self.c.submitAsync(query)
        res = callback.result().all().result()
        self.res = res

    def add_query(self, query="g.V().count()"):
        self.stack.append(query)

    def run_queries(self):
        self.open_client()
        res = {}
        for q in self.stack:
            self.run_query_from_list(q)
            res[q] = self.res
        self.res = res
        self.close_client()

    ## cleaning results
    def cs(self, s):
        # Clean String
        s = str(s).replace("'", "")
        s = str(s).replace("\\","-")
        return s

    def clean_node(self, x):
        for k in list(x.keys()):
            if len(x[k]) == 1:
                x[k] = x[k][0]
        if 'objid' in x.keys():
            x["id"] = x["objid"]
        return x

    def clean_nodes(self, nodes):
        return [self.clean_node(n) for n in nodes]

    def query_to_dict(self, res):
        d = []
        for r in res:
            lab = {}
            for itr,itm in enumerate(r['labels']):
                lab[itm[0]] = self.clean_node(r['objects'][itr])
            d.append(lab)
        return d

    def flatten(self, list_of_lists):
        if len(list_of_lists) == 0:
            return list_of_lists
        if isinstance(list_of_lists[0], list):
            return self.flatten(list_of_lists[0]) + self.flatten(list_of_lists[1:])
        return list_of_lists[:1] + self.flatten(list_of_lists[1:])

    # creating strings for uploading data
    def create_vertex(self,node, username):
        if (len(
            [i for i in expectedProperties 
                if i in list(node.keys())]
                )>len(expectedProperties)
            ):
            raise GraphFormatError
        gaddv = f"g.addV('{node['label']}')"
        properties = [k for k in node.keys()]
        for k in properties:
            # try to convert objects that aren't ids
            if k not in notFloats:
                #first try to upload it as a float.
                try:
                    rounded = np.round_(node[k],4)
                    substr = f".property('{k}',{rounded})"
                except:
                    substr = f".property('{k}','{self.cs(node[k])}')"
            else:
                substr = f".property('{k}','{self.cs(node[k])}')"
            gaddv += substr
        gaddv += f".property('username','{username}')"
        gaddv += f".property('objtype','{node['label']}')"
        return gaddv

    def create_edge(self, edge, username):
        gadde = f"g.V().has('objid','{edge['node1']}').addE('{self.cs(edge['label'])}').property('username','{username}')"
        for i in [j for j in edge.keys() if j not in ['label','node1','node2']]:
            gadde += f".property('{i}','{edge[i]}')"
        gadde_fin = f".to(g.V().has('objid','{self.cs(edge['node2'])}'))"
        return gadde + gadde_fin


    def upload_data(self, username, data):
        """
        uploads nodes and edges in a format {"nodes":nodes,"edges":edges}.
        Each value is a list of dicts with all properties. 
        Extra items are piped in as properties of the edge.
        Note that edge lables don't show in a valuemap. So you need to add a 'name' to the properties if you want that info. 
        """
        self.open_client()
        self.nodes = []
        self.edges = []
        self.res = []
        for node in data["nodes"]:
            n = self.create_vertex(node, username)
            self.nodes.append(n)
            callback = self.c.submitAsync(n)
            self.res.append(callback.result().all().result())
        for edge in data["edges"]:
            e = self.create_edge(edge, username)
            self.nodes.append(e)
            callback = self.c.submitAsync(e)
            self.res.append(callback.result().all().result())
        self.close_client()



# Even though `clean_nodes` is a part of the CosmosdbClient, there are use cases where you need it independanty
# for example, cleaning nodes that were returned from the ajax-requests. 
def clean_node(x):
    for k in list(x.keys()):
        if len(x[k]) == 1:
            x[k] = x[k][0]
    if 'objid' in x.keys():
        x["id"] = x["objid"]
    return x

def clean_nodes(nodes):
    return [clean_node(n) for n in nodes]
    
def get_galaxy_nodes():
    # TODO: Add Glat and glon to systems when created
    # TODO: Create edge from user that connects to systems that have been discovered
    query="g.V().haslabel('system').valueMap('hostname','objid','disc_facility','glat','glon')"
    c = CosmosdbClient()
    c.run_query(query)
    return c.clean_nodes(c.res)



def get_system(username):
    # TODO: This process just assumes there is only one system per account. Eventually will need to expand to take 
    # a system parameter to specify which system the user would like to fetch. 
    nodes_query = (
        f"g.V().hasLabel('system').has('username','{username}').in().valueMap()"
    )
    c = CosmosdbClient()
    c.run_query(nodes_query)   
    nodes = c.res
    edges = [{"source":i['objid'][0],"target":i['orbitsId'][0],"label":"orbits"} for i in nodes if "orbitsId" in i.keys()]
    system = {"nodes": c.clean_nodes(nodes), "edges": edges}
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




