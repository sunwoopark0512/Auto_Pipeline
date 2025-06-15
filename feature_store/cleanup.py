import os
import time
import boto3

ddb = boto3.client("dynamodb", region_name="ap-northeast-2")
TABLE = os.getenv("FEAST_TABLE", "feast-vinfinity")


def cleanup():
    paginator = ddb.scan(TableName=TABLE, ProjectionExpression="entity_id, ttl")
    for item in paginator.get("Items", []):
        if int(item["ttl"]["N"]) < time.time():
            ddb.delete_item(TableName=TABLE, Key={"entity_id": item["entity_id"]})
