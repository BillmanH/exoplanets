import azure.functions as func
import datetime
import json
import os
import logging

app = func.FunctionApp()

EVENT_HUB_FULLY_QUALIFIED_NAMESPACE = os.environ.get('EVENT_HUB_FULLY_QUALIFIED_NAMESPACE')
EVENT_HUB_CONNECTION_STR = os.environ.get('EVENT_HUB_CONNECTION_STR')
EVENT_HUB_NAME = os.environ.get('EVENT_HUB_NAME')

@app.function_name(name="EventHubTrigger1")
@app.event_hub_message_trigger(arg_name="event",
                               event_hub_name=EVENT_HUB_NAME,
                               connection="EVENT_HUB_CONNECTION_STR")
def eventGridTest(event: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                event.get_body().decode('utf-8'))

