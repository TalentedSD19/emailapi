from fastapi import FastAPI, HTTPException, Form
import smtplib
from email.message import EmailMessage
import ssl
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Email(BaseModel):
    receiver: str
    subject: str
    body: str


class Email2(BaseModel):
    sender: str
    password: str
    receiver: str
    subject: str
    body: str


@app.get('/')
def index():
    return {'Email API': 'API server has started','Version':'1.0.0','Author1':'Soumyajit Datta','Author2':'Jeet Nandigrami'}


@app.post('/sendmail/setsender')
async def sendmail(sender: str = Form(...), password: str = Form(...), receiver: str = Form(...), subject: str = Form(...),
                   body: str = Form(...)):
    email = Email2(sender=sender, password=password, receiver=receiver,
                   subject=subject, body=body)
    email_sender = email.sender
    email_password = email.password

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email.receiver
    em['Subject'] = email.subject
    em.set_content(email.body)

    context = ssl.create_default_context()

    try:

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email.receiver, em.as_string())
            return {'status': "mail sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/sendmail/')
async def sendmail(receiver: str = Form(...), subject: str = Form(...),
                   body: str = Form(...)):
    email = Email(receiver=receiver,
                  subject=subject, body=body)
    email_sender = 'imposters.contact@gmail.com'
    email_password = 'ehlevyqprdwvbsnv'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email.receiver
    em['Subject'] = email.subject
    em.set_content(email.body)

    context = ssl.create_default_context()

    try:

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email.receiver, em.as_string())
            return {'status': "mail sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
