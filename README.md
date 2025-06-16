# Auto Pipeline

This repository contains scripts used to run the automated pipeline.

## Resource Monitoring

Resource usage (CPU and memory) can be captured during pipeline execution.
Set the environment variable `ENABLE_MONITORING=true` before running
`run_pipeline.py` to enable monitoring. Metrics will be written to
`logs/resource_monitor.log`.

Monitoring is disabled by default if the variable is unset or set to any
other value.
