import os
# Pickle isn't used, but I might use it. 
import pickle
from functools import reduce
import operator

import yaml
import numpy as np
import pandas as pd

from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError
import logging


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
        # Note username is removed when performing in Azure Functions
        self.endpoint = os.getenv("endpoint","env vars not set")
        self.password = os.getenv("dbkey","env vars not set")+"=="
        self.username = os.getenv("dbusername","env vars not set")
        self.c = None
        self.res = "no query"
        self.stack = []
        self.stacklimit = 15
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
                x[k] = x[k][-1]
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
                t[l]=self.clean_node(objects[i])
            fab.append(t)
        return fab

    def test_fields(self,data):
        for n in data['nodes']:
            n['id']=n['objid']
        return data

    def create_custom_edge(self,n1,n2,label):
        edge = f"""
        g.V().has('objid','{n1['objid']}')
            .addE('{label}')
            .to(g.V().has('objid','{n2['objid']}'))
        """
        return edge
    
    # creating strings for uploading data
    def create_vertex(self,node):
        node['objid'] = str(node['objid'])
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
            gaddv += f".property('username','azfunction')"
        gaddv += f".property('objtype','{node['label']}')"
        # logging.info(f'gaddv: {gaddv}')
        return gaddv

    def create_edge(self, edge):
        gadde = f"g.V().has('objid','{edge['node1']}').addE('{self.cs(edge['label'])}').property('username','azfunction')"
        for i in [j for j in edge.keys() if j not in ['label','node1','node2']]:
            gadde += f".property('{i}','{edge[i]}')"
        gadde_fin = f".to(g.V().has('objid','{self.cs(edge['node2'])}'))"
        return gadde + gadde_fin


    def upload_data(self, data):
        """
        uploads nodes and edges in a format {"nodes":nodes,"edges":edges}.
        Each value is a list of dicts with all properties. 
        Extra items are piped in as properties of the edge.
        Note that edge lables don't show in a valuemap. So you need to add a 'name' to the properties if you want that info. 
        """
        data = self.test_fields(data)
        for node in data["nodes"]:
            n = self.create_vertex(node)
            self.add_query(n)
            if len(self.stack)>self.stacklimit:
                self.run_queries()
        self.run_queries()
        for edge in data["edges"]:
            e = self.create_edge(edge)
            self.add_query(e)
            if len(self.stack)>self.stacklimit:
                self.run_queries()
        self.run_queries()

