import logging
from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError
import os, yaml, json

import azure.functions as func
from .cmdb_graph import CosmosdbClient
from .validators import ActionValidator

def get_actions():
    if 'actions.yaml' in os.listdir():
        actions = yaml.safe_load(open('actions.yaml'))
    else: 
        actions = yaml.safe_load(open('./getActions/actions.yaml'))
    return actions["actions"]


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('************* Python HTTP trigger function processed a request.')
    
    c = CosmosdbClient()
    logging.info(f'CDB endpoint: {c.endpoint}')
    
    actions = get_actions()
    logging.info(f'total actions available: {len(actions)}')
    logging.info(f'total actions available: {[a["applies_to"] for a in actions]}')

    agent_id = req.params.get('objid')
    

    if agent_id:
        logging.info(f'************* Python HTTP trigger function processed a request. for {agent_id}')
        resp_json = {}
        c.run_query(f"g.V().has('objid','{agent_id}').valueMap()")
        agent = c.clean_nodes(c.res)
        logging.info(f'{agent_id} returns agents: {agent}')

        if len(agent)==0:
            logging.info(f'{agent_id} returns blank agent: {agent}')
            return func.HttpResponse(
                "error: agent not found",
                status_code=200
            )
        if len(agent)>1:
            logging.info(f'{agent_id} returns multiple agents: {agent}')
            return func.HttpResponse(
                "error: duplicate agents",
                status_code=200
            )

        agent = agent[0]
        logging.info(f'{agent_id} returns agent named: {agent.get("name")}')
        validator = ActionValidator(agent,actions)
        valid_actions = validator.validate()
        if len(valid_actions)>0:
            resp_json['actions'] = valid_actions
        else:
            resp_json['error'] = "no actions returned"
            
            

        return func.HttpResponse(json.dumps(resp_json),status_code=200)
    else:
        logging.info(f'req_body is bad: {agent_id}')
        return func.HttpResponse(
             "error: action requires agent",
             status_code=200
        )
    

