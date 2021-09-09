import yaml, os

from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError


def get_client():
    '''
    c = get_client()
    '''
    endpoint = os.getenv("endpoint","env vars not set")
    username = os.getenv("username","env vars not set")
    password = os.getenv("password","env vars not set")+"=="
    client_g = client.Client(
        endpoint,
        "g",
        username=username,
        password=password,
        message_serializer=serializer.GraphSONSerializersV2d0(),
    )
    return client_g


def run_query(query="g.V().count()"):
    c = get_client()
    callback = c.submitAsync(query)
    res = callback.result().all().result()
    c.close()
    return res