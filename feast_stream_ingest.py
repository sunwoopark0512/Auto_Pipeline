import aiokafka

KAFKA_BROKERS = "localhost:9092"

producer = aiokafka.AIOKafkaProducer(
    bootstrap_servers=KAFKA_BROKERS,
    transactional_id="vinfinity-producer",
    enable_idempotence=True,
    acks="all",
)

async def ingest(msg):
    await producer.start_transaction()
    await producer.send_and_wait("vinfinity.events", msg.encode())
    await producer.commit_transaction()
