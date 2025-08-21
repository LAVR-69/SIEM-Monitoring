from prometheus_client import start_http_server, Gauge
import psutil
import time


# Metrics
endpoint_gauge = Gauge('endpoints_connected', 'Number of endpoints connected')
network_gauge = Gauge('network_bytes_sent', 'Network bytes sent')

def collect_metrics():
    # Endpoint (example: 2 users)
    endpoint_gauge.set(2)

    # Network
    net = psutil.net_io_counters()
    network_gauge.set(net.bytes_sent)

if __name__ == "__main__":
    start_http_server(9101)  # Single port for all metrics
    while True:
        collect_metrics()
        time.sleep(5)

