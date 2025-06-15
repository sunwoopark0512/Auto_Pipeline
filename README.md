# Auto Pipeline

This repository contains scripts and utilities for automating content generation and uploading to Notion.

### KPI Feedback Module
```python
from analytics.kpi_feedback import generate_feedback

kpi = {
    "click_through_rate": 7.8,
    "engagement_rate": 4.5,
    "watch_time": 15,
    "conversion_rate": 1.2
}
print(generate_feedback(kpi))
# → {'feedback': [...], 'needed': True}
```
