import logging

from .db_functions import run_query

def get_global_actions(c):
    """
    Retrieve a list of the global actions.
    """
    # Autoincrement time by one:
    actions_query = """
    g.E().haslabel('takingAction').has('status','pending').as('job')
        .outV().as('agent').path().by(valueMap())
    """
    
    actions = run_query(actions_query)
    # Clenup the query results:    
    act = []
    for action in actions:
        lab = {}
        for itr,itm in enumerate(action['labels']):
            lab[itm[0]] = db.clean_node(action['objects'][itr])
        act.append(lab)
        

    logging.info(f"currentTime was updated to: {currentTime}")
