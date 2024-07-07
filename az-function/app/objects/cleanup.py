import logging

#factions that have no populations
def cleanup_empty_factions(c):
    unpopulated_factions_query = f"""
    g.V().has('label','faction').not(inE('isIn')).count()
    """
    c.run_query(unpopulated_factions_query)
    unpopulated_factions_count = c.res[0]
    logging.info(f"EXOADMIN: factions who have no people: {unpopulated_factions_count}")