# Backend functions runnign on a separate server.
# The Engine is something that is running all of the time. 
# Manages the passage of time, and the resolution of actions.

import datetime
import logging
import pandas as pd
import yaml
import pickle
import os
import asyncio

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from azure.identity.aio import DefaultAzureCredential

from app.connectors.cmdb_graph import CosmosdbClient
from app.objects import time as t

# Load configurations
logging.basicConfig(filename='engine.log', level=logging.INFO)
pop_growth_params = yaml.safe_load(open('app/configurations/popgrowthconfig.yaml'))
syllables = pickle.load(open('app/creators/specs/syllables.p', "rb"))

# Loading the event Hub

EVENT_HUB_CONNECTION_STR = os.environ.get("EVENT_HUB_CONNECTION_STR", "ERROR: Event Hub Connection not found")
EVENT_HUB_NAME = os.environ.get('EVENT_HUB_NAME', "ERROR: Event Hub Name not found")

eh_time_producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name="EXO_TIME"
    )

eh_action_producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name="EXO_ACTION"
    )

logging.info(f'Event hub: {EVENT_HUB_NAME}')

def get_time_from_cmdb(c):
    # Increments time and resolves actions
    # not to be confused with python's time object in the datetime library
    time = t.Time(c)
    time.get_current_UTU()
    logging.info(f'*** Time function ran at: {time }')
    return time



def update_time():
    async def run():
        async with eh_time_producer:
            event_data_batch = await eh_time_producer.create_batch()
            event_data_batch.add(EventData('Single message'))
            await eh_time_producer.send_batch(event_data_batch)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def resolve_actions(actions):
    async def run():
        async with eh_action_producer:
            event_data_batch = await eh_action_producer.create_batch()
            event_data_batch.add(EventData('Single message'))
            await eh_action_producer.send_batch(event_data_batch)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def main():
    runtime = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f'Engine started at: {runtime}')
    # Get the current time from the CMDB
    c = CosmosdbClient()
    current_time = get_time_from_cmdb(c)
    update_time()
    # resolve_actions(actions)
    logging.info(f'Current time: {current_time}')



if __name__ == "__main__":
    main()