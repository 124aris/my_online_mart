from app.models.notification_order_model import create_order_message, shipping_order_message, arrive_order_message, cancel_order_message
from app.models.notification_model import Email
from fastapi_mail import MessageSchema, MessageType, FastMail
from app.mail_config import configuration

async def send_create_order_message(email: Email, emailmessage = create_order_message):
    message = MessageSchema(
        subject = "My Online Mart Order Created",
        recipients = email.dict().get("email"),
        body = emailmessage,
        subtype = MessageType.html
    )
    fm = FastMail(configuration)
    await fm.send_message(message)
    return {"Message": "Order Created Email Has Been Sent"}

async def send_shipping_order_message(email: Email, emailmessage = shipping_order_message):
    message = MessageSchema(
        subject = "My Online Mart Order Shipped",
        recipients = email.dict().get("email"),
        body = emailmessage,
        subtype = MessageType.html
    )
    fm = FastMail(configuration)
    await fm.send_message(message)
    return {"Message": "Order Shipped Email Has Been Sent"}

async def send_arrive_order_message(email: Email, emailmessage = arrive_order_message):
    message = MessageSchema(
        subject = "My Online Mart Order Arrived",
        recipients = email.dict().get("email"),
        body = emailmessage,
        subtype = MessageType.html
    )
    fm = FastMail(configuration)
    await fm.send_message(message)
    return {"Message": "Order Arrived Email Has Been Sent"}

async def send_cancel_order_message(email: Email, emailmessage = cancel_order_message):
    message = MessageSchema(
        subject = "My Online Mart Order Canceled",
        recipients = email.dict().get("email"),
        body = emailmessage,
        subtype = MessageType.html
    )
    fm = FastMail(configuration)
    await fm.send_message(message)
    return {"Message": "Order Canceled Email Has Been Sent"}