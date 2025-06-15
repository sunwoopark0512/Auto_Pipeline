from feast import Entity, FeatureView, Field, ValueType
from feast.types import Float32, Int64
from data_sources import event_kafka
from datetime import timedelta

user = Entity(name="user_id", join_keys=["user_id"])

event_features = FeatureView(
    name="user_events_5m",
    entities=[user],
    ttl=timedelta(hours=1),
    schema=[
        Field(name="views_5m", dtype=Int64),
        Field(name="clicks_5m", dtype=Int64),
    ],
    source=event_kafka,
    timestamp_field="occurred_at",
)
