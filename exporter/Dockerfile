
FROM python:3.10-slim
ENV prometheus_multiproc_dir=/tmp/metrics

WORKDIR /app

COPY exporter/ exporter/
COPY metrics/ metrics/
COPY requirements.txt ./

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app 


RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "exporter/main.py"]
