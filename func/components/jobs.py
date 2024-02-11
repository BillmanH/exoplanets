import logging
import json
from azure.eventhub import EventData
import asyncio

def resolve_jobs(c,t,actions):
    # resolves actions
    # not to be confused with python's time object in the datetime library
    messages = []
    # Get all pending actions 
    t.get_global_actions()
    
    logging.info(f'Total jobs: {len(t.actions)}')
    validjob = 0 
    for i in t.actions:
        action = actions.Action(c,i)
        if action.validate_action_time(t):
            validjob += 1
            messages.append(action.get_action_message())
            logging.info(f'{action} was added to the message queue')

    logging.info(f'Total actions resolved in this run: {validjob}')

    return messages


def send_to_eventhub(messages, eh_producer):
    async def run(messages):
        async with eh_producer:
            event_data_batch = await eh_producer.create_batch()
            for message in messages:
                dump = json.dumps(message)
                event_data_batch.add(EventData(dump))
            await eh_producer.send_batch(event_data_batch)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop() 
    loop.run_until_complete(run(messages))