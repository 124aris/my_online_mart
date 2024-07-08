from app.models.notification_payment_model import payment_success_message, payment_failed_message
from app.models.notification_model import Email
from fastapi_mail import MessageSchema, MessageType, FastMail
from app.mail_config import conf

async def send_payment_success_message(email: Email, emailmessage = payment_success_message):
    message = MessageSchema(
        subject = "My Online Mart Payment Successful",
        recipients = email.dict().get("email"),
        body = emailmessage,
        subtype = MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"Message": "Payment Successful Email Has Been Sent"}

async def send_payment_failed_message(email: Email, emailmessage = payment_failed_message):
    message = MessageSchema(
        subject = "My Online Mart Payment Failed",
        recipients = email.dict().get("email"),
        body = emailmessage,
        subtype = MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"Message": "Payment Failed Email Has Been Sent"}