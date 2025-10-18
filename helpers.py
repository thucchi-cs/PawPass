from datetime import date
from flask import redirect, session, flash
from functools import wraps
from werkzeug.security import check_password_hash


def secret_key():
    import secrets
    print(secrets.token_hex(32))

def start_creating_pet():
    session["creating"] = True

def cancel_creating_pet():
    session["creating"] = False

def assign_pet_id(id):
    session["pet_id"] = id

def creating_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("creating"):
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function