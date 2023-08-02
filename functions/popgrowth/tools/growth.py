import pandas as pd
import numpy as np
import logging
import yaml


#importing the libraries from the app
from app.objects import population
from app.functions import language



def grow(c,params):

    def get_faction(objid):
        res = [i for i in factions if i.objid == objid]
        return res[0]
    
    # Get data regarding growth
    global_health_manager = population.Global_Pop_Manager(params,c)
    global_health_manager.get_pop_health()

    pops_df = pd.DataFrame([d['pop'] for d in global_health_manager.data])
    species_df = pd.DataFrame([d['species'] for d in global_health_manager.data])
    locations_df = pd.DataFrame([d['location'] for d in global_health_manager.data])
    factions_df = pd.DataFrame([d['faction'] for d in global_health_manager.data])

    if len(pops_df)==0:
        logging.info(f'**** No pops capable of reproducing ****')
        reproducing_pops = []

    # facilitate the die roll
    else:
        pops_df['roll'] = pops_df['objid'].apply(lambda x: np.random.random())
        pops_df['grow'] = pops_df[['wealth','health']].T.mean() >= pops_df['roll']

        reproducing_pops = pops_df[pops_df['grow']].drop(['roll','grow'],axis=1)

    if len(reproducing_pops)>0:
        
        logging.info(f"{len(reproducing_pops)} of {len(pops_df)} pops will grow")
        species = [population.species.Species(species_df.drop_duplicates().T.to_dict()[i]) for i in  species_df.drop_duplicates().T.to_dict().keys()]
        for i in species:
            global_health_manager.species_dict[i.objid]=i
        factions = [population.Faction(factions_df.drop_duplicates().T.to_dict()[i]) for i in  factions_df.drop_duplicates().T.to_dict().keys()]

        children = []
        events = []
        event_edges = []
        for i in reproducing_pops.index.to_list():
            s = global_health_manager.species_dict[species_df.loc[i].to_dict()['objid']]
            p = reproducing_pops.loc[i].to_dict()
            #adding the current pop as a defautl to the species.
            s.config['defaults'] = p
            f = factions_df.loc[i].to_dict()
            l = locations_df.loc[i].to_dict()
            child = population.Pop(s)
            child.birthplace = l
            child.inhabitsEdge = {"node1": child.objid, "node2": l['objid'], "label": "inhabits"}
            child.name = p['name']+language.make_word(1).lower()
            get_faction(f['objid']).assign_pop_to_faction(child)
            event = global_health_manager.population_growth_event(p,l,child)
            events.append(event)
            event_edges.append({"node1": event['objid'], "node2": l['objid'], "label": "happenedAt"})
            event_edges.append({"node1": p['objid'], "node2": event['objid'], "label": "caused"})
            children.append(child)    

        factionedges = []
        [f.get_pop_edges(factionedges) for f in factions]
        childofEdges = [c.childOf for c in children]
        isOfEdges = [c.isOfSpecies for c in children]
        inhabitsEdges = [c.inhabitsEdge for c in children]

        logging.info(f"Expecting {len(reproducing_pops)} children, got {len(children)}")
        logging.info(f"Expecting event_edges {len(event_edges)} (both caused and happenedAt)")

        data = {"nodes":[c.get_data() for c in children] + events ,"edges":isOfEdges + inhabitsEdges + childofEdges + factionedges + event_edges }
        print(f"The final dataset is {len(data.get('nodes'))} nodes and {len(data.get('edges'))} edges")
        c.upload_data('notebook',data)
    else:
        logging.info(f"zero population growth")

    logging.info(f"**** Growth Complete *****")