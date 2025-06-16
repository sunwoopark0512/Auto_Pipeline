# Auto Pipeline Monitoring Setup

This project exposes Prometheus metrics for each major script and writes logs to `logs/`. Example Prometheus and Logstash configuration files are provided in `config/`.

## Systemd
Use `auto-pipeline.service` to run the pipeline as a service. A simple health check script `health_check.sh` can be used for monitoring and alerting.
