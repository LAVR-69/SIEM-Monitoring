SIEM-Monitoring

## Dashboard Preview

![SIEM-Monitoring Dashboard Screenshot](/home/lavr69/Pictures/Screenshot from 2025-08-21 15-48-43.png)



---

## Project Overview

This repo delivers a **lightweight SIEM-lite monitoring stack** on Kubernetes with:

- **Prometheus** for scraping and alerting
- **Grafana** for dashboards and notifications
- **InfluxDB + Telegraf** for time-series ingestion (events/metrics pipeline)
- **Custom endpoint exporter** (Python) for extra metrics
- **Node Exporter** for node-level metrics

Deployed in **two namespaces**:
- `siem-ltm` → Prometheus, Grafana, node-exporter, endpoint-exporter
- `siem-event` → InfluxDB, Telegraf

No USB nonsense here. Just the monitoring stack we built.

---

## Project Structure

/siem-monitoring
├── Exporter/
│ ├── Dockerfile
│ ├── endpoint-exporter.yaml
│ └── endpoint_exporter.py
│
├── Hybrid SIEM K8 v.2/
│ ├── Alert-ASCII-flow.yaml
│ ├── Alert.yaml
│ └── Hybrid SIEM K8 v.2-1755813699348.json
│
├── Telegraf/
│ ├── Dockerfile
│ ├── telegraf.conf
│ └── telegraf.yaml
│
├── grafana-datasources.yaml
├── grafana-prometheus.yaml
├── grafana-pvc.yaml
├── node-exporter.yaml
├── prometheus-config.yaml
├── prometheus-deploy.yaml
├── tailscale-config.md
└── README.md

yaml
Copy
Edit

---

## Setup Instructions

### 1) Clone Repository

```bash
git clone https://github.com/LAVR-69/SIEM-Monitoring.git
cd SIEM-Monitoring
2) Create Namespaces
bash
Copy
Edit
kubectl create ns siem-ltm || true
kubectl create ns siem-event || true
3) Deploy Prometheus, Grafana, Node Exporter (namespace: siem-ltm)
bash
Copy
Edit
# Prometheus
kubectl apply -f prometheus-config.yaml -n siem-ltm
kubectl apply -f prometheus-deploy.yaml -n siem-ltm

# Grafana (PVC → Deployment → Datasources provisioning)
kubectl apply -f grafana-pvc.yaml -n siem-ltm
kubectl apply -f grafana-prometheus.yaml -n siem-ltm
kubectl apply -f grafana-datasources.yaml -n siem-ltm

# Node Exporter
kubectl apply -f node-exporter.yaml -n siem-ltm
4) Deploy InfluxDB + Telegraf (namespace: siem-event)
InfluxDB was already running in our cluster as influxdb-0 (StatefulSet). If you don’t have it, install InfluxDB first (Helm or your own manifest), then:

bash
Copy
Edit
# Telegraf (reads host/pod metrics, writes to InfluxDB)
kubectl apply -f Telegraf/telegraf.yaml -n siem-event
If your Influx endpoint/credentials differ, edit Telegraf/telegraf.conf + the ConfigMap in telegraf.yaml to match.

5) Deploy Custom Endpoint Exporter (namespace: siem-ltm)
bash
Copy
Edit
# If you need a custom image:
# cd Exporter && docker build -t <your-registry>/endpoint-exporter:latest .
# docker push <your-registry>/endpoint-exporter:latest
# (then update the image field in Exporter/endpoint-exporter.yaml)

kubectl apply -f Exporter/endpoint-exporter.yaml -n siem-ltm
Ensure prometheus-config.yaml has a scrape job for this exporter (it does in our setup).

6) Access Services (port-forward for local)
bash
Copy
Edit
# Prometheus
kubectl port-forward svc/prometheus 9090:9090 -n siem-ltm

# Grafana
kubectl port-forward svc/grafana 3000:3000 -n siem-ltm

# InfluxDB (if needed)
kubectl port-forward svc/influxdb 8086:8086 -n siem-event
7) Import Dashboard & Alerts (Grafana)
Grafana → Dashboards → Import → upload:

Hybrid SIEM K8 v.2/Hybrid SIEM K8 v.2-1755813699348.json

Grafana (Alerting → Alert rules):

Use Hybrid SIEM K8 v.2/Alert.yaml as reference (Grafana-managed rules are stored in Grafana DB; this file is a snapshot of what we configured).

8) Hook Up Notifications (Slack / Teams / Email)
Grafana → Alerting → Contact points → add Slack webhook

Route alerts via Notification policies to Slack/MS Teams

# Testing / Load Generation (to validate alerts)
CPU spike (inside a test pod):

bash
Copy
Edit
kubectl run cpu-burn --image=alpine -n siem-ltm --restart=Never -- sh -c "yes > /dev/null"
# cleanup: kubectl delete pod cpu-burn -n siem-ltm
Memory spike (inside a test pod):

bash
Copy
Edit
kubectl run mem-burn --image=alpine -n siem-ltm --restart=Never -- sh -c "head -c 500M < /dev/zero | tail > /dev/null && sleep 60"
# cleanup: kubectl delete pod mem-burn -n siem-ltm
Network throughput spike (iperf3) across namespaces:

bash
Copy
Edit
# server in siem-ltm
kubectl run iperf-server -n siem-ltm --image=networkstatic/iperf3 --restart=Never -- -s

# client in siem-event (run for 120s with 4 parallel streams)
kubectl run iperf-client -n siem-event --image=networkstatic/iperf3 --restart=Never -- \
  -c iperf-server.siem-ltm.svc.cluster.local -p 5201 -t 120 -P 4
If AlreadyExists, delete first:

bash
Copy
Edit
kubectl delete pod iperf-client -n siem-event --ignore-not-found
kubectl delete pod iperf-server -n siem-ltm --ignore-not-found
# Files Description
Exporter/endpoint_exporter.py
Python custom exporter exposing endpoint metrics on /metrics.

Exporter/endpoint-exporter.yaml
K8s Deployment/Service for the endpoint exporter.

Exporter/Dockerfile
Build context for the exporter container image.

grafana-prometheus.yaml
Grafana Deployment/Service (uses PVC for persistence).

grafana-datasources.yaml
Grafana provisioning for Prometheus + InfluxDB data sources.

grafana-pvc.yaml
PersistentVolumeClaim for Grafana data.

prometheus-config.yaml
Prometheus scrape configs (node-exporter, endpoint-exporter, etc.).

prometheus-deploy.yaml
Prometheus Deployment/Service.

node-exporter.yaml
Node Exporter DaemonSet + Service for node-level metrics.

Telegraf/telegraf.conf
Telegraf inputs/outputs config (writes to InfluxDB).

Telegraf/telegraf.yaml
K8s Deployment/ConfigMap/Service for Telegraf.

Hybrid SIEM K8 v.2/Hybrid SIEM K8 v.2-1755813699348.json
Exported Grafana dashboard JSON.

Hybrid SIEM K8 v.2/Alert.yaml
Snapshot of Grafana alert rules we configured through UI.

Hybrid SIEM K8 v.2/Alert-ASCII-flow.yaml
ASCII flow / doc reference for alert routing.

tailscale-config.md
Optional doc for Tailscale setup (if you centralize remote metric collection).

# Known Issues
If endpoint-exporter shows ImagePullBackOff, fix the image repo/tag in Exporter/endpoint-exporter.yaml.

Network alert won’t fire if you query the wrong metric. Use proper PromQL (see below).

Grafana-managed alert rules live in Grafana’s DB; YAML snapshots are for reference/backups, not 1:1 imports.

# Useful PromQL (what actually worked)
CPU usage (non-idle):

java
Copy
Edit
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
Memory available (MiB):

yaml
Copy
Edit
(node_memory_MemAvailable_bytes / 1024 / 1024)
Network throughput (RX+TX B/s, excluding loopback):

less
Copy
Edit
sum by (instance) (
  rate(node_network_receive_bytes_total{device!~"lo"}[1m]) +
  rate(node_network_transmit_bytes_total{device!~"lo"}[1m])
)
Sockets used (your “IPv4 requests” placeholder):

nginx
Copy
Edit
node_sockstat_sockets_used
Tune alert thresholds + pending windows in Grafana Alerting.

# Contributors
Afreen — Grafana dashboard design & alert setup

Aviral (me) — Kubernetes pods, Prometheus config, scraping, InfluxDB + Telegraf integration

# Project Development Journey & Challenges
Split namespaces: Put Prom/Grafana/node-exporter/endpoint-exporter in siem-ltm and Influx/Telegraf in siem-event to keep pipelines clean.

# Grafana datasource hiccup: Initial panels were empty → fixed Grafana provisioning (grafana-datasources.yaml) and verified Prometheus/Influx URLs.

# Network alert not firing: First query was wrong → switched to sum(rate(node_network_*_bytes_total[1m])) and excluded lo.

# Slack delay: Alerts felt slow → reduced evaluation interval and pending time.

# iperf missing: Pod failed (exec: "iperf3": not found) → used networkstatic/iperf3 image and ran server/client in separate namespaces.

# Endpoint exporter rollout: Built image, deployed via Exporter/endpoint-exporter.yaml, added scrape job in prometheus-config.yaml.

Everything is minimal, reproducible, and doesn’t drag in stuff we didn’t actually use.

Project Reflections
# Do’s (What We Did Right)

Used Kubernetes manifests for deployment → ensured reproducibility & scalability.

Chose Telegraf + InfluxDB for lightweight metric collection → minimal resource overhead.

Integrated Prometheus exporters (Node & Blackbox) → expanded observability beyond system metrics.

Designed Grafana dashboards with pre-built JSON files → fast setup for anyone cloning the repo.

Kept configs modular (separate dirs for Grafana, Prometheus, Telegraf, exporters) → maintainable structure.

Configured alerts in Prometheus with Slack integration (work in progress but functional for critical cases).

# Don’ts (What We Should Avoid Next Time)

Didn’t fully test persistent volumes for InfluxDB → caused metric resets after pod restarts.

Mixed manual & automated configs (some scripts + some kubectl apply) → should have gone all-in on automation.

Initially forgot to namespace monitoring stack → risked config conflicts with other cluster services.

Overlooked documenting exporter endpoints properly → caused scrape failures during setup.

# Achievements (Things We Pulled Off Successfully)

Deployed a fully working SIEM-lite dashboard showing system, network, and endpoint metrics.

Integrated multi-source data (InfluxDB + Prometheus exporters) into a single Grafana view.

Solved the “Grafana empty data” issue by fixing Telegraf → Influx pipeline.

Achieved real-time monitoring with low latency.

Created ready-to-use JSON dashboards so team members don’t have to build visualizations manually.

Established alerting pipeline (Prometheus → Slack).

# Limitations (Things We Couldn’t Achieve Yet)

No centralized log monitoring (e.g., Loki/ELK) → project focused only on metrics, not logs.

Alerts not fully tuned for thresholds & noise reduction (some false positives).

No RBAC or multi-user Grafana setup → only admin-level access configured.

Couldn’t implement long-term metric retention → limited by InfluxDB storage.

Didn’t integrate USB/device event monitoring (was in older SIEM-LTM project, not ported here).

Missing auto-provisioning for dashboards/alerts via Grafana API (manual import needed).
