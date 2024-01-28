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
from app.objects import structures
from app.functions import consumption, growth, replenish_resources, configurations


# Load configurations
buildings_config = configurations.get_building_configurations()
logging.basicConfig(filename='engine.log', level=logging.INFO)
pop_growth_params = yaml.safe_load(open('app/configurations/popgrowthconfig.yaml'))
syllables = pickle.load(open('app/creators/specs/syllables.p', "rb"))

# Loading the event Hub
credential = DefaultAzureCredential() 
EVENT_HUB_FULLY_QUALIFIED_NAMESPACE = os.environ.get('EVENT_HUB_FULLY_QUALIFIED_NAMESPACE')
EVENT_HUB_NAME = os.environ.get('EVENT_HUB_NAME')

eh_producer = EventHubProducerClient(
        fully_qualified_namespace=EVENT_HUB_FULLY_QUALIFIED_NAMESPACE,
        eventhub_name=EVENT_HUB_NAME,
        credential=credential,
    )

logging.info(f'Event hub: {EVENT_HUB_FULLY_QUALIFIED_NAMESPACE}:{EVENT_HUB_NAME}')

def test_eventhub():
    """
    This is a test function to see if the event hub is working
    not executed in the main function
    """
    async def run():
        async with eh_producer:
            event_data_batch = await eh_producer.create_batch()
            event_data_batch.add(EventData('Single message'))
            await eh_producer.send_batch(event_data_batch)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

def time(c,event_data_batch):
    # Increments time and resolves actions
    # not to be confused with python's time object in the datetime library
    time = t.Time(c)
    time.get_current_UTU()
    logging.info(f'*** Time function ran at: {time }')
    # Get all pending actions 
    time.get_global_actions()
    actions_df = pd.DataFrame(time.actions)
    
    logging.info(f'Total jobs: {actions_df.shape[0]}')
    validActionCounter = 0 
    new_buildings = []
    for i in actions_df.index:
        action = t.Action(c,actions_df.loc[i])
        if action.validate_action_time(time):
            validActionCounter += 1
            action.add_updates_to_c(time)
            # action.resolve_action()
            if action.action.get('type') == 'construction':
                # TODO: possibility that there are constructions other than buildings. 
                b = [b for b in buildings_config['building']['buildings'] if b['name'] == action.action['building']][0]
                new_buildings.append(structures.Building(action.agent,b))
            logging.info(f'{action} was resolved')

    logging.info(f'{len(new_buildings)} new buildings were created')
    if len(new_buildings) > 0:
        upload_new_buildings(new_buildings,c)

    logging.info(f'Total actions resolved in this run: {validActionCounter}')
    
    # Increment global time
    time.global_ticker()

    logging.info(f'*** Time function ended')

    return time

def upload_new_buildings(new_buildings,c):
    data = {"nodes": [], "edges": []}
    for b in new_buildings:
        data['nodes'].append(b.get_data())
        data['edges'].append(b.get_owned_by())
    c.upload_data('buildings',data)

def popgrowth(c,t):
    logging.info(f'*** Population growth function started at: {t }')
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    pop_growth_params['currentTime'] = t.params['currentTime']

    consumption.consume(c,pop_growth_params)

    growth.grow(c,pop_growth_params)
    logging.info(f'*** Population growth ended')



def main():
    runtime = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f'*** Engine started at: {runtime}')
    c = CosmosdbClient()

    event_data_batch = eh_producer.create_batch()
    t = time(c,event_data_batch)
    eh_producer.send_batch(event_data_batch)
    # popgrowth(c,t)
    # replenish_resources.renew_resources(c)
    endtime = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f'*** Engine loop finsihed at: {endtime}')
    credential.close()

if __name__ == "__main__":
    main()


    # def test_eventhub():
    # async def run():
    #     async with eh_producer:
    #         event_data_batch = await eh_producer.create_batch()
    #         event_data_batch.add(EventData('Single message'))
    #         await eh_producer.send_batch(event_data_batch)

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(run())