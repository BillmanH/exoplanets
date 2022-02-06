from datetime import datetime

from . import maths

def create_account(username):
    user = {
        "label": "account",
        "created": datetime.now().strftime("%d-%m-%Y-%H-%M-%S"),
        "objid":  maths.uuid(n=13),
        "name": username
    }
    return user