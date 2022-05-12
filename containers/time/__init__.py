import datetime
import logging

import azure.functions as func
from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError

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
    
def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
