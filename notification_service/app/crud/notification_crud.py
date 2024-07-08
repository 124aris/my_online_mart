from app.models.notification_model import Email
from fastapi_mail import MessageSchema, MessageType, FastMail
from app.mail_config import conf

def create_custom_message(message: str):
    custom_message = f"""
        <html>
        <body>
        <h1>My Online Mart</h1>
        <p>{message}</p>
        </body>
        </html>
        """
    return custom_message

async def send_custom_message(email: Email, emailsubject: str, emailmessage: str):
    custom_message = create_custom_message(emailmessage)
    message = MessageSchema(
        subject = emailsubject,
        recipients = email.dict().get("email"),
        body = custom_message,
        subtype = MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"Message": f"{emailsubject} Email Has Been Sent"}