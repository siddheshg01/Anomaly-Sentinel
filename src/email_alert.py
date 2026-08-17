import os

import smtplib

from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


def send_email_alert(
    subject,
    body
):

    sender = os.getenv(
        "EMAIL_SENDER"
    )

    password = os.getenv(
        "EMAIL_PASSWORD"
    )

    receiver = os.getenv(
        "EMAIL_RECEIVER"
    )

    smtp_server = os.getenv(
        "SMTP_SERVER",
        "smtp.gmail.com"
    )

    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "465"
        )
    )

    if not sender:

        print(
            "Email sender is not configured."
        )

        return False

    if not password:

        print(
            "Email password is not configured."
        )

        return False

    if not receiver:

        print(
            "Email receiver is not configured."
        )

        return False

    message = EmailMessage()

    message["From"] = sender

    message["To"] = receiver

    message["Subject"] = subject

    message.set_content(
        body
    )

    try:

        with smtplib.SMTP_SSL(

            smtp_server,

            smtp_port

        ) as server:

            server.login(

                sender,

                password

            )

            server.send_message(
                message
            )

        return True

    except Exception as error:

        print(
            f"Email error: {error}"
        )

        return False