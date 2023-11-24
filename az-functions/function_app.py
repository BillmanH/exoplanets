import azure.functions as func
import os
import datetime
import json
import logging

app = func.FunctionApp()


@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="EXO_TIME",
                               connection="EVENT_HUB_CONNECTION_STR")
def eh_update_time(azeventhub: func.EventHubEvent):
    logging.info('Time Event Was triggered: %s',
                azeventhub.get_body().decode('utf-8'))


@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="EXO_ACTION",
                               connection="EVENT_HUB_CONNECTION_STR")
def eh_resolve_action(azeventhub: func.EventHubEvent):
    logging.info('Action Event was triggered: %s',
                azeventhub.get_body().decode('utf-8'))
 