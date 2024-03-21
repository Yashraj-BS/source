import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from concurrent.futures import ThreadPoolExecutor


def send_email(subject, body, to_email, attachment_path, sender, gmail_password):
    # Create the MIME object
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, 'plain'))

    # Attach the file
    if attachment_path:
        attachment = open(attachment_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
        message.attach(part)

    # Connect to the Gmail SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, gmail_password)
        server.sendmail(sender, to_email, message.as_string())

def send_email_in_background(subject, body, to_email, attachment_path, sender, gmail_password):
    with ThreadPoolExecutor() as executor:
        # Schedule the email sending function to run in the background
        future = executor.submit(send_email, subject, body, to_email, attachment_path, sender, gmail_password)

        # If you need to do something after the email is sent, you can use future.result()

# Example usage
subject = 'Invoice aaya BC'
body = '20/03/2024'
to_email = 'rupeshvibhute30@gmail.com'
attachment_path = './invoice.pdf'
sender = 'yashraj.billing.system@gmail.com'
gmail_password = 'reth gwad ofye fdaj '

# Send email in the background
send_email_in_background(subject, body, to_email, attachment_path, sender, gmail_password)
