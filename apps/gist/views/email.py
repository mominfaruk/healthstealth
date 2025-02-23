import logging
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

class EmailService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def send_single_email(self, email_type, to_email, context, subject=None):
        try:
            if email_type == 'password_reset':
                subject = subject or "Password Reset Request"
                message = ("Hello,\n\n"
                           "Use the following link to reset your password:\n"
                           f"{context.get('reset_link', '#')}\n\n"
                           "If you did not request this, ignore this email.")
            elif email_type == 'notification':
                subject = subject or "Notification from HealthStealth"
                message = context.get('message', "You have a new notification.")
            else:
                self.logger.error(f"Unsupported email type: {email_type}")
                return False

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [to_email],
                fail_silently=False,
            )
            self.logger.info(f"{email_type.capitalize()} email sent to: {to_email}")
            return True
        except Exception as e:
            self.logger.exception(f"Error sending {email_type} email: {e}")
            return False

    def send_bulk_email(self, email_type, recipients, context, subject=None):
        try:
            if email_type == 'password_reset':
                subject = subject or "Password Reset Request"
                message = ("Hello,\n\n"
                           "Use the following link to reset your password:\n"
                           f"{context.get('reset_link', '#')}\n\n"
                           "If you did not request this, ignore this email.")
            elif email_type == 'notification':
                subject = subject or "Notification from HealthStealth"
                message = context.get('message', "You have a new notification.")
            else:
                self.logger.error(f"Unsupported email type: {email_type}")
                return False

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipients,
                fail_silently=False,
            )
            self.logger.info(f"{email_type.capitalize()} email sent to multiple recipients.")
            return True
        except Exception as e:
            self.logger.exception(f"Error sending bulk {email_type} email: {e}")
            return False

    def send_template_email(self, template_name, to_email, context, subject, from_email=None):
        try:
            html_content = render_to_string(template_name, context)
            text_content = "This email requires an HTML-capable email client."
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email or settings.EMAIL_HOST_USER,
                to=[to_email] if isinstance(to_email, str) else to_email
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
            self.logger.info(f"Templated email sent to: {to_email}")
            return True
        except Exception as e:
            self.logger.exception(f"Error sending templated email: {e}")
            return False

    def send_email(self, email_type, recipients, context, subject=None, template_name=None, from_email=None):
        """
        Sends an email using the appropriate method based on provided parameters.
        - If a template name is provided, a templated email is sent.
        - Otherwise, if recipients is a list and contains more than one address, a bulk email is sent.
        - If a single email is provided, a single email is sent.
        """
        try:
            if template_name:
                return self.send_template_email(
                    template_name,
                    recipients,
                    context,
                    subject or f"{email_type.capitalize()} Email",
                    from_email
                )
            if isinstance(recipients, list):
                if len(recipients) == 1:
                    return self.send_single_email(email_type, recipients[0], context, subject)
                else:
                    return self.send_bulk_email(email_type, recipients, context, subject)
            else:
                return self.send_single_email(email_type, recipients, context, subject)
        except Exception as e:
            self.logger.exception(f"Error sending email using send_email: {e}")
            return False

    def send_password_reset_email(self, to_email, reset_link):
        context = {'reset_link': reset_link}
        return self.send_single_email('password_reset', to_email, context)

    def send_notification_email(self, to_email, message):
        context = {'message': message}
        return self.send_single_email('notification', to_email, context)
