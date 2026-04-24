import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 5000))

HTML = """<!doctype html>
<html><head><meta charset="utf-8"><title>Zalith Launcher 2 - Source</title>
<style>
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:780px;margin:40px auto;padding:0 20px;line-height:1.55;color:#1f2328;background:#f6f8fa}
h1{font-size:28px;margin:0 0 8px}
h2{font-size:18px;margin-top:28px;border-bottom:1px solid #d0d7de;padding-bottom:6px}
code{background:#eaeef2;padding:2px 6px;border-radius:4px;font-size:13px}
.card{background:#fff;border:1px solid #d0d7de;border-radius:8px;padding:20px 24px;margin-top:16px}
ol li{margin:6px 0}
.note{background:#fff8c5;border:1px solid #d4a72c;padding:12px 14px;border-radius:6px;margin-top:14px;font-size:14px}
</style></head><body>
<h1>Zalith Launcher 2 - Source Repository</h1>
<p>This Replit project holds the Android source. It is built on GitHub Actions, not in Replit.</p>
<div class="card">
<h2>Push to your GitHub repo</h2>
<ol>
<li>Open the <b>Git</b> pane in the left sidebar.</li>
<li>Connect or create a GitHub repo.</li>
<li>Stage all changes, commit, and push.</li>
</ol>
<h2>Build the APK on GitHub</h2>
<ol>
<li>Go to your repo on GitHub.</li>
<li>Open the <b>Actions</b> tab.</li>
<li>Select <b>Build CI</b> and click <b>Run workflow</b> (or just push a commit - it runs automatically).</li>
<li>When it finishes, download the <b>debug apk (arm64)</b> artifact.</li>
</ol>
<div class="note">Builds are configured to produce <b>arm64-v8a only</b> (one APK per run, no other architectures).</div>
<h2>Build locally instead</h2>
<p>Open this folder in <b>Android Studio Bumblebee+</b> with JDK 17, then run <code>./gradlew ZalithLauncher:assembleDebug -Darch=arm64</code>.</p>
</div>
</body></html>
"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))
    def log_message(self, *a, **k):
        pass

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Info server on port {PORT}")
    httpd.serve_forever()
