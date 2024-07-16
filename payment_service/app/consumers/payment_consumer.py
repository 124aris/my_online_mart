from aiokafka import AIOKafkaConsumer
import json
from app import settings
from app.models.payment_model import Payment
from app.crud.payment_crud import create_new_payment
from app.deps import get_session

async def consume_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers = bootstrap_servers,
        group_id = settings.KAFKA_CONSUMER_GROUP_ID_FOR_PAYMENT,
        auto_offset_reset = "earliest",
    )
    await consumer.start()
    try:
        async for message in consumer:
            payment_data = json.loads(message.value.decode())
            with next(get_session()) as session:
                db_insert_payment = create_new_payment(Payment(**payment_data), session)
    finally:
        await consumer.stop()