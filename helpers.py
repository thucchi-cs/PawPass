from datetime import date
from flask import redirect, session, flash
from functools import wraps
from werkzeug.security import check_password_hash

def secret_key():
    import secrets
    print(secrets.token_hex(32))

def find_cat_id(cat, fields):
    for f in fields:
        if f["category"] == cat:
            return f["id"]
    return -1

def find_id_cat(id, fields):
    for f in fields:
        if f["id"] == id:
            return f["category"]
    return -1
