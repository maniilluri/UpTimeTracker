import time
import json
import requests
from datetime import datetime

CONFIG_PATH = "config.json"
LOG_PATH = "../logs/health.log"

# Load list of sites to monitor
def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading config.json:", e)
        return []

# Log a single result to health.log
def log_status(entry):
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

# Perform a health check on a single URL
def check_url(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code < 500:
            return "up"
        else:
            return "down"
    except Exception:
        return "down"

def run_scheduler():
    last_checked = {}  # Track last check time per URL

    print("[Scheduler] Starting UptimeTrackr scheduler...\n")

    while True:
        config = load_config()
        now = time.time()

        for entry in config:
            url = entry["url"]
            interval = entry["interval"]

            # Check if it's time to check this URL again
            if url not in last_checked or (now - last_checked[url]) >= interval:
                status = check_url(url)
                timestamp = datetime.utcnow().isoformat()

                # Log result
                log_entry = {
                    "url": url,
                    "status": status,
                    "timestamp": timestamp
                }
                log_status(log_entry)

                print(f"[{timestamp}] {url} ➜ {status}")
                last_checked[url] = now

        time.sleep(1)  # Small pause to avoid tight CPU loop

if __name__ == "__main__":
    run_scheduler()
