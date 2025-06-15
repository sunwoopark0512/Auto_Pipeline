from phoenix.alerting import AlertManager
from llm_monitor.phoenix_alert import alert

# Register Phoenix rules for monitoring
AlertManager.add_yaml("llm_monitor/phoenix_rules.yaml", callback=alert)
