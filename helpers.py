from datetime import date
from flask import redirect, session, flash, request
from functools import wraps
import qrcode
from qrcode.constants import ERROR_CORRECT_H
import os
from io import BytesIO

# Generate secret key
def secret_key():
    import secrets
    print(secrets.token_hex(32))

# Find the id of the given category
def find_cat_id(cat):
    for id,value in session.get("fields", {}).items():
        if value["name"] == cat:
            return id
    return -1

# Capitalize a word
def cap(s):
    return s.capitalize()

# Save the categories in session
def save_categories(categories):
    fields = {}
    for c in categories:
        fields[str(c["id"])] = {"name": c["category"], "req": c["req"], "descr": c["descr"]}
    session["fields"] = fields

# Get url to pet display
def _build_pet_url(pet_id):
    try:
        # request.host_url includes trailing '/'
        return request.host_url + f"pet?id={pet_id}"
    
    # Backup
    except RuntimeError:
        return f"/pet?id={pet_id}"

# Generate PNG of QR code and return as a BytesIO buffer
def generate_qr_bytes(pet_id):
    # Get url qr code is directed to
    pet_url = _build_pet_url(pet_id)
    session["pet_link"] = pet_url

    # Create the qr code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(pet_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#2563eb")

    # Save qr code to buffer
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# Create a qr code to the pet display page
def create_qr():
    # Get id of pet
    pet_id = session.get("pet_id")
    if not pet_id:
        return None
    
    # Return BytesIO of qr code
    return generate_qr_bytes(pet_id)
    
# Check if currently logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            print(session.get("logged_in"), "user")
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function