

import os
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend

def Send_Welcome_email(user):
    EMAIL_HOST_USER = 'admin@zarluxury.com'
    EMAIL_HOST_PASSWORD = 'Zara#24Admin'
    EMAIL_HOST = 'smtp.hostinger.com'
    EMAIL_PORT = 465

    email_backend = EmailBackend(
    host=EMAIL_HOST,
    port=EMAIL_PORT,
    username=EMAIL_HOST_USER,
    password=EMAIL_HOST_PASSWORD,
    use_ssl=True,  # Use TLS for port 587
)



    subject = "Welcome to Zar Luxury."

     # Load the email template and pass context variables
    context = {
        'email': user
    }
    body = render_to_string('email_templates/welcome-email-new.html', context)
    recipients = [user]
    from_email = '"ZAR Luxury" <admin@zarluxury.com>'

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=recipients,
        connection=email_backend,
    )
    email.content_subtype = "html"
    email.send()



def Send_Code_email(code, email):
    EMAIL_HOST_USER = 'admin@zarluxury.com'
    EMAIL_HOST_PASSWORD = 'Zara#24Admin'
    EMAIL_HOST = 'smtp.hostinger.com'
    EMAIL_PORT = 465
    
    email_backend = EmailBackend(
        host=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
        use_ssl=True
    )

    subject = f"Code Verification {code} for Zar Luxury"
    context = {
            'email': email,
            'code':code,
        }
    # Use an f-string for body formatting
    body = render_to_string('email_templates/passcode-new.html', context)

    recipients = [email]
    from_email = '"ZAR Luxury" <admin@zarluxury.com>'

    email_message = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=recipients,
        connection=email_backend,
    )
    email_message.content_subtype = "html"  # Sending HTML email
    email_message.send()


def Send_Payment_email(link,email):
    EMAIL_HOST_USER = 'admin@zarluxury.com'
    EMAIL_HOST_PASSWORD = 'Zara#24Admin'
    EMAIL_HOST = 'smtp.hostinger.com'
    EMAIL_PORT = 465
    email_backend = EmailBackend(
    host=EMAIL_HOST,
    port=EMAIL_PORT,
    username=EMAIL_HOST_USER,
    password=EMAIL_HOST_PASSWORD,
    use_ssl=True,  # Use TLS for port 587
)


    context ={
        'link':link,
        'email':email
    }
    subject = f"Payment Link from Zar Luxury"

    # Use a raw string (r"""...""") to avoid formatting issues with curly braces
    body = render_to_string('email_templates/payment-new.html',context)

    recipients = [email]

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=EMAIL_HOST_USER,
        to=recipients,
        connection=email_backend,
    )
    email.content_subtype = "html"
    email.send()