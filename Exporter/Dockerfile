FROM python:3.12-slim
WORKDIR /app
COPY endpoint_exporter.py /app/endpoint_exporter.py
RUN pip install --no-cache-dir prometheus_client psutil
EXPOSE 9101
CMD ["python", "/app/endpoint_exporter.py"]

