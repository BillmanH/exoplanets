def build_homeSystem(data, username):
    accountid = uuid(n=13)
    user = {
        "label": "account",
        "created": datetime.now().strftime("%d-%m-%Y-%H-%M-%S"),
        "objid": accountid,
    }