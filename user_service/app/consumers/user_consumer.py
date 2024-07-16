from aiokafka import AIOKafkaConsumer
import json
from app import settings
from app.models.user_model import User
from app.crud.user_crud import add_new_user
from app.deps import get_session

async def consume_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers = bootstrap_servers,
        group_id = settings.KAFKA_CONSUMER_GROUP_ID_FOR_USER,
        auto_offset_reset = "earliest",
    )
    await consumer.start()
    try:
        async for message in consumer:
            user_data = json.loads(message.value.decode())
            with next(get_session()) as session: 
                add_new_user(User(**user_data), session)
    finally:
        await consumer.stop()