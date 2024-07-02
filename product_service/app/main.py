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
from app.models.product_model import Product, ProductUpdate
from app.crud.product_crud import get_all_products, get_product_by_id, delete_product_by_id, update_product_by_id
from app.deps import get_session, get_kafka_producer
from app.consumers.product_consumer import consume_messages
from app.consumers.inventory_consumer import consume_inventory_messages
from app.hello_ai import chat_completion

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    task = asyncio.create_task(consume_messages(settings.KAFKA_PRODUCT_TOPIC, 'broker:19092'))
    asyncio.create_task(consume_inventory_messages("AddStock", 'broker:19092'))
    create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan, title = "Product Service", 
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8004",
            "description": "Development Server"
        }
        ]
    )

@app.get("/")
def read_root():
    return {"Hello": "Product Service"}

@app.post("/manage-products/", response_model = Product)
async def create_new_product(product: Product, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    product_dict = {field: getattr(product, field) for field in product.dict()}
    product_json = json.dumps(product_dict).encode("utf-8")
    await producer.send_and_wait(settings.KAFKA_PRODUCT_TOPIC, product_json)
    return product

@app.get("/manage-products/all", response_model = list[Product])
def call_all_products(session: Annotated[Session, Depends(get_session)]):
    return get_all_products(session)

@app.get("/manage-products/{product_id}", response_model = Product)
def get_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return get_product_by_id(product_id, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@app.delete("/manage-products/{product_id}", response_model = dict)
def delete_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return delete_product_by_id(product_id, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.patch("/manage-products/{product_id}", response_model = Product)
def update_single_product(product_id: int, product: ProductUpdate, session: Annotated[Session, Depends(get_session)]):
    try:
        return update_product_by_id(product_id, product, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@app.get("/hello-ai")
def get_ai_response(prompt:str):
    return chat_completion(prompt)