from flask import Flask, render_template, redirect, request, flash, session, jsonify
from supabase import create_client, Client
from helpers import *
import os
import dotenv

# Load env variables
dotenv.load_dotenv()

# Set up Flask
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
# flask run --debug

# Set up web app
app.config.update(
    SECRET_KEY=os.environ.get("FLASK_SECRET_KEY"),
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True
)
# Session(app)

# Set up database
db_url = os.environ.get("DB_URL")
db_key = os.environ.get("DB_KEY")
db: Client = create_client(db_url, db_key)

# Website homepage
@app.route("/")
def index():
    return render_template("index.html")
