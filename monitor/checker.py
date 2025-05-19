import json
import time
import requests
from datetime import datetime
from metrics.definitions import update_metrics

def load_config():
    with open("monitor/config.json", "r") as f:
        return json.load(f)

def log_result(url, status_code, response_time):
    log_line = f"{datetime.utcnow().isoformat()} | {url} | Status: {status_code} | Response Time: {response_time:.2f} ms\n"
    with open("logs/health.log", "a") as f:
        f.write(log_line)
    print(log_line.strip(), flush=True)

    update_metrics(url, status_code, response_time)

def check_url(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        elapsed = (time.time() - start) * 1000  # ms
        return response.status_code, elapsed
    except Exception as e:
        return f"Error: {e}", -1

def main():
    config = load_config()
    urls = config["urls"]
    interval = config.get("check_interval_seconds", 60)

    while True:
        for url in urls:
            status, latency = check_url(url)
            log_result(url, status, latency)
        print(f"Sleeping for {interval} seconds...\n", flush=True)
        time.sleep(interval)

if __name__ == "__main__":
    main()
