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
from app.models.payment_model import Payment
from app.crud.payment_crud import get_payment_by_id
from app.deps import get_session, get_kafka_producer
from app.consumers.payment_consumer import consume_messages

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    task = asyncio.create_task(consume_messages(settings.KAFKA_PAYMENT_TOPIC, settings.BOOTSTRAP_SERVER))
    create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan, title = "Payment Service",
    version = "0.0.1",
    servers = [
        {
            "url": "http://127.0.0.1:8003",
            "description": "Development Server"
        }
    ]
)

@app.get("/")
def read_root():
    return {"Hello": "Payment Service"}

@app.post("/manage-payments/", response_model = Payment)
async def create_new_payment(payment: Payment, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    payment_dict = {field: getattr(payment, field) for field in payment.dict()}
    payment_json = json.dumps(payment_dict).encode("utf-8")
    await producer.send_and_wait(settings.KAFKA_PAYMENT_TOPIC, payment_json)
    return payment

@app.get("/manage-payments/{payment_id}", response_model = Payment)
def get_single_payment(payment_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return get_payment_by_id(payment_id, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))