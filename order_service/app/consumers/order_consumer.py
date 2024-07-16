from aiokafka import AIOKafkaConsumer
import json
from app import settings
from app.models.order_model import Order
from app.crud.order_crud import add_new_order
from app.deps import get_session


async def consume_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers = bootstrap_servers,
        group_id = settings.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,
        auto_offset_reset = "earliest",
    )
    await consumer.start()
    try:
        async for message in consumer:
            order_data = json.loads(message.value.decode())
            with next(get_session()) as session:
                db_insert_order = add_new_order(Order(**order_data), session)
    finally:
        await consumer.stop()