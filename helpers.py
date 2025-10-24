from datetime import date
from flask import redirect, session, flash
from functools import wraps

def secret_key():
    import secrets
    print(secrets.token_hex(32))

def find_cat_id(cat):
    for id,value in session.get("fields", {}).items():
        if value["name"] == cat:
            return id
    return -1

def match_categories(data, categories):
    # for d in data:
    #     cat = find_id_cat(d["cat_id"], categories)
    pass

def save_categories(categories):
    fields = {}
    for c in categories:
        fields[c["id"]] = {"name": c["category"], "req": c["req"], "descr": c["descr"]}
    session["fields"] = fields

# TODO 1: Create the qr code to url
def create_qr():
    # Url to .../pet?id=...
    # id is saved in session["pet_id"]
    pass