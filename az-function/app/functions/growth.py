import pandas as pd
import numpy as np
import logging
from app.objects import species
from app.objects import population
from app.functions import language
from app.functions import maths


def calculate_growth(c,t,params):
    # Get data regarding growth
    messages = []
    logging.info(f"EXOADMIN: health requirement {params.get('pop_health_requirement')}")
    healthy_pops_query = f"""
            g.V().has('label','pop')
                .has('health',gt({params.get("pop_health_requirement")})).as('pop')
                .values('objid','health','wealth')
            """
    c.run_query(healthy_pops_query)

    a = np.array(c.res)
    logging.info(f"EXOADMIN: healthy_pops_query {len(a)}")
    if len(a)<=0:
        logging.info(f"EXOADMIN: No pops that meet the pop_health_requirement")
        return messages
    pops_df = pd.DataFrame(np.split(a,len(a)/3),columns=['objid','health','wealth'])
    pops_df[['health','wealth']] = pops_df[['health','wealth']].astype(float)

    # Add random roll to each pop
    pops_df['roll'] = pops_df['objid'].apply(lambda x: np.random.random())
    pops_df['grow'] = pops_df[['wealth','health']].T.mean() >= pops_df['roll']
    reproducing_pops = pops_df[pops_df['grow']].drop(['roll','grow'],axis=1).reset_index(drop=True)


    if len(reproducing_pops)==0:
        logging.info(f'EXOADMIN: **** No pops capable of reproducing ****')
        logging.info(f"EXOADMIN: **** Growth Complete *****")
        return messages
    
    if len(reproducing_pops)>0:
        logging.info(f"{len(reproducing_pops)} of {len(pops_df)} pops will grow")

        for parent_pop in reproducing_pops.to_dict(orient='records'):
            can_grow = check_pop_growth(c, parent_pop)
            if can_grow:
                logging.info(f"EXOADMIN: Growing Pop {parent_pop['objid']}")
                messages.append(get_growth_message(parent_pop))
            if not can_grow:
                logging.info(f"EXOADMIN: Pop {parent_pop['objid']} cannot grow")
        logging.info(f"EXOADMIN: **** Growth Complete *****")
        return messages


def check_pop_growth(c, parent_pop):
    query_pop_cap = f"""
        g.V().has('objid','{parent_pop["objid"]}').out('inhabits').values('objid','name','pop_cap')"
        """
    c.run_query(query_pop_cap)
    pop_cap = c.res
    query_location_pop = f"""
        g.V().has('objid','{parent_pop["objid"]}').out('inhabits').in('inhabits').has('label','pop').count()"
        """
    c.run_query(query_location_pop)
    location_pop = c.res
    over_pop = location_pop[0] > pop_cap[2]
    if not over_pop:
        return True
    else:
        return False

    

def get_growth_message(pop):
    message = {"agent":pop,"action":"reproduce"}
    return message
    
def grow_population(c,t, parent_pop):
    query_pop_species_faction = f"""
            g.V().has('objid','{parent_pop["objid"]}')
                .local(
                    union(
                        out('inhabits').as('location'),
                        out('isOf').as('species'),
                        out('isIn').as('faction')
                        )
                        .fold()).as('pop','location','species','faction')
                    .path()
                    .by(unfold().valueMap().fold())
            """


    c.run_query(query_pop_species_faction)
    # creating some data objects
    pop_dict = c.clean_node(c.res[0]['objects'][0][0])
    loc_dict = c.clean_node(c.res[0]['objects'][1][0])
    sp_dict = c.clean_node(c.res[0]['objects'][1][1])
    fact_dict = c.clean_node(c.res[0]['objects'][1][2])

    # creating the objects
    sp = species.Species(sp_dict)
    sp.config['defaults'] = pop_dict

    # the child
    child = population.Pop(sp)
    child.name = sp.config['defaults']['name']+language.make_word(1).lower()
    child_data = child.get_data()
    child_data['userguid'] = pop_dict['userguid'] 
    
    isIn_edge = child.get_isInFaction()
    isIn_edge['node2'] = fact_dict['objid']
    
    inhabits_edge = {'node1': child.objid, 'node2': loc_dict['objid'], 'label': 'inhabits'}

    data = {"nodes":[child_data] ,"edges":[inhabits_edge,child.isOfSpecies,isIn_edge] }
    c.upload_data(pop_dict['userguid'],data)
    return data


def get_renewal_message(resource):
    message = {"agent":resource,"action":"renew"}
    return message

def calculate_renewal(c,t,params):
    renewing_resources_query =f"""
    g.V().has('label','resource').has('replenish_rate').valuemap()
    """
    c.run_query(renewing_resources_query)
    renewing_resources = c.clean_nodes(c.res)
    messages = []
    for resource in renewing_resources:
        if resource['volume'] < resource['max_volume']:
            messages.append(get_renewal_message(resource))
    return messages

def renew_resource(c,message):
    objid = message['agent']['objid']
    new_volume = message['agent']['volume'] + message['agent']['replenish_rate']
    if new_volume > message['agent']['max_volume']:
        new_volume = message['agent']['max_volume']

    patch_resource_query = f"""
    g.V().has('objid','{objid}').out('has').has('label','resource')
        .property('volume', {new_volume})
    """
    c.run_query(patch_resource_query)
    logging.info(f"EXOADMIN: {message['agent']['name']}:{message['agent']['objid']} increased by {message['agent']['replenish_rate']}, {message['agent']['volume']}-> {new_volume}")
    return None