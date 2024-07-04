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
from app.models.user_model import User, UserUpdate
from app.crud.user_crud import get_all_users, get_user_by_id, delete_user_by_id, update_user_by_id
from app.deps import get_session, get_kafka_producer
from app.consumers.user_consumer import consume_messages

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    task = asyncio.create_task(consume_messages(settings.KAFKA_USER_TOPIC, 'broker:19092'))
    create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan, title = "User Service",
    version = "0.0.1",
    servers = [
        {
            "url": "http://127.0.0.1:8005",
            "description": "Development Server"
        }
    ]
)

@app.get("/")
def read_root():
    return {"Hello": "User Service"}

@app.post("/manage-users/", response_model = User)
async def create_new_user(user: User, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    user_dict = {field: getattr(user, field) for field in user.dict()}
    user_json = json.dumps(user_dict).encode("utf-8")
    await producer.send_and_wait(settings.KAFKA_USER_TOPIC, user_json)
    return user

@app.get("/manage-users/all", response_model = list[User])
def call_all_users(session: Annotated[Session, Depends(get_session)]):
    return get_all_users(session)

@app.get("/manage-users/{user_id}", response_model = User)
def get_single_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return get_user_by_id(user_id, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.delete("/manage-users/{user_id}", response_model = dict)
def delete_single_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    try:
        return delete_user_by_id(user_id, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.patch("/manage-users/{user_id}", response_model = User)
def update_single_user(user_id: int, user: UserUpdate, session: Annotated[Session, Depends(get_session)]):
    try:
        return update_user_by_id(user_id, user, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))