import asyncio
import time

import yaml,sys
#%% 
from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback
# from pygraphml import GraphMLParser
from tornado import httpclient

#%%
#Connection config

config = yaml.safe_load(open('../configure.yaml'))
endpoint = config['endpoint']
username = config['username']
password = config['password']
traversal_source = config['traversal_source']

#%%
# Getting the client
gremlin_count_vertices = "g.V().count()"


client = client.Client(endpoint, 'g',
                           username=username,
                           password=password,
                           message_serializer=serializer.GraphSONSerializersV2d0()
                           )

callback = client.submitAsync(gremlin_count_vertices)
print(callback.result().all().result())