from aiokafka import AIOKafkaConsumer
import json
from app import settings
from app.models.product_model import Product
from app.crud.product_crud import add_new_product
from app.deps import get_session


async def consume_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers = bootstrap_servers,
        group_id = settings.KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT,
        auto_offset_reset = "earliest",
    )
    await consumer.start()
    try:
        async for message in consumer:
            product_data = json.loads(message.value.decode())
            with next(get_session()) as session:
                db_insert_product = add_new_product(Product(**product_data), session)
    finally:
        await consumer.stop()