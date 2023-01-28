import logging
from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError
import os, yaml

import azure.functions as func
from .cmdb_graph import CosmosdbClient
from .validators import ActionValidator


if 'actions.yaml' in os.listdir():
    actions = yaml.safe_load('./actions.py')
else: 
    actions = yaml.safe_load('getActions/actions.py')


def main(req: func.HttpRequest) -> func.HttpResponse:
    c = CosmosdbClient()
    logging.info('************* Python HTTP trigger function processed a request.')
    logging.info(f'CDB endpoint: {c.endpoint}')
    

    req_body = req.get_json()
    request = req_body.get('agent')
    

    if request:
        logging.info('************* Python HTTP trigger function processed a request.')
        resp_json = {}
        c.run_query(f"g.V().has('objid','{request.get('objid')}')")
        agent = c.clean_node(c.res)
        validator = ActionValidator(agent,actions)
        valid_actions = validator.validate()
        if len(valid_actions)>0:
            resp_json['actions'] = valid_actions
        else:
            resp_json['error'] = "no actions returned"
            
        func.HttpResponse(resp_json)
            

        return func.HttpResponse(resp_json)
    else:
        logging.info(f'req_body is bad: {req_body}')
        return func.HttpResponse(
             "error: action requires agent"
             status_code=200
        )
    

