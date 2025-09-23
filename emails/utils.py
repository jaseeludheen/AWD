import hashlib
import time
from django.conf import settings 
from django.core.mail import EmailMessage
from .models import Email, Sent, EmailTracking, Subscriber
from bs4 import BeautifulSoup


def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):  # attachment=None , set default 
    try:
        from_email = settings.DEFAULT_FROM_EMAIL

        for recipient_email in to_email:
            # Create EmailTracking  record

            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=recipient_email)
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email = email,   # email field name from  EmailTracking model
                    subscriber = subscriber,
                    unique_id = unique_id,
                )

                base_url = settings.BASE_URL  # add your ngrok url here
                # Generate the tracking pixel
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                print('click_tracking_url ==>',click_tracking_url)

                # Search for the link in email body
                
                soup = BeautifulSoup(message, 'html.parser') #html parser is analying the html content in email body
                """
                for a in soup.find_all('a', href=True): # find all anchor tags with href attribute , 
                    print(a['href'])
                """
                # List comprehension method (above code)
                urls = [ a['href'] for a in soup.find_all('a', href=True) ]

                # If there are links / urls in the email body , Inject our click tracking url to that original link
                if urls:
                    new_message = message
                    for url in urls:
                        # make the final tracking url (combination of click_tracking_url and urls)
                        tracking_url = f"{click_tracking_url}?url={url}" # https://example.com/track?url=https://mywebsite.com/page1
                        #print('tracking_url ==>',tracking_url)
                        
                        new_message = new_message.replace(f"{url}", f"{tracking_url}") # Replace the existing url with tracking url in the email body
                else:
                    print("No URLs found in the email body.")
            else:
                new_message = message


            mail = EmailMessage(mail_subject, new_message, from_email, to=[recipient_email])    # replce message with new_message - new_message will sent inside email body ,, to_email change to recipient_email
            if attachment is not None:
                mail.attach_file(attachment)
            
            mail.content_subtype = "html" # to send HTML email , to show html content in email body 
            mail.send()


        # Store the total sent emails inside the sent model
        #email = Email.objects.get(pk=email_id)

        if email:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails()
            sent.save()
    except Exception as e:
        raise e