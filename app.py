from flask import Flask, redirect, request, render_template, jsonify
import qrcode
import qrcode.constants
from PIL import Image
import os
import random
import string
from database import init_db, create_campaign, get_all_campaigns, log_scan, get_campaign_by_code, get_scans_by_code

app = Flask(__name__)

# Folder to save QR code images
QR_FOLDER = "static/qr_codes"
os.makedirs(QR_FOLDER, exist_ok=True)

# Initialize the database on startup
init_db()

# ─── Generate a random short code ───────────────────────────────────────────
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ─── Home page ───────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ─── Create a new campaign + generate QR ─────────────────────────────────────
@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    name = data.get("name")
    destination_url = data.get("destination_url")
    color = data.get("color", "#000000")

    if not name or not destination_url:
        return jsonify({"error": "Name and URL are required"}), 400

    # Generate unique short code
    short_code = generate_short_code()

    # The tracking URL that the QR will point to
    base_url = request.host_url
    tracking_url = f"{base_url}track/{short_code}"

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(tracking_url)
    qr.make(fit=True)

    # Convert hex color to RGB tuple
    hex_color = color.lstrip("#")
    fill_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    img = qr.make_image(fill_color=fill_color, back_color="white")

    # Save QR code image
    qr_filename = f"{short_code}.png"
    qr_path = os.path.join(QR_FOLDER, qr_filename)
    img.save(qr_path)

    # Save campaign to database
    create_campaign(name, destination_url, short_code)

    return jsonify({
        "success": True,
        "short_code": short_code,
        "tracking_url": tracking_url,
        "qr_image": f"/static/qr_codes/{qr_filename}"
    })

# ─── Track scan + redirect ────────────────────────────────────────────────────
@app.route("/track/<short_code>")
def track(short_code):
    campaign = get_campaign_by_code(short_code)
    if not campaign:
        return "Campaign not found!", 404

    # Log the scan
    user_agent = request.headers.get("User-Agent", "")
    ip_address = request.remote_addr
    log_scan(short_code, user_agent, ip_address)

    # Redirect to destination
    return redirect(campaign[2])

# ─── Dashboard ────────────────────────────────────────────────────────────────
@app.route("/dashboard")
def dashboard():
    campaigns = get_all_campaigns()
    return render_template("dashboard.html", campaigns=campaigns)

# ─── API: Get scan details for a campaign ─────────────────────────────────────
@app.route("/api/scans/<short_code>")
def api_scans(short_code):
    scans = get_scans_by_code(short_code)
    scan_list = [{"scanned_at": s[2], "ip": s[4]} for s in scans]
    return jsonify(scan_list)

if __name__ == "__main__":
    app.run(debug=True)