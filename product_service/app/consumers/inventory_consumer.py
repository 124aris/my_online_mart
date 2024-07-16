from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
from app import settings
from app.crud.product_crud import validate_product_by_id
from app.deps import get_session
from app.hello_ai import chat_completion

async def consume_inventory_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers = bootstrap_servers,
        group_id = settings.KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY,
        auto_offset_reset = "earliest",
    )
    await consumer.start()
    try:
        async for message in consumer:
            inventory_data = json.loads(message.value.decode())
            product_id = inventory_data["product_id"]
            with next(get_session()) as session:
                product = validate_product_by_id(product_id, session)
                if product is None:
                    email_body = chat_completion(f"Admin has Sent InCorrect Product. Write Email to Admin {product_id}")
                if product is not None:
                    producer = AIOKafkaProducer(bootstrap_servers = settings.BOOTSTRAP_SERVER)
                    await producer.start()
                    try:
                        await producer.send_and_wait(settings.KAFKA_INVENTORY_RESPONSE_TOPIC, message.value)
                    finally:
                        await producer.stop()
    finally:
        await consumer.stop()