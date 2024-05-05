import azure.functions as func
from azure.eventhub.aio import EventHubProducerClient
from azure.identity.aio import DefaultAzureCredential

import datetime
import ast
import os
import logging
import yaml

# I should be able to pull the modules from the same libraries as the game iteself. 
from app.objects import time
from app.connectors import cmdb_graph
from app.functions import growth

app = func.FunctionApp()


EVENT_HUB_FULLY_QUALIFIED_NAMESPACE = os.environ.get('EVENT_HUB_FULLY_QUALIFIED_NAMESPACE')
EVENT_HUB_CONNECTION_STR = os.environ.get('EVENT_HUB_CONNECTION_STR')
EVENT_HUB_NAME = os.environ.get('EVENT_HUB_NAME')

eh_producer = EventHubProducerClient.from_connection_string(EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)
credential = DefaultAzureCredential() 

# func start --functions [a space separated list of functions]
# func start --functions actionResolverTimer resolveActionEvents ututimer

@app.function_name(name="resolveActionEvents")
@app.event_hub_message_trigger(arg_name="event",
                               event_hub_name=EVENT_HUB_NAME,
                               connection="EVENT_HUB_CONNECTION_STR")
def resolve_action_event(event: func.EventHubEvent):
    message = ast.literal_eval(event.get_body().decode('utf-8'))
    logging.info(f'Python EventHub trigger processed an messasge: {message} : {type(message)}')
    c = cmdb_graph.CosmosdbClient()
    t = time.Time(c)
    t.get_current_UTU()
    if 'job' in message.keys():
        action = time.Action(c,message)
        action.add_updates_to_c(t)
        c.upload_data(action.agent['userguid'], action.data)
        logging.info(f'      -------And with that processed an action: {action} at UTU:{t}')
    if message.get('action')=="rerpoduce":
        growth.grow_population(c,t, message['agent'])
        logging.info(f'      -------And with that processed reproduction: {action} at UTU:{t}')
