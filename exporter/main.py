# from prometheus_client import start_http_server
# import time
# from metrics.definitions import *  # Import the shared metrics

# if __name__ == "__main__":
#     print("Metrics exporter running on port 8000...")
#     start_http_server(8000)

#     # Keep the service alive
#     while True:
#         time.sleep(10)


from fastapi import FastAPI, Response
from prometheus_client import multiprocess, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
import uvicorn

app = FastAPI()

@app.get("/metrics")
def metrics():
    # Create a registry that gathers metrics from the shared multiprocess folder
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    # Run the FastAPI server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

