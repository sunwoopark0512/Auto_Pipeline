from feast import KafkaSource, PushSource, FileSource
from feast.data_format import JsonFormat
from datetime import timedelta

event_kafka = KafkaSource(
    name="event_kafka",
    bootstrap_servers="${KAFKA_BROKERS}",
    topic="vinfinity.events",
    timestamp_field="occurred_at",
    message_format=JsonFormat(),
)

conversion_file = FileSource(
    path="file:///app/data/conversions.parquet",
    timestamp_field="occurred_at",
)
