import logging

from .db_functions import run_query

def global_ticker(c,time):
    """
    Increment the time by one. Takes a graph connection `c` and the universal time node `time`.
    """
    # Autoincrement time by one:
    currentTime = time['currentTime'] + 1
    logging.info(f"time was discovered at: {time}")

    
    updateRes = run_query(c, f"g.V().hasLabel('time').property('currentTime', {currentTime}).propperty('updatedFrom','azfunction')")
    logging.info(f"currentTime was updated to: {currentTime}")
