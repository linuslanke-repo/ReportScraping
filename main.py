import http.server
import socketserver
import os
import threading
import subprocess

def run_your_scraper():
    print("[Docker Engine] Starting your Orchestrator scraping pipeline...")
    try:
        # This executes your existing Orchestrator script inside the container
        result = subprocess.run(["python", "Orchestrator.py"], capture_output=True, text=True)
        print("[Docker Engine] Script Output:\n", result.stdout)
        if result.stderr:
            print("[Docker Engine] Script Errors:\n", result.stderr)
    except Exception as e:
        print(f"[Docker Engine] Failed to run scraping architecture: {e}")

# Trigger the scraper execution in a separate background thread
# This prevents the web server from freezing or timing out on Render
threading.Thread(target=run_your_scraper, daemon=True).start()

# Initialize the fallback web server layer to satisfy Render's port checker
PORT = int(os.environ.get("PORT", 8080))
class CloudStatusHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html_response = """
        <html>
            <head><title>Scraper Status</title></head>
            <body style='font-family: sans-serif; text-align: center; padding-top: 50px;'>
                <h1>Report Scraping Engine Active</h1>
                <p>Your web scraper container is executing background extraction loops.</p>
                <p>Check your Render console log dashboard to view active scraping outputs.</p>
            </body>
        </html>
        """
        self.wfile.write(bytes(html_response, "utf-8"))

with socketserver.TCPServer(("", PORT), CloudStatusHandler) as httpd:
    print(f"[Docker Engine] Web status gateway heartbeat active on port {PORT}")
    httpd.serve_forever()
