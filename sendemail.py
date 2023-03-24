from typing import List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import BaseModel, EmailStr
from models import User
import jwt



# class EmailSchema(BaseModel):
#     email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME ="bismarkotu1006@gmail.com",
    MAIL_PASSWORD = "nana_akua1975.com",
    MAIL_FROM = "bismarkotu1006@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)




async def send_email(email: List, instance: User):

    token_data = {
        "id": instance.id,
        "username": instance.username
    }

    token = jwt.encode(token_data, "e9b684988b11fc27d0f2e00bf7cfa45b6c4b97a2", algorithm='HS256')


    template = f"""
        <!doctype html>
        <html lang="en">
            <head>
                <title>Verify Account</title>
            </head>

            <body>
                <div style="display:flex;align-items:center;justify-content:center;flex-direction:column;">
                    <h3>Account Verification</h3>
                    <br>

                    <p>Please click on the button below to verify your account</p>

                    <a style="margin-top:1rem;padding:1rem;border-radius:0.5rem;font-size:1rem;text-decoration:none;
                    background: #0275d8; color:white;" href="http://localhost:8000/verification/?token={token}">
                    Verify your email
                    </a>

                    <p>Please kindly Ignore this email if you did not register for FASTAPI Ecormerce</p>
                </div>

            </body>
        </html>
    """



    msg = MessageSchema(
        subject = "FASTAPI Ecormerce",
        recipients= email, #List of recipients emails
        body = template,
        subtype="html"
    )


    fm = FastMail(conf)
    await fm.send_message(message=msg)





