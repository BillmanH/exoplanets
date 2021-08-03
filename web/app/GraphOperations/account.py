
def drop_account(client,userid):
    query = f"g.V().has('username','{userid}').drop()"
    callback = client.submitAsync(query)
    res = callback.result().all().result()
    return res