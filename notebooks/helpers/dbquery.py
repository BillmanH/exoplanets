import yaml

from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError

def get_client():
    '''
    c = get_client()
    '''
    try:
        config = yaml.safe_load(open("./configure.yaml"))
    except FileNotFoundError:
        config = yaml.safe_load(open("../../configure.yaml"))
    endpoint = config["endpoint"]
    username = config["username"]
    password = config["password"]
    client_g = client.Client(
        endpoint,
        "g",
        username=username,
        password=password,
        message_serializer=serializer.GraphSONSerializersV2d0(),
    )
    return client_g


def run_query(client, query="g.V().count()"):
    c = get_client()
    """
    run_query(client, query)
    run_query(c, query)
    """
    callback = client.submitAsync(query)
    res = callback.result().all().result()
    c.close()
    return res