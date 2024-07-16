from contextlib import asynccontextmanager
from typing import Annotated
from sqlmodel import Session, SQLModel
from fastapi import FastAPI, Depends, HTTPException
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer
import asyncio
import json
from app import settings
from app.db_engine import engine
from app.models.order_model import Order, OrderUpdate
from app.crud.order_crud import get_all_orders, get_order_by_id, delete_order_by_id, update_order_by_id
from app.deps import get_session, get_kafka_producer
from app.consumers.order_consumer import consume_messages

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    task = asyncio.create_task(consume_messages(settings.KAFKA_ORDER_TOPIC, settings.BOOTSTRAP_SERVER))
    create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan, title = "Order Service",
    version = "0.0.1",
    servers = [
        {
            "url": "http://127.0.0.1:8002",
            "description": "Development Server"
        }
    ]
)

@app.get("/")
def read_root():
    return {"Hello": "Order Service"}

@app.post("/manage-orders/", response_model = Order)
async def create_new_order(order: Order, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    order_dict = {field: getattr(order, field) for field in order.dict()}
    order_json = json.dumps(order_dict).encode("utf-8")
    await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, order_json)
    return order

@app.get("/manage-orders/all", response_model = list[Order])
def call_all_orders(session: Annotated[Session, Depends(get_session)]):
    return get_all_orders(session)

@app.get("/manage-orders/{order_id}", response_model = Order)
def get_single_order(order_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return get_order_by_id(order_id, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@app.delete("/manage-orders/{order_id}", response_model = dict)
def delete_single_order(order_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return delete_order_by_id(order_id, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.patch("/manage-orders/{order_id}", response_model = Order)
def update_single_order(order_id: int, order: OrderUpdate, session: Annotated[Session, Depends(get_session)]):
    try:
        return update_order_by_id(order_id, order, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))