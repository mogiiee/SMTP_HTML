from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()


app = FastAPI()
my_email = os.environ.get("MAIL_USERNAME")
my_password = os.environ.get("MAIL_PASSWORD")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return HTMLResponse('''
         <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Contact Me</title>
        </head>
        <body>
            <h1>Contact Me</h1>
            <form method="post" action="/send_email">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br>
                <label for="email">Email:</label><br>
                <input type="email" id="email" name="email" required><br>
                <label for="subject">Subject:</label><br>
                <input type="text" id="subject" name="subject" required><br>
                <label for="message">Message:</label><br>
                <textarea id="message" name="message" required></textarea><br>
                <input type="submit" value="Send">
            </form>
        </body>
        </html>
    ''')

@app.post("/send_email", response_class=HTMLResponse)
async def send_email(name: str = Form(...), email: str = Form(...), subject: str = Form(...), message: str = Form(...)):
    
    # create email message
    email_message = EmailMessage()
    email_message['From'] = email
    email_message['To'] = 'singhananya2002@gmail.com' # replace with your email address
    email_message['Subject'] = subject
    email_message.set_content(f"Name: {name}\nEmail: {email}\n\n{message}")
    print(my_email,my_password)
    print(email_message['From'])
    # send email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(my_email, my_password) # replace with your email address and password
        smtp.send_message(email_message)

    
    return HTMLResponse('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Message Sent</title>
        </head>
        <body>
            <h1>Message Sent</h1>
            <p>Your message has been sent successfully.</p>
        </body>
        </html>
    ''')




# from fastapi import FastAPI
# from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
# from starlette.requests import Request
# from starlette.responses import JSONResponse
# from pydantic import EmailStr, BaseModel
# from typing import List
# app = FastAPI()