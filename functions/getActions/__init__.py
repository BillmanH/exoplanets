import logging
from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError
import os, yaml

import azure.functions as func
from .cmdb_graph import CosmosdbClient

if 'actions.yaml' in os.listdir():
    actions = yaml.safe_load('./actions.py')
else: 
    actions = yaml.safe_load('getActions/actions.py')


def main(req: func.HttpRequest) -> func.HttpResponse:
    c = CosmosdbClient()
    logging.info('************* Python HTTP trigger function processed a request.')
    logging.info(f'CDB endpoint: {c.endpoint}')
    

    req_body = req.get_json()
    name = req_body.get('name')
    

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
