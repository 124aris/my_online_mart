from app.models.notification_model import Email
from fastapi import FastAPI
from app.crud.notification_crud import send_custom_message

app = FastAPI(title = "Notification Service",
    version = "0.0.1",
    servers = [
        {
            "url": "http://127.0.0.1:8001",
            "description": "Development Server"
        }
    ]
)

@app.get("/")
def read_root():
    return {"Hello": "Notification Service"}

@app.post("/manage_notifications/custom", response_model = dict)
async def send_custom_notification(email: Email, emailsubject: str, emailmessage: str):
    message = await send_custom_message(email, emailsubject, emailmessage)
    return message