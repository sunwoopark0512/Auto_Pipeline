from feast import Entity, FeatureView, Field, FileSource
from feast.types import Int64, Float32
from data_sources import conversion_file
from datetime import timedelta

user = Entity(name="user_id", join_keys=["user_id"])

conversion_features = FeatureView(
    name="user_conversion_stats",
    entities=[user],
    ttl=timedelta(days=90),
    schema=[
        Field(name="total_revenue", dtype=Float32),
        Field(name="purchases", dtype=Int64),
    ],
    source=conversion_file,
    timestamp_field="occurred_at",
)
