🚀 Project Overview

We built a hybrid SIEM (Security Information & Event Management) stack deployed on Kubernetes.

Afreen focused on dashboard design and alert configuration inside Grafana.

[Your Name] handled Kubernetes pod deployments, Prometheus setup, and scraping/InfluxDB integration.

The goal:

Collect metrics (CPU, memory, network, disk, custom tests).

Visualize them in Grafana dashboards.

Trigger alerts (via Slack) when thresholds were breached.

Test under hybrid setups (local pods, cloud-ready configs, serverless considerations).

📂 Project Structure
siem-monitoring/
├── manifests/           # All Kubernetes YAML files (deployments, services, configmaps)
├── dashboards/          # Exported Grafana dashboards (JSON)
├── alerts/              # Grafana/Prometheus alert rules
├── telegraf/            # Telegraf configs for InfluxDB
├── README.md            # This file (full documentation)

🏗️ Setup Process (Step by Step)
1. Kubernetes Namespaces

We isolated components into two namespaces for clarity:

siem-ltm → Prometheus, Grafana, exporters

siem-event → InfluxDB, Telegraf, iperf-client

apiVersion: v1
kind: Namespace
metadata:
  name: siem-ltm
---
apiVersion: v1
kind: Namespace
metadata:
  name: siem-event

2. Prometheus Deployment

Deployed in siem-ltm.

Scrapes node-exporter, endpoint-exporter, and custom metrics.

Configured prometheus.yml inside a ConfigMap.

apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: siem-ltm
data:
  prometheus.yml: |
    scrape_configs:
      - job_name: 'node'
        static_configs:
          - targets: ['node-exporter:9100']

3. Grafana Deployment

Deployed in siem-ltm.

Datasources: Prometheus + InfluxDB.

Dashboards stored in JSON (dashboards/Hybrid-SIEM-K8-v2.json).

4. InfluxDB + Telegraf

Deployed in siem-event.

Telegraf scrapes system metrics + iperf tests, pushes to InfluxDB.

5. Exporters

Node Exporter → for CPU, memory, disk, network.

Endpoint Exporter → for custom service monitoring.

iPerf → for active network throughput testing.

6. Alerts

Alerts configured in Grafana with Prometheus queries.

Notifications routed to Slack.

Examples:

Memory Alert
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) 
  / node_memory_MemTotal_bytes * 100 > 80

Network Alert
rate(node_network_receive_bytes_total[1m]) > 1000000
or
rate(node_network_transmit_bytes_total[1m]) > 1000000


Slack notifications were verified successfully.

7. Dashboard

Dashboard: Hybrid SIEM K8 v.2 (JSON exported in dashboards/).

Panels: CPU, Memory, Disk I/O, Network, Custom tests.

Designed by Afreen.

⚔️ Challenges & Fixes
Problem	What Happened	Fix
Redash crash	UI broke after restart	Restarted from scratch, cleaned DB
Pod stuck in Creating	Wrong file name usb.py shadowed dependency	Renamed file
Empty Grafana data	Datasource misconfigured	Fixed Prometheus/Influx endpoints
Slow Slack alerts	Delay in firing	Tweaked evaluation interval
iperf missing	Pod failed (executable not found)	Built iperf client/server images
🌩️ Notes for Cloud / Serverless / Hybrid

Cloud (EKS/AKS/others):

Use persistent volumes for Prometheus & InfluxDB.

External secret manager for credentials.

Serverless:

Prometheus scraping must be externalized (use Prometheus + Pushgateway).

Not ideal for long-running exporters.

Hybrid:

Split monitoring namespaces (as we did).

Route alerts to unified Slack/MS Teams channel.

🛠️ How to Run

Clone repo:

git clone https://github.com/your-org/siem-monitoring.git
cd siem-monitoring


Apply manifests:

kubectl apply -f manifests/ -n siem-ltm
kubectl apply -f manifests/ -n siem-event


Port forward Prometheus/Grafana:

kubectl port-forward svc/prometheus 9090:9090 -n siem-ltm
kubectl port-forward svc/grafana 3000:3000 -n siem-ltm


Import dashboards (dashboards/Hybrid-SIEM-K8-v2.json) into Grafana.

👥 Contributors

Afreen → Dashboard design, alert setup.

[Your Name] → Kubernetes deployments, Prometheus, scraping, InfluxDB integration.

📜 License

MIT – free to use, share, improve.
