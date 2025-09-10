from django.conf import settings 
from django.core.mail import EmailMessage
from .models import Email, Sent


def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):  # attachment=None , set default 
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=to_email)
        if attachment is not None:
            mail.attach_file(attachment)
        
        mail.content_subtype = "html" # to send HTML email , to show html content in email body 
        mail.send()
        # Store the total sent emails inside the sent model

        email = Email.objects.get(pk=email_id)
        sent = Sent()
        sent.email = email
        sent.total_sent = email.email_list.count_emails()
        sent.save()
    except Exception as e:
        raise e