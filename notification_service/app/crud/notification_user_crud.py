from app.models.notification_user_model import welcome_message, verification_message, update_user_message
from app.models.notification_model import Email
from fastapi_mail import MessageSchema, MessageType, FastMail
from app.mail_config import conf

async def send_welcome_message(email: Email, emailmessage = welcome_message):
    message = MessageSchema(
        subject = "Welcome to My Online Mart",
        recipients = email.dict().get("email"),
        body = emailmessage,
        subtype = MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"Message": "Welcome Email Has Been Sent"}

async def send_verification_message(email: Email, emailmessage = verification_message):
    message = MessageSchema(
        subject = "My Online Mart User Verification",
        recipients = email.dict().get("email"),
        body = emailmessage,
        subtype = MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"Message": "User Verification Email Has Been Sent"}

async def send_update_user_message(email: Email, emailmessage = update_user_message):
    message = MessageSchema(
        subject = "My Online Mart User Updated",
        recipients = email.dict().get("email"),
        body = emailmessage,
        subtype = MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"Message": "User Updated Email Has Been Sent"}