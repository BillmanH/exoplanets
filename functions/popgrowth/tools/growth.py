import pandas as pd
import numpy as np
import logging
import yaml


def uuid(n=13):
    return "".join([str(i) for i in np.random.choice(range(10), n)])

def make_word(n, syllables):
    syl = np.random.choice(syllables, n)
    word = "".join(syl)
    return word.capitalize()


def population_growth_event(p,location,child, params):
    node = {
        'objid':uuid(),
        'name':'population growth',
        'label':'event',
        'text': f"The population ({p['name']}) inhabiting {location['name']} has grown to produce the population: {child['name']}.",
        'visibleTo':p['username'],
        'time':params['time']['currentTime']
    }
    # logging.info(node)
    return node


def grow_pop(p,species,params,syllables):
    child = p.copy()
    child['foundedTime']:params['time']['currentTime'] 
    child['label'] = 'pop'
    child['name'] = child['name']+make_word(1,syllables).lower()
    id = uuid()
    child['objid'] = id
    child['id'] = id
    child['isIdle'] = 'true'
    child['health'] = np.round(child['health']*.6,3)
    child['wealth'] = np.round(child['wealth']*.6,3)
    child['industry'] = np.round(child['industry']*.6,3)
    for v in params['changing_values']:
        child[v] = np.round(child[v] + np.random.uniform(low=-.1, high=.1),3)
    return child

def get_pop_health(c,params):
    healthy_pops_query = f"""
    g.V().has('label','pop')
        .has('health',gt({params['pop_health_requirement']})).as('pop')
        .local(
            union(
                out('inhabits').as('location'),
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

    return pops_df,species_df,locations_df



def grow(c,params,syllables):
    # Get data regarding growth
    pops_df,species_df,locations_df = get_pop_health(c,params)
    logging.info(f"Total pops who could grow: {len(pops_df)}")

    if len(pops_df)==0:
        logging.info(f'**** No pops capable of reproducing ****')
        reproducing_pops = []

    # facilitate the die roll
    else:
        pops_df['roll'] = pops_df['objid'].apply(lambda x: np.random.random())
        pops_df['grow'] = pops_df[['wealth','health']].T.mean() >= pops_df['roll']

        reproducing_pops = pops_df[pops_df['grow']].drop(['roll','grow'],axis=1)
        logging.info(f"Total reproducing pops: {len(reproducing_pops)}")
    
    if len(reproducing_pops)>0:
        nodes = []
        edges = []
        # Event edges must be uploaded separately, because the event nodes haven't been created yet.    
        event_edges = []
        # now we grow each pop
        for i in reproducing_pops.index.to_list():
            p = reproducing_pops.loc[i].to_dict()
            species = species_df.loc[i].to_dict()
            location = locations_df.loc[i].to_dict()
            child = grow_pop(p,species,params,syllables)
            nodes.append(child)
            event = population_growth_event(p, location,child, params)
            nodes.append(event)
            edges.append({"node1": child["objid"], "node2": p["objid"], "label": "childOf"})
            edges.append({"node1": child["objid"], "node2": child["isInFaction"], "label": "isInFaction"})
            edges.append({"node1": child["objid"], "node2": species["objid"], "label": "isOfSpecies"})
            edges.append({"node1": child["objid"], "node2": location["objid"], "label": "inhabits"})
            event_edges.append(c.create_custom_edge(event,location,'happenedAt'))
            event_edges.append(c.create_custom_edge(p,event,'caused'))
        upload_data = {'nodes':nodes,'edges':edges}
        c.upload_data(upload_data)
        for e in event_edges:
            c.add_query(e)
        c.run_queries()
    else:
        logging.info(f"zero population growth")