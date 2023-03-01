import datetime
import logging
import yaml, pickle
import pandas as pd
import numpy as np

import azure.functions as func
from .cmdb_graph import CosmosdbClient
from .tools import consumption
import os

logger = logging.getLogger('azure.mgmt.resource')



try:
    params = yaml.safe_load(open('settings.yml'))
    syllables = pickle.load(open('syllables.p', "rb"))
except:
    params = yaml.safe_load(open('popgrowth/settings.yml'))
    syllables = pickle.load(open('popgrowth/syllables.p', "rb"))






def main(mytimer: func.TimerRequest) -> None:
    c = CosmosdbClient()
    logging.info(f'CDB endpoint: {c.endpoint}')

    if mytimer.past_due:
        logging.info('The timer is past due!')

    renewables_query = f"""
    g.V().has('label','resource')
            .has('replenish_rate',gt(0)).valuemap()
    """
    c.run_query(renewables_query)
    data = c.clean_nodes(c.res)


    
    logging.info(f"Total resources with the ability to renew: {len(data)}")
    if len(data)>0:
        for r in data:
            c.add_query(f"""
            g.V().has('objid','{r['objid']}').property('volume','{r['volume']+r['replenish_rate']}')
            """)
        c.run_queries()

        logging.info(f'**** resources have been renewed ****')
    else:
        logging.info(f'**** No resources to renew ****')


    ### END 
    logging.info(f'Resource renewal completed')

