import azure.functions as func
import datetime
import json
import ast
import os
import logging

from components import actions
from components import cmdb_graph
from components import time
app = func.FunctionApp()


EVENT_HUB_FULLY_QUALIFIED_NAMESPACE = os.environ.get('EVENT_HUB_FULLY_QUALIFIED_NAMESPACE')
EVENT_HUB_CONNECTION_STR = os.environ.get('EVENT_HUB_CONNECTION_STR')
EVENT_HUB_NAME = os.environ.get('EVENT_HUB_NAME')

@app.function_name(name="resolveActionEvents")
@app.event_hub_message_trigger(arg_name="event",
                               event_hub_name=EVENT_HUB_NAME,
                               connection="EVENT_HUB_CONNECTION_STR")
def eventGridTest(event: func.EventHubEvent):
    message = ast.literal_eval(event.get_body().decode('utf-8'))
    logging.info(f'Python EventHub trigger processed an messasge: {message} : {type(message)}')
    c = cmdb_graph.CosmosdbClient()
    t = time.Time(c)
    t.get_current_UTU()
    action = actions.Action(c,message)
    action.add_updates_to_c(t)
    c.upload_data(action.agent['userguid'], action.data)
    logging.info(f'      -------And with that processed an action: {action} at UTU:{t}')

