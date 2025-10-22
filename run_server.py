# run_server.py - Production server using Waitress (Windows-compatible)
from waitress import serve
from tracker import app
import os

if __name__ == "__main__":
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    threads = int(os.getenv("THREADS", "4"))

    print(f"Starting Mail Tracker on {host}:{port}")
    print(f"Using {threads} threads")
    print("Press Ctrl+C to stop")

    # Run with Waitress
    serve(
        app,
        host=host,
        port=port,
        threads=threads,
        url_scheme="http",
        ident="MailTracker"
    )