# 🚀 SIEM-Monitoring Dashboard

## 📸 Dashboard Preview
![SIEM-Monitoring Dashboard Screenshot](./Screenshot-from-2025-08-21-15-48-43.png)

---

## 📖 Project Overview
This project implements a **lightweight SIEM-lite monitoring stack** on **Kubernetes**, designed for real-time monitoring of nodes, endpoints, and events.  

It integrates multiple components:  
- **Prometheus** → scraping & alerting  
- **Grafana** → visualization & alert delivery  
- **InfluxDB + Telegraf** → time-series ingestion (system + event metrics pipeline)  
- **Custom Python Exporter** → endpoint-level monitoring  
- **Node Exporter** → node-level metrics  

**Namespaces Used:**  
- `siem-ltm` → Prometheus, Grafana, node-exporter, endpoint-exporter  
- `siem-event` → InfluxDB, Telegraf  

---

 ## 🗂 Project Structure
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

---

## ⚙️ Setup Instructions
 1️⃣ Clone Repository
git clone https://github.com/LAVR-69/SIEM-Monitoring.git
cd SIEM-Monitoring

2️⃣ Create Namespaces
kubectl create ns siem-ltm || true
kubectl create ns siem-event || true

3️⃣ Deploy Prometheus, Grafana, Node Exporter (siem-ltm)
kubectl apply -f prometheus-config.yaml -n siem-ltm
kubectl apply -f prometheus-deploy.yaml -n siem-ltm
kubectl apply -f grafana-pvc.yaml -n siem-ltm
kubectl apply -f grafana-prometheus.yaml -n siem-ltm
kubectl apply -f grafana-datasources.yaml -n siem-ltm
kubectl apply -f node-exporter.yaml -n siem-ltm

4️⃣ Deploy InfluxDB + Telegraf (siem-event)
kubectl apply -f Telegraf/telegraf.yaml -n siem-event

5️⃣ Deploy Endpoint Exporter (siem-ltm)
kubectl apply -f Exporter/endpoint-exporter.yaml -n siem-ltm

6️⃣ Access Services (Local Port-Forward)
kubectl port-forward svc/prometheus 9090:9090 -n siem-ltm
kubectl port-forward svc/grafana 3000:3000 -n siem-ltm
kubectl port-forward svc/influxdb 8086:8086 -n siem-event

7️⃣ Import Dashboard & Alerts

## Dashboard JSON:
Hybrid SIEM K8 v.2/Hybrid SIEM K8 v.2-1755813699348.json

## Alerts Config:
Hybrid SIEM K8 v.2/Alert.yaml

8️⃣ Notifications

## Configure Slack/MS Teams inside Grafana:

Alerting → Contact Points

Route alerts via Notification Policies

---

## ✅ Do’s (What We Did Right)

Used Kubernetes manifests → reproducible, scalable deployments

Integrated Telegraf + InfluxDB → lightweight time-series pipeline

Modularized configs → Prometheus, Grafana, Telegraf, exporters separated

Pre-built JSON dashboards → fast reproducibility

Slack alerts worked for critical events

## ❌ Don’ts (Mistakes Made)

Didn’t configure persistent storage for InfluxDB → metrics reset on pod restart

Mixed manual steps + automation instead of full automation

Initially missed namespaces → risked cluster conflicts

Poor exporter documentation → caused scrape failures

## 🏆 Achievements

Fully working SIEM-lite dashboard (system, network, endpoint metrics)

Integrated data sources: Prometheus + InfluxDB → Grafana

Fixed “empty Grafana” issue by stabilizing Telegraf → Influx pipeline

Achieved real-time monitoring with low latency

Alerts flowing end-to-end → Prometheus → Grafana → Slack

## ⚠️ Limitations

No centralized logs (ELK/Loki missing)

Alerts need tuning (false positives exist)

Grafana has only admin-level access (no RBAC yet)

Metrics retention limited (InfluxDB not persistent)

Dashboards/alerts not auto-provisioned (manual import)

## 👥 Contributors

Afreen — Grafana dashboards & alert setup

Aviral (me) — Kubernetes manifests, Prometheus configs, InfluxDB + Telegraf integration
 │
 ├── grafana-datasources.yaml
 ├── grafana-prometheus.yaml
 ├── grafana-pvc.yaml
 ├── node-exporter.yaml
 ├── prometheus-config.yaml
 ├── prometheus-deploy.yaml
 ├── tailscale-config.md
 └── README.md

---

