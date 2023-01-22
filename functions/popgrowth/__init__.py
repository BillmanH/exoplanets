import datetime
import logging
import yaml, pickle
import pandas as pd
import numpy as np

import azure.functions as func
from .cmdb_graph import CosmosdbClient
from .time_functions import global_ticker


params = yaml.safe_load(open('settings.yaml'))
syllables = pickle.load(open('syllables.p'), "rb")


logger = logging.getLogger('azure.mgmt.resource')

def uuid(n=13):
    return "".join([str(i) for i in np.random.choice(range(10), n)])

def make_word(n):
    syl = np.random.choice(syllables, n)
    word = "".join(syl)
    return word.capitalize()

changing_values = ['conformity','literacy','aggression','constitution','wealth','factionLoyalty']


def grow_pop(p,species):
    child = p.copy()
    child['name'] = child['name']+make_word(1).lower()
    id = uuid()
    child['objid'] = id
    child['id'] = id
    child['isIdle'] = 'False'
    child['health'] = np.round(child['health']*.6,3)
    child['wealth'] = np.round(child['wealth']*.6,3)
    child['industry'] = np.round(child['industry']*.6,3)
    for v in params['changing_values']:
        child[v] = np.round(child[v] + np.random.uniform(low=-.1, high=.1),3)
    return child



def main(mytimer: func.TimerRequest) -> None:
    c = CosmosdbClient()
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    healthy_pops_query = f"""
    g.V().has('label','pop')
        .has('health',gt({params['pop_health_requirement']})).as('pop')
        .local(
            union(
                out('enhabits').as('location'),
                out('isOfSpecies').as('species')
                )
                .fold()).as('location','species')
            .path()
            .by(unfold().valueMap().fold())
    """
    c.run_query(healthy_pops_query)
    data = c.reduce_res(c.res)

    
    pops_df = pd.DataFrame([d['pop'] for d in data])
    species_df = pd.DataFrame([d['species'] for d in data])
    locations_df = pd.DataFrame([d['location'] for d in data])

    logging.info("Total pops loaded: ",len(pops_df))

    pops_df['roll'] = pops_df['objid'].apply(lambda x: np.random.random())
    pops_df['grow'] = pops_df[['wealth','health']].T.mean() >= pops_df['roll']

    reproducing_pops = pops_df[pops_df['grow']].drop(['roll','grow'],axis=1)
    logging.info("Total reproducing pops: ",len(reproducing_pops))


    nodes = []
    edges = []

    for i in reproducing_pops.index.to_list():
        p = reproducing_pops.loc[i].to_dict()
        species = species_df.loc[i].to_dict()
        child = grow_pop(p,species)
        nodes.append(child)
        edges.append({"node1": child["objid"], "node2": p["objid"], "label": "childOf"})
        edges.append({"node1": child["objid"], "node2": child["isInFaction"], "label": "isInFaction"})
        edges.append({"node1": child["objid"], "node2": species["objid"], "label": "isOfSpecies"})
        
    upload_data = {'nodes':nodes,'edges':edges}
    c.upload_data()
    ### END 
    logging.info(f'Population Growth trigger ran at: {utc_timestamp}')
    c.close()
