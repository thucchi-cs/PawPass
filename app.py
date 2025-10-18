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
    data = db.table("test").select("*").execute().data
    print(data)
    return render_template("index.html")

@app.route("/create-pet-1", methods=["POST", "GET"])
def create_pet1():
    if request.method == "POST":
        start_creating_pet()
        return redirect("create-pet-2")
    fields = db.table("pets").select("*").eq("id", 1).execute().data[0]
    print(fields)
    return render_template("create_pet.html", stage=1,fields=fields)

@app.route("/create-pet-2", methods=["POST", "GET"])
@creating_required
def create_pet2():
    if request.method == "POST":
        cancel_creating_pet()
        return redirect("/")
    fields = db.table("additional_info").select("*").eq("pet_id",1).execute().data[0]
    return render_template("create_pet.html", stage=2,fields=fields)

@app.route("/cancel_creation", methods=["POST"])
def cancel():
    cancel_creating_pet()
    return redirect("/")