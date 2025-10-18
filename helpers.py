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