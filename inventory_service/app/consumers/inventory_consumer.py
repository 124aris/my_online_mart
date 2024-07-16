from aiokafka import AIOKafkaConsumer
import json
from app import settings
from app.deps import get_session
from app.crud.inventory_crud import add_new_inventory_item
from app.models.inventory_model import InventoryItem

async def consume_messages(topic, bootstrap_servers):
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
            with next(get_session()) as session:
                db_insert_product = add_new_inventory_item(InventoryItem(**inventory_data), session)
    finally:
        await consumer.stop()