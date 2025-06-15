```mermaid
flowchart TD
    GPT-->Phoenix
    User-->CloudflareWorker-->A/B_Page
    Phoenix-->Prometheus-->Grafana
    BigQuery--train-->WandB
    FeastRedis-->DynamoDB
    DynamoDB-->PersonalizationService
```
