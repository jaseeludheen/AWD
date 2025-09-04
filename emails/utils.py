from django.conf import settings 
from django.core.mail import EmailMessage


def send_email_notification(mail_subject, message, to_email, attachment=None):  # attachment=None , set default 
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=to_email)
        if attachment is not None:
            mail.attach_file(attachment)
        mail.send()
    except Exception as e:
        raise e