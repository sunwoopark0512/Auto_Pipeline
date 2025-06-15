import json, os, asyncio, aiokafka, redis

KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "kafka:9092").split(",")
r = redis.Redis(host="redis", port=6379)

async def stream():
    consumer = aiokafka.AIOKafkaConsumer(
        "vinfinity.events",
        bootstrap_servers=KAFKA_BROKERS,
        value_deserializer=lambda v: json.loads(v.decode())
    )
    await consumer.start()
    async for msg in consumer:
        evt = msg.value
        uid = evt["user_id"]
        key = f"user:{uid}:5m"
        if evt["event"] == "view":   r.hincrby(key, "views_5m", 1)
        if evt["event"] == "click":  r.hincrby(key, "clicks_5m", 1)
        r.expire(key, 3600)
    await consumer.stop()

asyncio.run(stream())
