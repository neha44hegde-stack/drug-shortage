import smtplib
from email.message import EmailMessage


def send_email(medicine, stock, reorder):

    sender = "angelbeulahk@gmail.com"
    password = "owbw anzv sncv jvfx"

    receiver = sender

    msg = EmailMessage()

    msg["Subject"] = "🚨 Low Stock Alert"

    msg["From"] = sender
    msg["To"] = receiver

    msg.set_content(f"""
Medicine: {medicine}

Current Stock: {stock}

Reorder Level: {reorder}

Please restock this medicine immediately.

AI Pharmacy Management System
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)