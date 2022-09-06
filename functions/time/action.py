import logging

from .db_functions import run_query, clean_node

def validate_action(time,a):
    '''
    validate that the time to complete the task has passed. 
    Not the same as validation that the action can be taken. 
    If the `takingAction` edge has been applied to the agent `a`, then it is just a check of time completed. 
    '''

    if int(a['weight']) < int(time['currentTime']):
        return True
    else:
        return False

def get_global_actions(c):
    """
    Retrieve a list of the global actions.
    """
    # Autoincrement time by one:
    actions_query = """
    g.E().haslabel('takingAction').has('status','pending').as('job')
        .outV().as('agent').path().by(valueMap())
    """
    
    actions = run_query(c, actions_query)
    # Clenup the query results:    
    act = []
    for action in actions:
        lab = {}
        for itr,itm in enumerate(action['labels']):
            lab[itm[0]] = clean_node(action['objects'][itr])
        act.append(lab)


    logging.info(f"number of pending actions found: {len(act)}")
    return act


def augments_self_properties(a,j):
    """
    builds the query that updates the object according to the properties that it has. 
    takes an agent `a` and a job `j`.
    requires that job has, for example, 'augments_self_properties': 'faction_loyalty,literacy,aggression;0.05,0.01,0.05'
    """
    patched_properties = j['augments_self_properties'].split(";")[0].split(",")
    patched_values = [float(f) for f in j['augments_self_properties'].split(";")[1].split(",")]

    # creating a dict of the new, patched values
    new_a = {}
    for itr,itm in enumerate(patched_properties):
        new_a[itm] = round(a[itm]+patched_values[itr], 4)

    # building the update query
    query = f"g.V().has('objid','{a['objid']}')"
    for n in new_a.keys():
        query += f".property('{n}',{new_a[n]})"

    logging.info(f"patch query: {query}")
    return query
