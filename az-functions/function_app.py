import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="myfunc", auth_level=func.AuthLevel.FUNCTION)
def myfunc(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="exo-game-loop",
                               connection="Endpoint=sb://exo-jobs.servicebus.windows.net/;SharedAccessKeyName=exo-engine;SharedAccessKey=SV8PLOLmTa7FQ9dGt0wpksShm9dBkFSYM+AEhNb7IC0=") 
def myFunction(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))
