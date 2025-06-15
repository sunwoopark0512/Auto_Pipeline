```mermaid
flowchart TD
    A[Super Orchestrator] --> B[OSMU Dispatcher]
    B --> C[FFmpeg Renderer] --> D[Shorts Uploaders]
    B --> E[Social Uploaders]
    A -->|WP ID| F[Performance Tracker]
    D & E & F --> G[Analytics Worker]
    G --> H[analytics_log]
    H --> I[Retool KPI Dashboard]
```
