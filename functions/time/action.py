import logging

from .db_functions import run_query

def get_global_actions(c):
    """
    Retrieve a list of the global actions.
    """
    # Autoincrement time by one:
    query_actions = """
    g.E().haslabel('pending').as('status')
    .outV().as('agent')
    .outE('hasAction').as('completed')
    .inV().as('action')
    .outE('takingAction').as('completed')
    .inV().as('time')
        .path()
        .by(valueMap())
    """
    
    updateRes = run_query(c, f"g.V().hasLabel('time').property('currentTime', {currentTime}).property('updatedFrom','azfunction')")
    logging.info(f"currentTime was updated to: {currentTime}")
