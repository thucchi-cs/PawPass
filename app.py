from flask import Flask, render_template, redirect, request, flash, session, jsonify, send_file
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import *
import os
import dotenv

# Load env variables
dotenv.load_dotenv()

# Set up Flask
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
# flask run --debug

# Set up jinja filters
app.jinja_env.filters["str"] = str
app.jinja_env.filters["int"] = int
app.jinja_env.filters["cap"] = cap

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

# Debug only: clear session
@app.route("/clear_session")
def clear():
    session.clear()
    return redirect("/")

# Display pet info
@app.route("/pet", methods=["GET"])
def display():
    # Save categories if not yet
    if not session.get("fields"):
        categories = db.table("info_categories").select("*").order("id").execute().data
        save_categories(categories)

    # Get data of pet to display
    pet_id = request.args.get("id")
    data = db.table("information").select("*").eq("pet_id", int(pet_id)).order("cat_id").execute().data
    print(session["fields"])
    # Go to display page
    return render_template("pet.html", id=pet_id, data=data, fields=session["fields"])

# Edit pet
@app.route("/edit-pet", methods=["POST", "GET"])
def edit_pet():
    # Save categories if not yet
    if not session.get("fields"):
        categories = db.table("info_categories").select("*").order("id").execute().data
        save_categories(categories)
    
    # Get url parameters if any
    arg_id = request.args.get("id")

    # 1st page
    if not arg_id:
        # If submit
        if request.method == "POST":
            # Get user input
            id = request.form.get("id")
            pwd = request.form.get("password")

            # Check if pet is in db
            pet = db.table("pets").select("*").eq("id", int(id)).execute().data
            if len(pet) < 1:
                flash("Invalid id")
                return redirect("/edit-pet")
            pet = pet[0]

            # Check password
            if not check_password_hash(pet["pwd"], pwd):
                flash("Incorrect password")
                return redirect("/edit-pet")

            return redirect(f"/edit-pet?id={id}")

        # Go to page
        print("get 1")
        return render_template("edit_pet.html", stage=1)
    
    # 2nd page
    else:
        # If submit
        if request.method == "POST":
            # Delete all existing data of pet
            db.table("information").delete().eq("pet_id", int(arg_id)).execute()

            # Join all info into list of dicts
            data = []
            for cat,val in request.form.items():
                if (val != ""):
                    data.append({"pet_id": int(arg_id), "cat_id": cat, "info": val})   

            # Add new data to db
            db.table("information").insert(data).execute()         

            print("post 2")
            return redirect("/create-qr")

        # Get pet data
        data = db.table("information").select("*").eq("pet_id", int(arg_id)).execute().data

        # Save pet id to cookies to create qr
        session["pet_id"] = int(arg_id)

        # Create qr code of pet
        create_qr()

        # Create readable dict of data
        info = {}
        for d in data:
            cat_id = str(d["cat_id"])
            info[cat_id] = d["info"]

        # Go to page
        print("get 2")
        print(info)
        return render_template("edit_pet.html", stage=2, id=arg_id, fields=session["fields"], info=info)        

# Create pet
@app.route("/create-pet", methods=["POST", "GET"])
def create_pet():
    # Save categories if not yet
    if not session.get("fields"):
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

        # Create qr code for pet
        create_qr()

        # Redirect to qr code display page
        return redirect("/create-qr")
    
    # Go to page
    return render_template("create_pet.html", fields=session["fields"])

# Display QR code
@app.route("/create-qr", methods=["GET"])
def redirect_qr():
    return render_template("qr_display.html")


# Send qr code image data
@app.route('/qr_image', methods=['GET'])
def qr_image():
    # Get id of pet
    pet_id = session.get('pet_id') or request.args.get('id')
    if not pet_id:
        return ("No pet id", 404)

    # pet_id might be string; ensure int when generating
    try:
        pid = int(pet_id)
    except Exception:
        return ("Invalid pet id", 400)

    # Import helper function here to avoid circular imports on module load
    from helpers import generate_qr_bytes

    # Send image data
    buf = generate_qr_bytes(pid)
    return send_file(buf, mimetype='image/png', as_attachment=False, download_name=f'qr_pet_{pid}.png')