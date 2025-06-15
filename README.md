# Auto Pipeline

This repository contains automation scripts for running keyword pipelines and related tasks.

## Trace Export & Sampling

The tracing module includes a latency filter that only exports spans taking longer than the configured threshold (default `2000ms`). Important events shorter than the threshold can set the `force_export` attribute.

## Opsgenie Routing

Alerts sent to Opsgenie map teams and priority based on the step name and error type.

## Environment Settings

| ENV    | Trace Export Threshold (ms) | Default Sampling Rate | Priority Limit |
|-------|---------------------------|----------------------|----------------|
| dev   | 0                         | 1.0                  | P5             |
| qa    | 500                       | 1.0                  | P4             |
| staging | 2000                    | 0.20                 | P3             |
| prod  | 2000                      | 0.05                 | P1             |
