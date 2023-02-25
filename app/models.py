import os,sys

from functools import reduce
import operator

import yaml
import numpy as np
import pandas as pd
from django.db import models
from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError

import asyncio
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


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
    # TODO: build capability to 'upsert' nodes instead of drop and replace. 
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
        self.stack = []
        self.close_client()

    ## cleaning results
    def cs(self, s):
        # Clean String
        s = (str(s).replace("'", "")
                .replace("\\","-")
            )
        return s

    def clean_node(self, x):
        for k in list(x.keys()):
            if type(x[k])==list:
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

    def reduce_res(self, res):
        fab = []
        for n,r in enumerate(res): 
            t = {}
            labels = reduce(operator.concat, r['labels'])
            objects = reduce(operator.concat, r['objects'])

            for i,l in enumerate(labels):
                try:
                    t[l]=self.clean_node(objects[i])
                except:
                    print("had an issue with ,",i,l, objects)
            fab.append(t)
        return fab

    def test_fields(self,data):
        for n in data['nodes']:
            n['id']=n['objid']
        return data

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
        if 'username' not in properties:
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
        data = self.test_fields(data)
        for node in data["nodes"]:
            n = self.create_vertex(node, username)
            self.add_query(n)
            if len(self.stack)>15:
                self.run_queries()
        self.run_queries()
        for edge in data["edges"]:
            e = self.create_edge(edge, username)
            self.add_query(e)
            if len(self.stack)>15:
                self.run_queries()
        self.run_queries()


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



def get_home_system(username):
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
            f"g.V().has('objid','{objid}').out('isInSystem').in().valueMap()"
        )
        system_query = (
            f"g.V().has('objid','{objid}').out('isInSystem').valueMap()"
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
    nodes_query = (
        f"""g.V().has('objid','{objid}').as('location')
            .in('inhabits').as('population')
            .local(
                union(
                    out('isInFaction').as('faction'),
                    out('isOfSpecies').as('species')
                    )
                    .fold()).as('faction','species')
                    .path()
                    .by(unfold().valueMap().fold())"""
    )
    c = CosmosdbClient()
    c.run_query(nodes_query)   
    nodes = c.reduce_res(c.res)
    data = {"nodes": nodes, "edges": []}
    return data
