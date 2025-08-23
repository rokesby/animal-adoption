import os
from flask import current_app, jsonify
import sendgrid
from sendgrid.helpers.mail import *

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")


def send_verification_email(recipient, pin, token):
    verification_link = f"http://localhost:5173/verify?token={token}"
    
    current_env = os.getenv("ENV")
    
    if current_env == 'development':
        print("development env")
        recipient = os.getenv("SENDGRID_TEST_RECIPIENT")
   
    
    content = Content("text/html", f"""
    <p>Your verification PIN is: <strong>{pin}</strong></p>
    <p>Please confirm your account by clicking the link below:</p>
    <p><a href="{verification_link}">{verification_link}> Click here to verify </a></p>
    """)

    mail = Mail(
        from_email=Email('mattwilkesdev@gmail.com'),
        to_emails=To(recipient),
        subject='Verify Your Email',
        html_content=content
    )

    try:
        print("attempting to send email")
        sg=sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(f'finished sending email: {response.status_code}')
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {e}")
        raise