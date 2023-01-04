FROM ubuntu
RUN apt-get update && apt-get install -y \
    python3-prometheus-client \
    intel-gpu-tools
COPY prometheus_igpu_exporter.py /var/python_scripts/prometheus_igpu_exporter.py
CMD  /usr/bin/python3 /var/python_scripts/prometheus_igpu_exporter.py $REFRESH_PERIOD_MS

# docker build -t prometheus_igpu_exporter .