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

@app.route("/clear_session")
def clear():
    session.clear()
    return redirect("/")

# Display pet info
@app.route("/pet", methods=["GET"])
def display():
    if not session.get("fields"):
        print("HEYY")
        categories = db.table("info_categories").select("*").order("id").execute().data
        save_categories(categories)
    pet_id = request.args.get("id")
    data = db.table("information").select("*").eq("pet_id", int(pet_id)).order("cat_id").execute().data
    return render_template("pet.html", id=pet_id, data=data)

@app.route("/create-pet", methods=["POST", "GET"])
def create_pet():
    # Save categories if not yet
    if not session.get("fields"):
        print("HEYY")
        categories = db.table("info_categories").select("*").order("id").execute().data
        save_categories(categories)

    # If POST
    if request.method == "POST":
        # Hash user password
        pwd = request.form.get(str(find_cat_id("Password")))
        hashed_pwd = generate_password_hash(pwd)

        # Insert pet into data, get pet id
        db.table("pets").insert({"pwd": hashed_pwd}).execute()
        pet_id = db.table("pets").select("id").order("id", desc=True).limit(1).execute().data[0]
        
        # Join all info into list of dicts
        data = []
        for cat,val in request.form.items():
            if (cat != str(find_cat_id("Password"))) and (val != ""):
                data.append({"pet_id": pet_id.get("id"), "cat_id": cat, "info": val})
        
        # Add info to database
        db.table("information").insert(data).execute()

        # Save pet id to cookies to create qr
        session["pet_id"] = pet_id.get("id")

        # TODO 2: Call func that creates qr code
        create_qr()

        # TODO 5: Redirect to page that displays qr code with option to download as png (redirect to route in todo 4)
        return redirect("/")
    
    # Go to page
    return render_template("create_pet.html", fields=session["fields"])

# TODO 4: Create a route (return render_template()) to the page that displays qr code (route to qr_display.html in todo 3)