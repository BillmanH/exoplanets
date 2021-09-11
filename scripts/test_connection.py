import asyncio
import time

import yaml,sys, os
#%% 
from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback


#%%
#Connection config
endpoint = os.getenv("endpoint","env vars not set")
username = os.getenv("dbusername","env vars not set")
password = os.getenv("dbkey","env vars not set")+"=="


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