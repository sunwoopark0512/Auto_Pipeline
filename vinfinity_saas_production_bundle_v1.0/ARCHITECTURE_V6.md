```mermaid
flowchart TD
    subgraph Data&ML
      BigQuery--dbt-->Snowflake
      Kafka --> Personalize
      Personalize --> Frontend
    end
    subgraph Ops
      PromExporter-->Prometheus-->Grafana
      Prometheus-->GPUCostGovernor
      Sentry-->Slack
    end
    FeatureFlags-->Pipeline
    PrivacyAPI-->DB
```
