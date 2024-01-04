import azure.functions as func
import os
import datetime
import json
import logging

# from connector import cmdb_graph as cmdb
# from utu_time import timemanager as tm

app = func.FunctionApp()


@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="EXO_TIME",
                               connection="EVENT_HUB_CONNECTION_STR")
def eh_update_time(azeventhub: func.EventHubEvent):
    # Call the time module that gets and updates the time (increment by one)
    c = cmdb.CosmosdbClient()
    tm.update_time(c)
    logging.info('Time Event Was triggered: %s',
                azeventhub.get_body().decode('utf-8'))
    
 

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="EXO_ACTION",
                               connection="EVENT_HUB_CONNECTION_STR")
def eh_resolve_action(azeventhub: func.EventHubEvent):
    logging.info('Action Event was triggered: %s',
                azeventhub.get_body().decode ('utf-8'))
 
