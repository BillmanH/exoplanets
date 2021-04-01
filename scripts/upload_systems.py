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

pl_df = pd.read_csv('../data/parsed_planets.csv')

sy_df = pl_df.drop_duplicates(subset='hostname')[[c for c in pl_df.columns if 'pl_' not in c]]

# Check that planets and hostnames don't match:
pl_df['matches_host'] = pl_df['pl_name']==pl_df['hostname']
if len(pl_df['matches_host'].unique())>1:
    raise Exception("A planet as the same name as the host. Cannot create edge to self.")


#%%

def uuid(n=8):
    return ''.join([str(i) for i in np.random.choice(range(10),n)])

def cs(s):
    #Clean String
    s = str(s).replace("'","")
    return s

def create_vertex(labelV,node):
    gaddv = f"g.addV('{labelV}')"
    properties = [k for k in node.keys() if str(node[k])!='nan']
    for k in properties:
        substr = f".property('{k}','{cs(node[k])}')"
        gaddv += substr
    gaddv += f".property('objid','{uuid()}')"
    return gaddv

def create_edge(labelE,node1,node2,node1L,node2L,node1cl,node2cl):
    gadde = f"g.V().hasLabel('{node1cl}').has('{cs(node1L)}','{cs(node1)}').addE('{cs(labelE)}').to(g.V().hasLabel('{node2cl}').has('{cs(node2L)}','{cs(node2)}'))"
    return gadde

# # Upload Planets
# for i in df.index:
#     node = df.loc[i].dropna().to_dict()
#     addstr = create_vertex('planet',node)
#     callback = client_g.submitAsync(addstr)
#     res = callback.result().all().result()
#     print(node['pl_name'], i ,i/len(df.index))

# # Upload systems
# for i in df.index:
#     node = sy_df.loc[i].dropna().to_dict()
#     addstr = create_vertex('system',node)
#     callback = client_g.submitAsync(addstr)
#     res = callback.result().all().result()
#     print(node['hostname'], i ,i/len(sy_df.index))


# Assuming planets and systems are both updated, you can link them. 
pairs = pl_df[['pl_name','hostname']].drop_duplicates().values
for i,p in enumerate(pairs[::-1]):
    addstr = create_edge('isInSystem',p[0],p[1],'pl_name','hostname','planet','system')
    callback = client_g.submitAsync(addstr)
    res = callback.result().all().result()
    print(p, i ,i/len(pairs))


