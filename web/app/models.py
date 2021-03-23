from django.db import models

from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import yaml,os
#%%
# my Gremlin Model is like Django modesl in name only. 

def get_client():
    config = yaml.safe_load(open('configure.yaml'))
    endpoint = config['endpoint']
    username = config['username']
    password = config['password']
    traversal_source = config['traversal_source']
    client_g = client.Client(endpoint, 'g',
                            username=username,
                            password=password,
                            message_serializer=serializer.GraphSONSerializersV2d0()
                            )
    return client_g

def run_query(client,query="g.V().count()"):
    callback = client.submitAsync(query)
    res = callback.result().all().result()
    return res
