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
#For troubleshooting, making sure the function is the one I think it is. 
function_version_string = "sunday hackathon"

# func start --functions [a space separated list of functions]
# func start --functions actionResolverTimer resolveActionEvents ututimer

@app.function_name(name="resolveActionEvents")
@app.event_hub_message_trigger(arg_name="event",
                               event_hub_name=EVENT_HUB_NAME,
                               connection="EVENT_HUB_CONNECTION_STR")
def resolve_action_event(event: func.EventHubEvent):
    logging.info(f'EXOADMIN: function deploy version: {function_version_string}')
    eh_producer = EventHubProducerClient.from_connection_string(EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)
    credential = DefaultAzureCredential() 
    message = ast.literal_eval(event.get_body().decode('utf-8'))
    c = cmdb_graph.CosmosdbClient()
    t = time.Time(c)
    t.get_current_UTU()
    logging.info(f"EXOADMIN: processing message: {message.get('action')} at UTU:{t}")
    pop_growth_params = yaml.safe_load(open(os.path.join(os.getenv("ABS_PATH"),"app/configurations/popgrowthconfig.yaml")))
    # adding the pop growth params to the time object
    t.pop_growth_params = pop_growth_params
    outgoing_messages = []

    # jobs happen over take time, and havev an agent, action, and job (which has weight)
    if 'job' in message.keys():
        action = time.Action(c,message)
        action.add_updates_to_c(t)
        c.upload_data(action.agent['userguid'], action.data)
        logging.info(f"EXOADMIN:       -------And with that processed a JOB: {action} at UTU:{t}")

    # given an object, creates a child object and links it to a parent. 
    if message.get('action')=="reproduce":
        growth.grow_population(c,t, message['agent'])
        logging.info(f"EXOADMIN:       -------And with that processed REPRODUCTION: {message['agent']} at UTU:{t}")

    # Objects that consume the resources of a space that they inhabit.
    if message.get('action')=="consume":
        for resource in message['agent']['consumes']:
            # starving messages are generated when pops don't have resources
            outgoing_messages += consumption.reduce_location_resource(c,t,message,resource)
        logging.info(f"EXOADMIN:       -------And with that processed CONSUMPTION: {message['agent']} at UTU:{t}")

    # resources that automatically renew. Like organic resources. 
    if message.get('action')=="renew":
        growth.renew_resource(c,message)
        logging.info(f"EXOADMIN:       -------And with that processed RENEWAL: {message['agent']} at UTU:{t}")

    # Update either increases or decreases a specific property of an object
    if message.get('action')=="update":
        growth.renew_resource(c,message)
        logging.info(f"EXOADMIN:       -------And with that processed UPDATE: {message['agent']} at UTU:{t}")

    # Catchall for messages that are not recognized.
    if message.get('action') not in ["reproduce","consume","renew","update"]:
        logging.info(f"EXOADMIN:       ------- UNKNOWN ACTION NOT PROCESSED: {message['agent']} at UTU:{t}")

    if outgoing_messages>0:
        logging.info(f"EXOADMIN: produced {len(outgoing_messages)} outgoing messages")
        jobs.send_to_eventhub(outgoing_messages, eh_producer)
        logging.info(f"EXOADMIN: additional messages sent to EH. ")



# Generates messages to be resolved asynchronously.
@app.function_name(name="actionResolverTimer")
@app.schedule(schedule="0 */5 * * * *", 
              arg_name="mytimer",
              run_on_startup=RUNNING_LOCALLY) 
def action_resolver(mytimer: func.TimerRequest) -> None:
    logging.info(f'EXOADMIN: function deploy version: {function_version_string}')
    eh_producer = EventHubProducerClient.from_connection_string(EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)
    credential = DefaultAzureCredential() 
    utc_timestamp = datetime.datetime.now(datetime.timezone.utc).replace(
        tzinfo=datetime.timezone.utc).isoformat()
    c = cmdb_graph.CosmosdbClient()
    pop_growth_params = yaml.safe_load(open(os.path.join(os.getenv("ABS_PATH"),"app/configurations/popgrowthconfig.yaml")))
    # Establish the time
    t = time.Time(c)
    t.get_current_UTU()

    # Different kinds of EventHub Messages:
    growth_messasges = growth.calculate_growth(c,t,pop_growth_params)
    job_messages = jobs.resolve_jobs(c,t,time.Action)
    consumption_messages = consumption.calculate_consumption(c,t)
    renewal_messages = growth.calculate_renewal(c,t,pop_growth_params)
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
    logging.info(f'EXOADMIN: function deploy version: {function_version_string}')
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    if mytimer.past_due:
        logging.info('EXOADMIN: The timer is past due!')
    c = cmdb_graph.CosmosdbClient()
    t = time.Time(c)
    t.get_current_UTU()
    r = t.global_ticker()
    logging.info(f'EXOADMIN: UTU was updated, result: {r} at: {t}')

