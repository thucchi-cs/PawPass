from datetime import date
from flask import redirect, session, flash, request
from functools import wraps
import qrcode
from qrcode.constants import ERROR_CORRECT_H
import os


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
    pet_id = session.get("pet_id")
    if not pet_id:
        return None

    # Build absolute URL to pet display page (host_url includes trailing slash)
    try:
        pet_url = request.host_url + f"pet?id={pet_id}"
    except RuntimeError:
        # If request context unavailable, fall back to relative URL
        pet_url = f"/pet?id={pet_id}"

    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code (1-40)
        error_correction=ERROR_CORRECT_H, # Error correction level (L, M, Q, H)
        box_size=10,  # Number of pixels per "box" of the QR code
        border=4,  # Thickness of the border around the QR code
    )

    # Add data to the QR code and render image
    qr.add_data(pet_url)
    qr.make(fit=True) # Adjusts the size of the QR code to fit the data

    # Create the image with custom colors
    img = qr.make_image(fill_color="darkblue", back_color="lightblue")

    # Ensure static directory exists and save the QR image there
    filename = f"qr_{pet_id}.png"
    static_dir = os.path.join(os.getcwd(), "static")
    if not os.path.isdir(static_dir):
        try:
            os.makedirs(static_dir, exist_ok=True)
        except Exception:
            # fallback to current directory if unable to create
            static_dir = os.getcwd()

    out_path = os.path.join(static_dir, filename)
    img.save(out_path)

    # Store filename in session so template can access it
    session["qr_filename"] = filename
    return filename
    
