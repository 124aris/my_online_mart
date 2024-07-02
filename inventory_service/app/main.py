from contextlib import asynccontextmanager
from typing import Annotated
from sqlmodel import Session, SQLModel
from fastapi import FastAPI, Depends, HTTPException
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer
import asyncio
import json
from app.db_engine import engine
from app.models.inventory_model import InventoryItem, InventoryItemUpdate
from app.crud.inventory_crud import delete_inventory_item_by_id, get_all_inventory_items, get_inventory_item_by_id, update_inventory_item_by_id
from app.deps import get_session, get_kafka_producer
from app.consumers.add_stock_consumer import consume_messages


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    task = asyncio.create_task(consume_messages("inventory-add-stock-response", 'broker:19092'))
    create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan, title = "Inventory Service",
    version = "0.0.1",
    servers = [
        {
            "url": "http://127.0.0.1:8000",
            "description": "Development Server"
        }
    ]
)

@app.get("/")
def read_root():
    return {"Hello": "Inventory Service"}

@app.post("/manage-inventory/", response_model = InventoryItem)
async def create_new_inventory_item(item: InventoryItem, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):

    item_dict = {field: getattr(item, field) for field in item.dict()}
    item_json = json.dumps(item_dict).encode("utf-8")
    await producer.send_and_wait("AddStock", item_json)
    return item

@app.get("/manage-inventory/all", response_model = list[InventoryItem])
def all_inventory_items(session: Annotated[Session, Depends(get_session)]):
    return get_all_inventory_items(session)

@app.get("/manage-inventory/{item_id}", response_model = InventoryItem)
def single_inventory_item(item_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return get_inventory_item_by_id(inventory_item_id = item_id, session = session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.delete("/manage-inventory/{item_id}", response_model = dict)
def delete_single_inventory_item(item_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return delete_inventory_item_by_id(inventory_item_id = item_id, session = session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.patch("/manage-inventory/{item_id}", response_model = InventoryItem)
def update_single_inventory_item(item_id: int, item: InventoryItemUpdate, session: Annotated[Session, Depends(get_session)]):
    try:
        return update_inventory_item_by_id(item_id, item, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))