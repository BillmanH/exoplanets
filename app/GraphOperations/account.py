
def drop_account(client,userid):
    query = f"g.V().has('username','{userid}').drop()"
    client.run_query(query)