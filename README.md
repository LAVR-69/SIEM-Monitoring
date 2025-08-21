SIEM-Monitoring Dashboard

## Dashboard Preview
![SIEM-Monitoring Dashboard Screenshot](./Screenshot-from-2025-08-21-15-48-43.png)

---

## Project Overview
This project delivers a **lightweight SIEM-lite monitoring stack** on Kubernetes, featuring:

- **Prometheus** → scraping & alerting  
- **Grafana** → dashboards & notifications  
- **InfluxDB + Telegraf** → time-series ingestion (events/metrics pipeline)  
- **Custom Endpoint Exporter (Python)** → extra endpoint metrics  
- **Node Exporter** → node-level metrics  

Deployed across two namespaces:  
- `siem-ltm` → Prometheus, Grafana, node-exporter, endpoint-exporter  
- `siem-event` → InfluxDB, Telegraf  

---

## Project Structure
```plaintext
/siem-monitoring
 ├── Exporter/
 │    ├── Dockerfile
 │    ├── endpoint-exporter.yaml
 │    └── endpoint_exporter.py
 │
 ├── Hybrid SIEM K8 v.2/
 │    ├── Alert-ASCII-flow.yaml
 │    ├── Alert.yaml
 │    └── Hybrid SIEM K8 v.2-1755813699348.json
 │
 ├── Telegraf/
 │    ├── Dockerfile
 │    ├── telegraf.conf
 │    └── telegraf.yaml
 │
 ├── grafana-datasources.yaml
 ├── grafana-prometheus.yaml
 ├── grafana-pvc.yaml
 ├── node-exporter.yaml
 ├── prometheus-config.yaml
 ├── prometheus-deploy.yaml
 ├── tailscale-config.md
 └── README.md
Setup Instructions
Clone Repository

bash
Copy
Edit
git clone https://github.com/LAVR-69/SIEM-Monitoring.git
cd SIEM-Monitoring
Create Namespaces

bash
Copy
Edit
kubectl create ns siem-ltm || true
kubectl create ns siem-event || true
Deploy Prometheus, Grafana, Node Exporter (namespace: siem-ltm)

bash
Copy
Edit
kubectl apply -f prometheus-config.yaml -n siem-ltm
kubectl apply -f prometheus-deploy.yaml -n siem-ltm
kubectl apply -f grafana-pvc.yaml -n siem-ltm
kubectl apply -f grafana-prometheus.yaml -n siem-ltm
kubectl apply -f grafana-datasources.yaml -n siem-ltm
kubectl apply -f node-exporter.yaml -n siem-ltm
Deploy InfluxDB + Telegraf (namespace: siem-event)

bash
Copy
Edit
kubectl apply -f Telegraf/telegraf.yaml -n siem-event
Deploy Endpoint Exporter (namespace: siem-ltm)

bash
Copy
Edit
kubectl apply -f Exporter/endpoint-exporter.yaml -n siem-ltm
Access Services (port-forward locally)

bash
Copy
Edit
kubectl port-forward svc/prometheus 9090:9090 -n siem-ltm
kubectl port-forward svc/grafana 3000:3000 -n siem-ltm
kubectl port-forward svc/influxdb 8086:8086 -n siem-event
Import Dashboard & Alerts

Import JSON: Hybrid SIEM K8 v.2/Hybrid SIEM K8 v.2-1755813699348.json

Alerts reference: Hybrid SIEM K8 v.2/Alert.yaml

Notifications

Configure Slack/MS Teams in Grafana Alerting → Contact Points

Route via Notification Policies

Project Reflections
✅ Do’s (What We Did Right)
Used Kubernetes manifests → reproducible & scalable deployments

Integrated Telegraf + InfluxDB → lightweight time-series pipeline

Modular configs (separate dirs for Grafana, Prometheus, Telegraf, exporters)

Ready-to-use JSON dashboards → fast reproducibility

Slack alert integration (functional for critical alerts)

❌ Don’ts (Mistakes We Made)
Didn’t test persistent storage for InfluxDB → metric resets after pod restarts

Mixed manual steps with automation → should’ve gone full automation

Initially forgot namespaces → risked conflicts with cluster services

Poorly documented exporter endpoints → led to scrape failures

🏆 Achievements
Fully working SIEM-lite dashboard (system, network, endpoint metrics)

Multi-source data integration (Prometheus + InfluxDB) into Grafana

Fixed “empty Grafana” issue → Telegraf → Influx pipeline stable

Real-time monitoring with low latency

Alerts pipeline from Prometheus → Slack

⚠️ Limitations
No centralized log monitoring (ELK/Loki not included)

Alerts need tuning (false positives)

Grafana only admin-level access (no RBAC)

No long-term retention for metrics (Influx storage limited)

Dashboards/alerts not auto-provisioned (manual import required)

Contributors
Afreen — Grafana dashboards & alert setup

Aviral (me) — Kubernetes manifests, Prometheus configs, InfluxDB + Telegraf integration
