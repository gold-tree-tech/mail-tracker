# tracker.py
from flask import Flask, request, send_file, make_response
import sqlite3
import io
import datetime
import os

DB = "opens.db"
app = Flask(__name__)

# create db
if not os.path.exists(DB):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE opens (
        id TEXT,
        ip TEXT,
        ua TEXT,
        ts TEXT
    )
    """)
    conn.commit()
    conn.close()

# a 1x1 transparent GIF binary
TRANSPARENT_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF!"
    b"\xF9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00"
    b"\x00\x02\x02L\x01\x00;"
)

@app.route("/track")
def track():
    tracking_id = request.args.get("id", "unknown")
    ip = request.remote_addr or ""
    ua = request.headers.get("User-Agent", "")
    ts = datetime.datetime.utcnow().isoformat() + "Z"

    # store
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO opens (id, ip, ua, ts) VALUES (?, ?, ?, ?)",
                (tracking_id, ip, ua, ts))
    conn.commit()
    conn.close()

    # return transparent gif
    response = make_response(send_file(io.BytesIO(TRANSPARENT_GIF),
                                       mimetype="image/gif"))
    # prevent caching to get repeated opens
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    # run in debug for testing; use a production server (gunicorn) for production
    app.run(host="0.0.0.0", port=5000)
