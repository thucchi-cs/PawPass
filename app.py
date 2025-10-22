from flask import Flask, render_template, redirect, request, flash, session, jsonify
from supabase import create_client, Client
from werkzeug.security import generate_password_hash
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

@app.route("/create-pet", methods=["POST", "GET"])
def create_pet1():
    # Query all categories of info
    fields = db.table("info_categories").select("*").order("id").execute().data

    # If POST
    if request.method == "POST":
        # Hash user password
        pwd = request.form.get(str(find_cat_id("Password", fields)))
        hashed_pwd = generate_password_hash(pwd)

        # Insert pet into data, get pet id
        db.table("pets").insert({"pwd": hashed_pwd}).execute()
        pet_id = db.table("pets").select("id").order("id", desc=True).limit(1).execute().data[0]
        
        # Join all info into list of dicts
        data = []
        for cat,val in request.form.items():
            if (cat != str(find_cat_id("Password", fields))) and (val != ""):
                data.append({"pet_id": pet_id.get("id"), "cat_id": cat, "info": val})
        
        # Add info to database
        db.table("information").insert(data).execute()

        # Return to homepage
        return redirect("/")
    
    # Go to page
    return render_template("create_pet.html", fields=fields)