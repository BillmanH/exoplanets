#%%
import time
import yaml
import pandas as pd
import numpy as np
#%% 
from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError



#%%
#Connection config

config = yaml.safe_load(open('../configure.yaml'))
endpoint = config['endpoint']
username = config['username']
password = config['password']


#%%
# Getting the client
gremlin_count_vertices = "g.V().count()"


client_g = client.Client(endpoint, 'g',
                           username=username,
                           password=password,
                           message_serializer=serializer.GraphSONSerializersV2d0()
                           )

callback = client_g.submitAsync(gremlin_count_vertices)
print(callback.result().all().result())


#%%
# Loading the Dataframe
import os
os.listdir()
df = (pd.read_csv('../data/parsed_planets.csv')
    .drop_duplicates(subset='hostname'))
df = df[[c for c in df.columns if 'pl_' not in c]]

#%%

def uuid():
    return ''.join([str(i) for i in np.random.choice(range(10),8)])

def create_vertex(labelV,node):
    gaddv = f"g.addV('{labelV}')"
    properties = [k for k in node.keys() if str(node[k])!='nan']
    for k in properties:
        value = str(node[k]).replace("'","")
        substr = f".property('{k}','{value}')"
        gaddv += substr
    gaddv += f".property('objid','{uuid()}')"
    return gaddv

# Upload systems
for i in df.index:
    node = df.loc[i].dropna().to_dict()
    addstr = create_vertex('system',node)
    callback = client_g.submitAsync(addstr)
    res = callback.result().all().result()
    print(node['hostname'], i ,i/len(df.index))

# Assuming planets and systems. 