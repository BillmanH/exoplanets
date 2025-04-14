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
from app.objects import structures
from app.objects import ships
from app.connectors import cmdb_graph
from app.functions import jobs
from app.functions import growth
from app.functions import consumption
from app.functions import cleanup

RUNNING_LOCALLY = False
EVENT_HUB_FULLY_QUALIFIED_NAMESPACE = os.environ.get('EVENT_HUB_FULLY_QUALIFIED_NAMESPACE')
EVENT_HUB_CONNECTION_STR = os.environ.get('EVENT_HUB_CONNECTION_STR')
EVENT_HUB_NAME = os.environ.get('EVENT_HUB_NAME')
#For troubleshooting, making sure the function is the one I think it is. 
function_version_string = "Mar 8"

# func start --functions [a space separated list of functions]
# func start --functions actionResolverTimer resolveActionEvents ututimer

# quick debugging in app insights: 

# union traces
# | union exceptions
# | where timestamp > ago(1d)
# | where message contains "this structure renews the resources of the faction"
# | order by timestamp desc
# | limit 100 

# union traces
# | union exceptions
# | where timestamp > ago(30d)
# | where operation_Id == "ef9ad9f6b1831037fb33480fd5300c1c"
# | order by timestamp asc
# | limit 100 


@app.function_name(name="resolveActionEvents")
@app.event_hub_message_trigger(arg_name="event",
                               event_hub_name=EVENT_HUB_NAME,
                               connection="EVENT_HUB_CONNECTION_STR")
def resolve_action_event(event: func.EventHubEvent):
    logging.info(f'EXOADMIN: <resolveActionEvents> deploy version: {function_version_string}')
    eh_producer = EventHubProducerClient.from_connection_string(EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)
    credential = DefaultAzureCredential() 
    message = ast.literal_eval(event.get_body().decode('utf-8'))
    # proccessing messages is removed so that I can test it locally. 
    outgoing_messages = process_action_event_message(message)
    if len(outgoing_messages)>0:
        logging.info(f"EXOADMIN: produced {len(outgoing_messages)} outgoing messages")
        jobs.send_to_eventhub(outgoing_messages, eh_producer)
        logging.info(f"EXOADMIN: additional messages sent to EH. ")

def process_action_event_message(message):
    c = cmdb_graph.CosmosdbClient()
    t = time.Time(c)
    t.get_current_UTU()
    logging.info(f"EXOADMIN: processing message: {message.get('action')} at UTU:{t}")
    pop_growth_params = yaml.safe_load(open(os.path.join(os.getenv("ABS_PATH"),"app/configurations/populations.yaml")))
    # adding the pop growth params to the time object
    t.pop_growth_params = pop_growth_params
    outgoing_messages = []

    # jobs happen over time, and havev an agent, action, and job (which has weight)
    if 'job' in message.keys():
        action = time.Action(c,message)
        action.add_updates_to_c(t)
        c.upload_data(action.agent['userguid'], action.data)
        if message['job']['actionType'] == "construction":
            logging.info(f"EXOADMIN: 'actionType is construction")
            structures.construct_building(c,message)
        if message['job']['actionType'] == "fabricating":
            logging.info(f"EXOADMIN: 'actionType is fabricating")
            ships.fabricate(c,message)
        logging.info(f"EXOADMIN:       -------And with that processed a JOB: {action} at UTU:{t}")

    # given an object, creates a child object and links it to a parent. 
    if message.get('action')=="reproduce":
        growth.grow_population(c,t, message['agent'])
        logging.info(f"EXOADMIN:       -------And with that processed REPRODUCTION: {message['agent']} at UTU:{t}")

    # Objects that consume the resources of a space that they inhabit.
    if message.get('action')=="consume":
        for resource in message['agent']['consumes']:
            # starving messages are generated when pops don't have resources
            consumption_messages = consumption.consume(c,t,message,resource)
            if consumption_messages:
                outgoing_messages += consumption_messages
        logging.info(f"EXOADMIN:       -------And with that processed CONSUMPTION: {message['agent']} at UTU:{t}")

    # resources that automatically renew. Like organic resources. 
    if message.get('action')=="renew":
        growth.renew_resource(c,message)
        logging.info(f"EXOADMIN:       -------And with that processed RENEWAL: {message['agent']} at UTU:{t}")

    # Update either increases or decreases a specific property of an object
    if message.get('action')=="update":
        growth.renew_resource(c,message)
        logging.info(f"EXOADMIN:       -------And with that processed UPDATE: {message['agent']} at UTU:{t}")

    # individual structure updates
    if message.get('action')=="structure":
        # structures may not have agents. Write the whole message to log. 
        structure_messages = structures.process_structure(c,message)
        if structure_messages:
            outgoing_messages += structure_messages
        logging.info(f"EXOADMIN:       -------And with that processed STRUCTURE: {message} at UTU:{t}")


    # Catchall for messages that are not recognized.
    if (message.get('action') not in ["reproduce","consume","renew","update","structure"])&('job' not in message.keys()):
        logging.info(f"EXOADMIN:       ------- UNKNOWN ACTION NOT PROCESSED: {message['agent']} at UTU:{t}")
    return outgoing_messages

# Generates messages to be resolved asynchronously.
@app.function_name(name="actionResolverTimer")
@app.schedule(schedule="0 */5 * * * *", 
              arg_name="mytimer",
              run_on_startup=RUNNING_LOCALLY) 
def action_resolver(mytimer: func.TimerRequest) -> None:
    logging.info(f'EXOADMIN: <actionResolverTimer> deploy version: {function_version_string}')
    eh_producer = EventHubProducerClient.from_connection_string(EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)
    credential = DefaultAzureCredential() 
    utc_timestamp = datetime.datetime.now(datetime.timezone.utc).replace(
        tzinfo=datetime.timezone.utc).isoformat()
    messages = process_action_messages()
    jobs.send_to_eventhub(messages, eh_producer)
    logging.info('EXOADMIN: Messages Sent Successfully')

def process_action_messages():
    c = cmdb_graph.CosmosdbClient()
    pop_growth_params = yaml.safe_load(open(os.path.join(os.getenv("ABS_PATH"),"app/configurations/populations.yaml")))
    # Establish the time
    t = time.Time(c)
    t.get_current_UTU()
    # Different kinds of EventHub Messages:
    growth_messasges = growth.calculate_growth(c,t,pop_growth_params)
    job_messages = jobs.resolve_jobs(c,t,time.Action)
    consumption_messages = consumption.calculate_consumption(c,t)
    renewal_messages = growth.calculate_renewal(c,t,pop_growth_params)
    logging.info(f'EXOADMIN: messages: job:{len(job_messages)}, growth:{len(growth_messasges)}, consumption:{len(consumption_messages)}, renewal:{len(renewal_messages)} - at: {t}')
    messages = growth_messasges + job_messages + consumption_messages + renewal_messages
    logging.info(f'EXOADMIN: Total Messages generated: {len(messages)} at: {t}')
    return messages

# Faction and building Updates
@app.function_name(name="factionBuildingTimer")
@app.schedule(schedule="0 */10 * * * *", 
              arg_name="mytimer",
              run_on_startup=RUNNING_LOCALLY)
def faction_building_resolver(mytimer: func.TimerRequest) -> None:
    logging.info(f'EXOADMIN: <faction_building_resolver> deploy version: {function_version_string}')
    eh_producer = EventHubProducerClient.from_connection_string(EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)
    credential = DefaultAzureCredential()
    utc_timestamp = datetime.datetime.now(datetime.timezone.utc).replace(
        tzinfo=datetime.timezone.utc).isoformat()
    messages = get_structure_messages()
    jobs.send_to_eventhub(messages, eh_producer)
    logging.info('EXOADMIN: Messages Sent Successfully')
    
def get_structure_messages():
    c = cmdb_graph.CosmosdbClient()
    # Establish the time
    t = time.Time(c)
    t.get_current_UTU()
    t.building_params = yaml.safe_load(open(os.path.join(os.getenv("ABS_PATH"),"app/configurations/buildings.yaml")))
    # getting the list of structures that can take actions:
    messages = structures.get_faction_pop_structures(c)
    logging.info(f'EXOADMIN: Total Messages generated: {len(messages)} at: {t}')
    return messages

# UTU is the universal time unit
@app.function_name(name="cleanup")
@app.schedule(schedule="0 0 */2 * * *", 
              arg_name="mytimer",
              run_on_startup=RUNNING_LOCALLY) 
def utu_timer(mytimer: func.TimerRequest) -> None:
    logging.info(f'EXOADMIN: <cleanup> deploy version: {function_version_string}')
    c = cmdb_graph.CosmosdbClient()
    cleanup.cleanup_empty_factions(c)

# UTU is the universal time unit
@app.function_name(name="ututimer")
@app.schedule(schedule="0 */5 * * * *", 
              arg_name="mytimer",
              run_on_startup=RUNNING_LOCALLY) 
def utu_timer(mytimer: func.TimerRequest) -> None:
    logging.info(f'EXOADMIN: <ututimer> deploy version: {function_version_string}')
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    increment_timer()

def increment_timer():
    c = cmdb_graph.CosmosdbClient()
    t = time.Time(c)
    t.get_current_UTU()
    r = t.global_ticker()
    logging.info(f'EXOADMIN: UTU was updated, result: {r} at: {t}')

