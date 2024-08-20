from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from loguru import logger

from app.shared.config import cfg


class EmailClient:
    def __init__(self):
        self.sender = f"{cfg.SMTP_FROM_NAME} <{cfg.SMTP_FROM}>"
        self.client = boto3.client("ses", region_name=cfg.AWS_REGION)

    def send_email(self, subject, body_text, path, to, to_name, token_url):
        body_html = None
        with path.open("r") as f:
            html_content = f.read()
            temp_html = html_content.replace("TO_NAME", to_name)
            body_html = temp_html.replace("TOKEN_URL", token_url)
        charset = "UTF-8"
        try:
            self.client.send_email(
                Destination={
                    "ToAddresses": [
                        to,
                    ],
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": charset,
                            "Data": body_html,
                        },
                        "Text": {
                            "Charset": charset,
                            "Data": body_text,
                        },
                    },
                    "Subject": {
                        "Charset": charset,
                        "Data": subject,
                    },
                },
                Source=self.sender,
            )
        except ClientError as e:
            logger.error(f"Issue sending verification email: {e}")
        else:
            logger.info(f"Successfully sent verification email to {to}")

    def send_register_verification_email(self, token_url, to, to_name):
        subject = "Song of the Week Email Verification"
        body_text = f"Hello {to_name},\nThank you for signing up for Song of the Week! Please use the link below to complete your account registration:\n\n{token_url}"
        path = Path(__file__).parent / "./emails/registration_email_verification.html"
        return self.send_email(subject, body_text, path, to, to_name, token_url)

    def send_change_verification_email(self, token_url, to, to_name):
        subject = "Song of the Week Email Verification"
        body_text = f"Hello {to_name},\nYou have changed your email for your Song of the Week account. Please verify your new email address using the button below to confirm this email change:\n\n{token_url}"
        path = Path(__file__).parent / "./emails/change_email_verification.html"
        return self.send_email(subject, body_text, path, to, to_name, token_url)

    def send_password_reset_email(self, token_url, to, to_name):
        subject = "Song of the Week Password Reset"
        body_text = f"Hello {to_name},\nYou have requested to reset your password for Song of the Week. Please do so by clicking the link below. If you did not request a password change, please disregard this email.\n\n{token_url}"
        path = Path(__file__).parent / "./emails/reset_password_verification.html"
        return self.send_email(subject, body_text, path, to, to_name, token_url)
