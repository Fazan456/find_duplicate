import os.path
import base64
from email.mime.multipart import MIMEMultipart
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request



SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

def create_message(sender, to, cc, subject, message_text, file_path=None):
    message = MIMEMultipart()
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    message["cc"] = cc

    msg = MIMEText(message_text)
    message.attach(msg)

    if file_path:
        attachment = MIMEBase("application", "octet-stream")
        with open(file_path, "rb") as attachment_file:
            attachment.set_payload(attachment_file.read())
        encoders.encode_base64(attachment)
        attachment.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(file_path)}",
        )
        message.attach(attachment)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print("Message Id: %s" % message["id"])
        return message
    except HttpError as error:
        print(f"An error occurred: {error}")

def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                " ",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def send_email_with_attachment(sender_email, receiver_email, cc_email, subject, message_text, file_path):
    service = get_gmail_service()

    message = create_message(sender_email, receiver_email, cc_email, subject, message_text, file_path)
    send_message(service, "me", message)
    print("Email sent successfully!")
