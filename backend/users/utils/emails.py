import logging
from typing import Literal, Tuple

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

logger = logging.getLogger(__name__)

User = get_user_model()


def fallback_message_email_verification(link: str) -> str:
    return f"""
    Hello!
    
    Your email address has been used to register with raggy.
    
    If that is correct, please verify your email by clicking on the link below.

    {link}
    
    You can also copy the link and paste it into your browser's address bar.
    
    Thank you for using raggy!
    """


class EmailSendingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class EmailSender:
    def __init__(self, from_email: str):
        self.from_email = from_email

    def send_email(self, to_email: str, subject: str, html_content: str, fallback_message: str):
        try:
            send_mail(
                subject=subject,
                from_email=self.from_email,
                recipient_list=[to_email],
                html_message=html_content,
                message=fallback_message,
                fail_silently=False,
            )
        except Exception as e:
            logger.exception(
                f"Could not send email regarding '{subject}' to {to_email}. Failed with exception: {e}"
            )
            raise EmailSendingError(str(e))
        else:
            logger.info(f"Sent email regarding '{subject}' to {to_email}.")


class EmailVerifier:
    token_generator = default_token_generator

    def __init__(self, host: str, scheme:  Literal["http", "https"], from_email: str):
        self.url = f"{scheme}://{host}"
        self.email_sender = EmailSender(from_email)

    def send_verification_email(self, user: User):
        to_email = user.email
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = self.token_generator.make_token(user)
        sub_link = reverse(viewname="users:verify_email", kwargs={"uidb64": uidb64, "token": token})
        link = f"{self.url}{sub_link}"
        fallback_message = fallback_message_email_verification(link)
        html_content = render_to_string(template_name="users/emails/verify_email.html", context={"link": link})
        self.email_sender.send_email(
            to_email=to_email,
            subject="Please verify your email for raggy",
            html_content=html_content,
            fallback_message=fallback_message,
        )

    def verify_email_for_user(self, uidb64: str, token: str) -> Tuple[bool, str]:
        user = self.get_user(uidb64)
        if user is not None:
            if user.email_verified:
                return False, "Your email has already been verified."

            if self.token_generator.check_token(user, token):
                user.email_verified = True
                user.save()
                logger.info(f"Email for user {user} verified.")
                return True, "success"

            logger.warning(f"Email verification failed.")
            logger.info("User exists, resending email verification link.")
            self.send_verification_email(user)
            return False, "The link appears to be invalid, we have sent you a new one. Please check your email."

        return False, "The link appears to be invalid and we are unable identify you. Please contact support."

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user