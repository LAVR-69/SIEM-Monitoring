📖 Hybrid SIEM Monitoring on Kubernetes

This repository documents the complete journey of building a Hybrid SIEM Monitoring system using Kubernetes, Prometheus, InfluxDB, Telegraf, and Grafana.

The project was designed to:

Collect metrics from pods, nodes, and services

Store them reliably in Prometheus and InfluxDB

Visualize them in Grafana with rich dashboards

Trigger alerts to Slack/MS Teams

Experiment with exporters (including USB detection, iperf tests, etc.)

Afreen focused on dashboard design + alerts.
Me(Aviral) worked on Kubernetes pods, Prometheus setup, and InfluxDB integration.

📂 Project Structure
siem-monitoring/
├── manifests/                # Kubernetes YAML manifests
│   ├── prometheus-config.yaml
│   ├── prometheus-deploy.yaml
│   ├── grafana-datasources.yaml
│   ├── grafana-prometheus.yaml
│   ├── grafana-pvc.yaml
│   ├── node-exporter.yaml
│   ├── telegraf.yaml
│   ├── tailscale-config.md
│   ├── ...
│
├── dashboards/               # Exported Grafana dashboards
│   └── Hybrid-SIEM-K8-v2.json
│
├── alerts/                   # Prometheus/Grafana alert rules
│   ├── Alert.yaml
│   ├── Alert-ASCII-flow.yaml
│
├── telegraf/                 # Telegraf configs for InfluxDB
│   ├── telegraf.conf
│   ├── Dockerfile
│
├── exporter/                 # Custom exporters
│   ├── endpoint-exporter.yaml
│   ├── endpoint_exporter.py
│   ├── Dockerfile
│
└── README.md                 # This file

🚀 Step-by-Step Journey
1. Setting Up the Environment

Kubernetes cluster created locally.

Namespaces created:

siem-ltm → for long-term monitoring stack (Prometheus, Grafana, InfluxDB).

siem-event → for event-based exporters and tests.

2. Prometheus Setup

Configured via prometheus-config.yaml for scraping:

Node Exporter

Telegraf metrics (pushed to InfluxDB)

Blackbox exporter for endpoint monitoring

Deployed via prometheus-deploy.yaml.

Verified Prometheus targets and scrape intervals.

3. Grafana Setup

Installed in siem-ltm.

Datasource config:

Prometheus (for live K8s metrics).

InfluxDB (for Telegraf-collected metrics).

Persistent Volume Claim added for dashboards to persist after restarts.

Imported dashboard Hybrid-SIEM-K8-v2.json.

4. Telegraf + InfluxDB Integration

telegraf.conf configured to:

Collect system/network metrics.

Push data to InfluxDB.

Deployed via telegraf.yaml.

Validated using curl queries against InfluxDB to confirm metrics were stored.

5. Exporters

Node Exporter → pod-level and node-level metrics.

Custom Endpoint Exporter → Python-based (monitored USB events, etc.).

Blackbox Exporter → monitored network endpoints, integrated with Prometheus.

iperf pods → created for bandwidth testing (client/server custom images).

6. Alerting Setup

Alerts defined in Prometheus + Grafana:

High CPU/memory.

Disk usage thresholds.

Network packet drops.

Endpoint downtime (via blackbox).

Slack webhook integrated for alert delivery.

Tweaked evaluation intervals for faster detection (reduced delay).

⚔️ Problems We Faced & How We Solved Them
Problem	Cause	Solution
Redash crash	Restart caused DB corruption	Dropped DB + restarted fresh
Pod stuck in Creating	File named usb.py shadowed dependency	Renamed file to avoid conflict
Empty Grafana panels	Wrong datasource config	Fixed Prometheus + Influx endpoints
Slow Slack alerts	Default evaluation interval too high	Tuned down to 15s
iperf pods failing	Image missing executable	Built custom iperf images
USB exporter error	Dependency mismatch	Fixed Python pyusb import
Telegraf → Influx issues	Bad config	Corrected telegraf.conf + validated
Grafana dashboards lost	Restart without PVC	Added persistent volume claim
🌩️ Notes for Cloud / Serverless / Hybrid
Cloud (EKS, AKS, etc.):

Always use Persistent Volumes for Prometheus/InfluxDB.

Use external secret manager (AWS Secrets Manager, Azure Key Vault).

Expose Grafana/Prometheus via Ingress + LoadBalancer.

Serverless:

Prometheus scraping doesn’t work well with short-lived pods → use Pushgateway.

Avoid exporters that need long sessions.

Hybrid:

Split workloads into namespaces (like siem-ltm + siem-event).

Centralize alerts into one Slack/MS Teams channel.

Balance InfluxDB + Prometheus for storage and querying.

🛠️ How to Run
# Clone repository
git clone https://github.com/your-org/siem-monitoring.git
cd siem-monitoring

# Apply monitoring stack
kubectl apply -f manifests/ -n siem-ltm
kubectl apply -f manifests/ -n siem-event

# Port forward for local access
kubectl port-forward svc/prometheus 9090:9090 -n siem-ltm
kubectl port-forward svc/grafana 3000:3000 -n siem-ltm


👉 Then log in to Grafana (localhost:3000) and import the dashboard:
dashboards/Hybrid-SIEM-K8-v2.json

👥 Contributors

Afreen → Grafana dashboard design, alert configuration

Me(Aviral) → Kubernetes pod deployments, Prometheus setup, Telegraf + InfluxDB integration

This file serves as both documentation and a record of every challenge + solution during our SIEM monitoring project.
