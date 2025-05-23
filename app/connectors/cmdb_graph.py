import os,sys, ssl

from functools import reduce
import operator

import yaml
import numpy as np
import pandas as pd


from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError


import asyncio


if sys.platform == 'win32':
    print("executing local windows deployment")


# ASSERTIONS: 
# Nodes must have expected values
expectedProperties = ['label','objid','name']

# Don't convert these to floats
notFloats = ['id','objid','orbitsId','isSupportsLife','isPopulated','label']


class GraphFormatError(Exception):
    """exodestiny data structure error graph error message for cosmos/gremlin checks"""
    pass


# TODO: For some reason this exception triggers when the app starts, but doesn't seem to be an issue. 
class ExoAdminGremlinQueryIssue(Exception):
    print(f"something wrong with your query: {Exception}")
    pass

#%%
# my Gremlin Model is like Django models in name only.
# I'm creating a client object and connecting it to the 

# NOTE: in order not to delay load times, try making small queries to populate the page first, 
# then handle additional queries in `axajviews`. This will be better for the clint in the long run. 

class CosmosdbClient():
    # TODO: build capability to 'upsert' nodes instead of drop and replace. 
    """s
    cb = CosmosdbClient()
    cb.add_query()
    cb.run_queries()

    data format = `{"nodes":nodes_list,"edges":edges_list}`

    node format = {
        'label':'foo',
        'objid':'00001',
        'name':'myname'
    }
    

    edge format = `{'node1':0000,'node2':0001,'label':'hasRelationship',...other properties}`
        it's always the objid of the nodes, connecting to the objid of the ohter node. 

    """
    def __init__(self) -> None:
        self.endpoint = os.getenv("COSMOS_DB_ENDPOINT","env vars not set")
        self.username = os.getenv("COSMOS_DB_USERNAME","env vars not set")
        self.password = os.getenv("COSMOS_DB_KEY","env vars not set")+"=="
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
                message_serializer=serializer.GraphSONSerializersV2d0()
            )
            
    def close_client(self):
        self.c.close()

    ## Managing the queries
    def run_query(self, query="g.V().count()"):
        self.open_client()
        callback = self.c.submitAsync(query)
        try:
            res = callback.result().all().result()
        except GremlinServerError as e:
            print(f"GremlinServerError: {e}")
            raise ExoAdminGremlinQueryIssue
            res = e
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

    def parse_properties(self,node):
        """
        used in actions and other places where json is nested in properties. 
        example:
                'properties': {'type': [{'id': 'de09040b-2c60-4a8a-b640-d78a248688f9',
                        'value': 'healthcare_initiatives'}],
                    'applies_to': [{'id': 'd753c296-7b62-4eb4-8e18-df39a67977ea',
                        'value': 'pop'}],
        returns nicely formated dict
        """
        n = {}
        for k in node["properties"].keys():
            if len(node["properties"][k]) == 1:
                n[k] = node["properties"][k][0]["value"]
        return n

    def parse_all_properties(self,res):
        """
        meant to pas in one response item at a time:
            `self.actions = [self.c.parse_all_properties(i) for i in self.c.res]`
        """
        r = {}
        for part in self.res[0].keys():
            if res[part]['type']=='edge':
                r[part] = res[part]['properties']
            else:
                r[part] = self.parse_properties(res[part])
        return r



    ## cleaning results
    def cs(self, s):
        # Clean String
        s = (str(s).replace("'", "")
                .replace("\\","-")
            )
        return s

    def clean_node(self, x):
        # For each value, return the last value in the array for that object. 
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
                try:
                    t[l]=self.clean_node(objects[i])
                except:
                    print("had an issue with ,",i,l, objects)
            fab.append(t)
        return fab

    def split_list_to_dict(self,lst,cols):
        """
        Some queries return a list of items that repeats. this breaks them down, but you have to know the column names. 
        **Note** that this requres that the length of the list is divisible by the length of the columns.
        example:
        ```
        ['Damshamunling',
        'planet',
        '6135767546801',
        'Teinspringsgio',
        'planet',
        '9482778660790']
        
        split_list_to_dict(c.res, ['name','label','objid'])
        ```
        turns into 
        ```
        [{'name': 'Damshamunling', 'label': 'planet', 'objid': '6135767546801'},
        {'name': 'Teinspringsgio', 'label': 'planet', 'objid': '9482778660790'}]
        ```
        """
        n_items = int(len(lst)/len(cols))
        res_dct = [{cols[i]:lst[(n_items*j)+i+j] for i in range(len(cols))} for j in range(n_items)]
        return res_dct

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
    def create_vertex(self,node, userguid):
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
            # converting boolian values to gremlin bools
            if type(node[k])==bool:
                node[k]=str(node[k]).lower()
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
        if 'userguid' not in properties:
            gaddv += f".property('userguid','{userguid}')"

        gaddv += f".property('objtype','{node['label']}')"
        return gaddv

    def create_edge(self, edge, userguid):
        gadde = f"g.V().has('objid','{edge['node1']}').addE('{self.cs(edge['label'])}').property('userguid','{userguid}')"
        for i in [j for j in edge.keys() if j not in ['label','node1','node2']]:
            gadde += f".property('{i}','{edge[i]}')"
        gadde_fin = f".to(g.V().has('objid','{self.cs(edge['node2'])}'))"
        return gadde + gadde_fin


    def upload_data(self, userguid, data):
        """
        uploads nodes and edges in a format `{"nodes":nodes,"edges":edges}`.
        edge format:
            `{'node1':0000,'node2':0001,'label':'hasRelationship',...other properties}`
        Each value is a list of dicts with all properties. 
        Extra items are piped in as properties of the edge.
        Note that edge lables don't show in a valuemap. So you need to add a 'name' to the properties if you want that info. 
        """
        data = self.test_fields(data)
        for node in data["nodes"]:
            n = self.create_vertex(node, userguid)
            self.add_query(n)
            if len(self.stack)>self.stacklimit:
                self.run_queries()
        self.run_queries()
        for edge in data["edges"]:
            e = self.create_edge(edge, userguid)
            self.add_query(e)
            if len(self.stack)>self.stacklimit:
                self.run_queries()
        self.run_queries()

    def patch_property(self, objid, property, value):
        """
        updates a specific property on a specific object
        """
        query = f"""
        g.V().has('objid','{objid}').property('{property}','{value}')
        """ 
        res = self.run_query(query)
        self.res = res

    def set_value(self, objid, property, value):
        """
        updates a specific property that is an int or float on a specific object
        """
        value = float(np.round(value,4))
        query = f"""
        g.V().has('objid','{objid}').property('{property}',{value})
        """ 
        res = self.run_query(query)
        self.res = res

    def delta_property(self,objid,property,x):
        """
        delta_property(objid,property,value)
        _____________________________________________________
        augments or diminishes a numerical property.
        e.g. health + x, or wealth + x
        if x is negative it will subtract
        """
        get_object_query = f"""
        g.V().has('objid','{objid}').valueMap()
        """
        self.run_query(get_object_query)
        o = self.clean_nodes(self.res)[0]
        og_value = o[property]
        # if the value is a float, convert it to a string.
        if type(og_value) != float:
            og_value = float(og_value)
        if type(x) != float:
            x = float(x)
        new_value = og_value + x
        if new_value < 0:
            new_value = 0
        # round new_value to 2 decimal places
        new_value = float(np.round(new_value,4))
        patch_query = f"""
            g.V().has('objid','{objid}').property('{property}',{new_value})
        """ 
        self.run_query(patch_query)
        o[property] = new_value
        return o

    def query_patch_properties(self, agent, action):
        query = f"g.V().has('objid','{agent['objid']}')"
        for n in yaml.safe_load(action["augments_self_properties"]):
            query += f".property('{n}',{agent[n]})"

        res = self.run_query(query)
        self.res = res