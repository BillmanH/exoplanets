# Libraries that should exist in azure
import azure.functions as func
from azure.eventhub.aio import EventHubProducerClient
from azure.identity.aio import DefaultAzureCredential

# core components that make functions work
import logging
app = func.FunctionApp()

import datetime
import ast
import os
import yaml

# I should be able to pull the modules from the same libraries as the game iteself. 
from app.objects import time
from app.connectors import cmdb_graph
from app.functions import jobs
from app.functions import growth
from app.functions import consumption


RUNNING_LOCALLY = False
EVENT_HUB_FULLY_QUALIFIED_NAMESPACE = os.environ.get('EVENT_HUB_FULLY_QUALIFIED_NAMESPACE')
EVENT_HUB_CONNECTION_STR = os.environ.get('EVENT_HUB_CONNECTION_STR')
EVENT_HUB_NAME = os.environ.get('EVENT_HUB_NAME')


# func start --functions [a space separated list of functions]
# func start --functions actionResolverTimer resolveActionEvents ututimer

@app.function_name(name="resolveActionEvents")
@app.event_hub_message_trigger(arg_name="event",
                               event_hub_name=EVENT_HUB_NAME,
                               connection="EVENT_HUB_CONNECTION_STR")
def resolve_action_event(event: func.EventHubEvent):
    message = ast.literal_eval(event.get_body().decode('utf-8'))
    logging.info(f'EXOADMIN: Python EventHub trigger processed an messasge: {message} : {type(message)}')
    c = cmdb_graph.CosmosdbClient()
    t = time.Time(c)
    t.get_current_UTU()
    logging.info(f"EXOADMIN: processing message: {message.get('action')} at UTU:{t}")
    if 'job' in message.keys():
        action = time.Action(c,message)
        action.add_updates_to_c(t)
        c.upload_data(action.agent['userguid'], action.data)
        logging.info(f"EXOADMIN:       -------And with that processed a JOB: {action} at UTU:{t}")
    if message.get('action')=="reproduce":
        growth.grow_population(c,t, message['agent'])
        logging.info(f"EXOADMIN:       -------And with that processed REPRODUCTION: {message['agent']} at UTU:{t}")
    if message.get('action')=="consume":
        for resource in message['agent']['consumes']:
            consumption.reduce_location_resource(c,message,resource)
        logging.info(f"EXOADMIN:       -------And with that processed CONSUMPTION: {message['agent']} at UTU:{t}")
    if message.get('action')=="renew":
        growth.renew_resource(c,t,message)
        logging.info(f"EXOADMIN:       -------And with that processed RENEWAL: {message['agent']} at UTU:{t}")
        
        

# Check the open actions and resolve them
@app.function_name(name="actionResolverTimer")
@app.schedule(schedule="0 */5 * * * *", 
              arg_name="mytimer",
              run_on_startup=RUNNING_LOCALLY) 
def action_resolver(mytimer: func.TimerRequest) -> None:
    eh_producer = EventHubProducerClient.from_connection_string(EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)
    credential = DefaultAzureCredential() 
    utc_timestamp = datetime.datetime.now(datetime.timezone.utc).replace(
        tzinfo=datetime.timezone.utc).isoformat()
    c = cmdb_graph.CosmosdbClient()
    params = yaml.safe_load(open(os.path.join(os.getenv("ABS_PATH"),"app/configurations/popgrowthconfig.yaml")))
    # Establish the time
    t = time.Time(c)
    t.get_current_UTU()

    growth_messasges = growth.calculate_growth(c,t,params)
    job_messages = jobs.resolve_jobs(c,t,time.Action)
    consumption_messages = consumption.calculate_consumption(c,t)
    renewal_messages = growth.calculate_renewal(c,t,params)
    messages = growth_messasges + job_messages + consumption_messages + renewal_messages
    jobs.send_to_eventhub(messages, eh_producer)
    logging.info(f'EXOADMIN: messages: job:{len(job_messages)}, growth:{len(growth_messasges)}, consumption:{len(consumption_messages)}, renewal:{len(renewal_messages)} - at: {t}')
    logging.info(f'EXOADMIN: Total Messages sent to EH: {len(messages)} at: {t}')

# UTU is the universal time unit
@app.function_name(name="ututimer")
@app.schedule(schedule="0 */5 * * * *", 
              arg_name="mytimer",
              run_on_startup=RUNNING_LOCALLY) 
def utu_timer(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    if mytimer.past_due:
        logging.info('EXOADMIN: The timer is past due!')
    c = cmdb_graph.CosmosdbClient()
    t = time.Time(c)
    t.get_current_UTU()
    r = t.global_ticker()
    logging.info(f'EXOADMIN: UTU was updated, result: {r} at: {t}')

