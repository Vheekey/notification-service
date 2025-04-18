import json
import smtplib
import logging
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config.email_config import EmailConfig
from tenacity import retry, stop_after_attempt, wait_fixed

logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(10))  # retry 3 times with 10 seconds delay
def send_email(user_data):
    logger.info(f"Preparing to send email to user data: {user_data}")

    try:
        try:
            data = json.loads(user_data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            return
        logger.info(f"data details: {data}")

        user_email = data.get('email')
        user_token = data.get('code')
        user_message = data.get('message', f"Hello, here is your token. <br> Token: {user_token}")
        logger.info(f"Preparing to send email to {user_email}: {user_message}")

        msg = MIMEMultipart()
        msg["From"] = EmailConfig.SMTP_USERNAME
        msg["To"] = user_email
        msg["Subject"] = "User Token Notification"

        body = f"You have a mail! <br> {user_message}"
        msg.attach(MIMEText(body, "html"))

        try:
            # send the message via our own SMTP server
            #     server = smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT)
            #     server.starttls()
            #     server.login(EmailConfig.SMTP_USERNAME, EmailConfig.SMTP_PASSWORD)
            #     text = msg.as_string()
            #     logger.info(f"Sending email to {user_email}: {msg['Subject']} - {text}")
            #     server.sendmail(EmailConfig.SMTP_USERNAME, user_email, text)
            #     logger.info(f"Email sent to {user_email}")
            #     server.quit()

            # Send the email using msmtp
            process = subprocess.Popen(
                ["msmtp", user_email],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            process.stdin.write(msg.as_string().encode('utf-8'))
            process.stdin.close()
            # Write the email content to the stdin of the msmtp process
            output, error = process.communicate(input=msg.as_string().encode('utf-8'))

            if process.returncode != 0:
                logger.error(f"msmtp error: {error.decode().strip()}")
            else:
                logger.info(f"Email sent to {user_email}")
        except Exception as e:
            logger.error(f"Email sending exception: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode user_data: {e}")
    except AttributeError as e:
        logger.error(f"AttributeError in send_email: {e}")
