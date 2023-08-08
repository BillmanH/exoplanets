import datetime
import logging
import yaml, pickle

import azure.functions as func


from .tools import consumption, growth
from .app.connectors import cmdb_graph
from .app.objects import time
from .app.objects import population
from .app.functions import language


logger = logging.getLogger('azure.mgmt.resource')



try:
    params = yaml.safe_load(open('settings.yml'))
    syllables = pickle.load(open('syllables.p', "rb"))
except:
    params = yaml.safe_load(open('popgrowth/settings.yml'))
    syllables = pickle.load(open('popgrowth/syllables.p', "rb"))



def main(mytimer: func.TimerRequest) -> None:
    c = cmdb_graph.CosmosdbClient()
    logging.info(f'CDB endpoint: {c.endpoint}')
    logging.info(f"[param] amount people will suffer by starving: {params['starve_damage']}")
    logging.info(f"[param] amount of health needed to grow: {params['pop_health_requirement']}")
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    

    t = time.Time(c)
    t.get_current_UTU()
    params['currentTime'] = t.params['currentTime']


    consumption.consume(c,params)

    growth.grow(c,params)

    ### END 
    logging.info(f'Population Growth trigger ran at: {utc_timestamp}')

