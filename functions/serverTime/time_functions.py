import logging
import datetime


def global_ticker(c,time):
    """
    Increment the time by one. Takes a graph connection `c` and the universal time node `time`.
    """
    # Autoincrement time by one:
    currentTime = time['currentTime'] + 1
    logging.info(f"time was discovered at: {time}")

    
    updateRes = c.run_query(f"""g.V().hasLabel('time')
                                .property('currentTime', {currentTime})
                                .property('updatedFrom','azfunction')
                                .property('updatedAt','{str(datetime.datetime.now())}')
                            """
                            )
    logging.info(f"currentTime was updated to: {currentTime}")
 