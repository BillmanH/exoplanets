#Bytecode Models for testing
# After some testing, looks like MSFT won't support bytecode. So this is a dead end. I'll keep the script here just for notes. 
# Here is a link to one of many discussions about this. 
# https://github.com/Azure-Samples/azure-cosmos-db-graph-nodejs-getting-started/issues/23

#%%
import yaml
from django.db import models
from gremlin_python.driver import serializer
from gremlin_python.driver.protocol import GremlinServerError

#Local modules:
from .GraphOperations import account


# my Gremlin Model is like Django models in name only.
# I'm creating a client object and connecting it to the 
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

#%%
# If running in REPL
# import nest_asyncio
# nest_asyncio.apply()
#%%
def get_traversal():
    '''
    g = get_traversal()
    '''
    config = yaml.safe_load(open("./configure.yaml"))
    g = traversal().withRemote(DriverRemoteConnection(
                                    config["endpoint"],
                                    "g",
                                    username = config["username"],
                                    password = config["password"],
                                    message_serializer=serializer.GraphSONSerializersV2d0()))
    return g



def run_query(client, g):
    res = g.V().count().next()
    return res

