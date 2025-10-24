from datetime import date
from flask import redirect, session, flash, request
from functools import wraps
import qrcode
from qrcode.constants import ERROR_CORRECT_H
import os
from io import BytesIO


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
def _build_pet_url(pet_id: int) -> str:
    """Return an absolute or relative URL to the pet page for given id."""
    try:
        # request.host_url includes trailing '/'
        return request.host_url + f"pet?id={pet_id}"
    except RuntimeError:
        return f"/pet?id={pet_id}"


def generate_qr_bytes(pet_id: int) -> BytesIO:
    """Generate a PNG QR image for the pet URL and return a BytesIO buffer.

    This avoids writing to disk so it works on read-only filesystems.
    """
    pet_url = _build_pet_url(pet_id)

    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(pet_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="darkblue", back_color="lightblue")

    buf = BytesIO()
    # Pillow-compatible save
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def create_qr():
    """Legacy helper kept for compatibility.

    If called after storing `session['pet_id']`, it will ensure QR can be
    generated on-demand. It does not write to disk.
    """
    pet_id = session.get("pet_id")
    if not pet_id:
        return None
    # Return BytesIO but don't persist it to session (session size limits)
    return generate_qr_bytes(pet_id)
    
