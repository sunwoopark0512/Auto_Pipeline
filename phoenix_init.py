from phoenix.alerting import AlertManager
from llm_monitor.phoenix_alert import alert

# Register alerting rules for LLM monitoring
AlertManager.add_yaml("llm_monitor/phoenix_rules.yaml", callback=alert)
