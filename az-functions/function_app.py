import azure.functions as func
import os
import datetime
import json
import logging

app = func.FunctionApp()


@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name=os.getenv("EVENT_HUB_NAME"),
                               connection="EVENT_HUB_CONNECTION_STR")
def myFunction(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))
