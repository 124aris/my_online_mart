from fastapi import FastAPI, HTTPException
from app.models.notification_model import Email
from app.crud.notification_crud import send_custom_message
from app.crud.notification_order_crud import send_create_order_message, send_cancel_order_message, send_arrive_order_message, send_shipping_order_message
from app.crud.notification_payment_crud import send_payment_failed_message, send_payment_success_message
from app.crud.notification_user_crud import send_welcome_message, send_verification_message, send_update_user_message

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

@app.post("/manage-notifications/custom", response_model = dict)
async def send_custom_notification(email: Email, emailsubject: str, emailmessage: str):
    message = await send_custom_message(email, emailsubject, emailmessage)
    return message

@app.post("/manage-notifications/order", response_model = dict)
async def send_order_notification(email: Email):
    if email.notification_type == "create_order_message":
        message = await send_create_order_message(email)
    elif email.notification_type == "cancel_order_message":
        message = await send_cancel_order_message(email)
    elif email.notification_type == "arrive_order_message":
        message = await send_arrive_order_message(email)
    elif email.notification_type == "shipping_order_message":
        message = await send_shipping_order_message(email)
    else:
        raise HTTPException(status_code = 404, detail = "Notification Type Not Found")
    return message

app.post("/manage-notifications/payment", response_model = dict)
async def send_payment_notification(email: Email):
    if email.notification_type == "payment_failed_message":
        message = await send_payment_failed_message(email)
    elif email.notification_type == "payment_success_message":
        message = await send_payment_success_message(email)
    else:
        raise HTTPException(status_code = 404, detail = "Notification Type Not Found")
    return message

app.post("/manage-notifications/user", response_model = dict)
async def send_user_notification(email: Email):
    if email.notification_type == "welcome_message":
        message = await send_welcome_message(email)
    elif email.notification_type == "verification_message":
        message = await send_verification_message(email)
    elif email.notification_type == "update_user_message":
        message = await send_update_user_message(email)
    else:
        raise HTTPException(status_code = 404, detail = "Notification Type Not Found")
    return message