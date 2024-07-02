from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
from app.crud.product_crud import validate_product_by_id
from app.deps import get_session
from app.hello_ai import chat_completion

async def consume_inventory_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="inventory-add-group",
        # auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for message in consumer:
            print("\n\n RAW INVENTORY MESSAGE\n\n ")
            print(f"Received message on topic {message.topic}")
            print(f"Message Value {message.value}")
            inventory_data = json.loads(message.value.decode())
            product_id = inventory_data["product_id"]
            print("PRODUCT ID", product_id)
            with next(get_session()) as session:
                product = validate_product_by_id(
                    product_id=product_id, session=session)
                print("PRODUCT VALIDATION CHECK", product)
                if product is None:
                    email_body = chat_completion(f"Admin has Sent InCorrect Product. Write Email to Admin {product_id}")
                if product is not None:
                    print("PRODUCT VALIDATION CHECK NOT NONE")
                    producer = AIOKafkaProducer(
                        bootstrap_servers='broker:19092')
                    await producer.start()
                    try:
                        await producer.send_and_wait(
                            "inventory-add-stock-response",
                            message.value
                        )
                    finally:
                        await producer.stop()
    finally:
        await consumer.stop()