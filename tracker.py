from flask import Flask, request, make_response, send_file
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid
import datetime
import io
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Supabase Setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 1x1 Transparent GIF for tracking
TRANSPARENT_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF!"
    b"\xF9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00"
    b"\x00\x02\x02L\x01\x00;"
)

# Log email metadata into Supabase


def store_email_metadata(recipient_email, tracking_id):
    supabase.table("email_metadata").insert({
        "recipient_email": recipient_email,
        "tracking_id": tracking_id,
        "timestamp": datetime.datetime.now().isoformat()
    }).execute()

# Log email opens into Supabase


def log_open(tracking_id):
    supabase.table("opens").insert({
        "tracking_id": tracking_id,
        "timestamp": datetime.datetime.now().isoformat()
    }).execute()

# Route for sending tracked email


@app.route('/email', methods=['POST'])
def send_email():
    to_email = request.form.get('to_email')
    subject = request.form.get('subject')
    body_html = request.form.get('body_html')
    smtp_user = request.form.get('smtp_user')
    smtp_pass = request.form.get('smtp_pass')

    # Generate a unique tracking ID
    tracking_id = str(uuid.uuid4())

    # Store metadata
    store_email_metadata(to_email, tracking_id)

    # Prepare HTML email with tracking pixel
    base_url = os.getenv("BASE_URL", "http://localhost:5000")
    print(base_url)
    tracker_url = f"{base_url}/track?id={tracking_id}"
    tracked_html = f"""
    {body_html}
    <img src="{tracker_url}" width="1" height="1" alt="" style="opacity:0;position:absolute;" />
    """

    # Send the email
    try:
        smtp_host = "smtp.gmail.com"  # Update if using a different SMTP service
        smtp_port = 587

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg.attach(MIMEText(tracked_html, "html"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, to_email, msg.as_string())

        return f"Email sent to {to_email} with tracking ID: {tracking_id}"
    except Exception as e:
        return f"Failed to send email: {e}"

# Route for tracking pixel


@app.route('/track')
def track():
    tracking_id = request.args.get('id')
    if tracking_id:
        try:
            log_open(tracking_id)  # Log the open event
            print(f"Tracked open for ID: {tracking_id}")
        except Exception as e:
            print(f"Error logging open: {e}")

    # Return the 1x1 transparent GIF
    response = make_response(
        send_file(io.BytesIO(TRANSPARENT_GIF), mimetype="image/gif"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
