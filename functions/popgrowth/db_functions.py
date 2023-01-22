from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError
import os

from functools import reduce
import operator

def get_client():
    '''
    c = get_client()
    '''
    endpoint = os.getenv("endpoint","env vars not set")
    username = os.getenv("dbusername","env vars not set")
    password = os.getenv("dbkey","env vars not set")+"=="
    client_g = client.Client(
        endpoint,
        "g",
        username=username,
        password=password,
        message_serializer=serializer.GraphSONSerializersV2d0(),
    )
    return client_g

def run_query(client, query="g.V().count()"):
    """
    run_query(client, query)
    run_query(c, query)
    """
    callback = client.submitAsync(query)
    res = callback.result().all().result()
    return res


def clean_node(x):
    '''
    Can also be used to clean edges, but there won't be an objid. 
    '''
    for k in list(x.keys()):
        if len(x[k]) == 1:
            x[k] = x[k][0]
    if 'objid' in x.keys():
        x["id"] = x["objid"]
    return x

def reduce_res(res):
    fab = []
    for n,r in enumerate(res): 
        t = {}
        labels = reduce(operator.concat, r['labels'])
        objects = reduce(operator.concat, r['objects'])

        for i,l in enumerate(labels):
            t[l]=clean_node(objects[i])
        fab.append(t)
    return fab