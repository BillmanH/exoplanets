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
    if len(a)>=0:
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
            logging.info(f"EXOADMIN: Growing Pop {parent_pop['objid']}")
            messages.append(get_growth_message(parent_pop))
        logging.info(f"EXOADMIN: **** Growth Complete *****")
        return messages

    

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

    event = population_growth_event(t,pop_dict,loc_dict,child)
    event_edge = {'node1': child.objid, 'node2': event['objid'], 'label': 'caused'}

    data = {"nodes":[child_data, event] ,"edges":[inhabits_edge,child.isOfSpecies,isIn_edge,event_edge] }
    c.upload_data(pop_dict['userguid'],data)
    return data


def population_growth_event(t,parent,location,child):
    node = {
        'objid':maths.uuid(),
        'name':'population growth',
        'label':'event',
        'text': f"The population ({parent['name']}) inhabiting {location['name']} has grown to produce the population: {child.name}.",
        'visibleTo':parent['userguid'],
        'time':t.params['currentTime'],
        'userguid':parent['userguid'],
        'source':'notebook'
    }
    return node