from flask import Flask, render_template, request, redirect
import json
import os
import datetime

# CONFIG_PATH = "../monitor/config.json"
# LOG_PATH = "../logs/health.log"


CONFIG_PATH = "/app/monitor/config.json"
LOG_PATH = "/app/logs/health.log"

app = Flask(__name__)

# Load config file, return the "urls" list
def load_config():
    if not os.path.exists(CONFIG_PATH):
        return []
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
        return data.get("urls", [])

# Save config file with top-level "urls" key
def save_config(sites):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"urls": sites}, f, indent=2)

# Load latest status info from health.log
def load_latest_status():
    status_map = {}
    if not os.path.exists(LOG_PATH):
        return status_map
    with open(LOG_PATH, "r") as f:
        lines = f.readlines()
        for line in reversed(lines):
            try:
                record = json.loads(line)
                url = record.get("url")
                if url not in status_map:
                    status_map[url] = {
                        "status": "green" if record.get("status") == "up" else "red",
                        "timestamp": record.get("timestamp"),
                        "history": record.get("history", [])
                    }
            except:
                continue
    return status_map

@app.route("/")
def index():
    sites = load_config()
    statuses = load_latest_status()
    data = []
    for site in sites:
        url = site['url']
        interval = site['interval']
        s = statuses.get(url, {"status": "unknown", "history": []})
        data.append({
            "url": url,
            "interval": interval,
            "status": s["status"],
            "history": ''.join(s.get("history", [])) or "(no data)"
        })
    return render_template("index.html", data=data)

@app.route("/add", methods=["POST"])
def add_url():
    url = request.form.get("url")
    interval = int(request.form.get("interval"))
    sites = load_config()

    if not any(s['url'] == url for s in sites):
        sites.append({"url": url, "interval": interval})
        save_config(sites)
    return redirect("/")

@app.route("/remove", methods=["POST"])
def remove_url():
    url = request.form.get("url")
    
    #print("Trying to remove:", url) 
    
    sites = load_config()
    sites = [s for s in sites if s['url'] != url]
    save_config(sites)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
