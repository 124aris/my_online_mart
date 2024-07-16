from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
from sqlmodel import Session, SQLModel
from fastapi import FastAPI, Depends, HTTPException
from aiokafka import AIOKafkaProducer
import asyncio
import json
from app import settings
from app.db_engine import engine
from app.models.user_model import User, UserUpdate
from app.crud.user_crud import get_all_users, get_user_by_id, delete_user_by_id, update_user_by_id
from app.deps import get_session, get_kafka_producer
from app.consumers.user_consumer import consume_messages
from jose import JWTError
from datetime import timedelta
from app.crud.auth_crud import create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    task = asyncio.create_task(consume_messages(settings.KAFKA_USER_TOPIC, settings.BOOTSTRAP_SERVER))
    create_db_and_tables()
    yield

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

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

@app.post("/manage-users/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]):
    user_in_db = User.get(form_data.username)
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Incorrect username")
    if not form_data.password == user_in_db["password"]:
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token_expires = timedelta(minutes=1)
    access_token = create_access_token(subject = user_in_db["username"], expires_delta = access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "expires_in": access_token_expires.total_seconds() }

@app.get("/manage-users/get-access-token")
def get_access_token(user_name: str):
    access_token_expires = timedelta(minutes = 1)
    access_token = create_access_token(subject = user_name, expires_delta = access_token_expires)
    return {"access_token": access_token}

@app.get("/manage-users/decode_token")
def decoding_token(access_token: str):
    try:
        decoded_token_data = decode_access_token(access_token)
        return {"decoded_token": decoded_token_data}
    except JWTError as e:
        return {"error": str(e)}

@app.get("/manage-users/me")
def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    user_token_data = decode_access_token(token)
    user_in_db = User.get(user_token_data["sub"])
    return user_in_db

@app.post("/manage-users/", response_model = User)
async def create_new_user(user: User, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
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