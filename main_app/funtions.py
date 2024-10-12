

import os
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend

def Send_Welcome_email(user,name):
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
        'email': user,
    'name':name

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



def Send_Code_email(code, email,name):
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
            'name':name
        }
    # Use an f-string for body formatting
    body = render_to_string('email_templates/final-passcode.html', context)

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


def Send_Payment_email(link,email,name):
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
        'email':email,
        'name':name
    }
    subject = f"Payment Link from Zar Luxury"

    # Use a raw string (r"""...""") to avoid formatting issues with curly braces
    body = render_to_string('email_templates/final-payment.html',context)

    recipients = [email]
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
    
    
    
def send_mail_impression(x):
    
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
    if x.brand.type=='Material Provider':
        brand = x.brand.brand_name
        
    else:
        brand = x.brand.first_name + ' ' + x.brand.last_name
    
    if  x.user.type == 'Material Provider':
        User = x.user.brand_name
        Category = x.user.type
        email = x.user.email
        phone = x.user.mobile
    else:
        User = x.user.first_name + ' ' + x.user.last_name
        Category = x.user.type
        email = x.user.email
        phone = x.user.mobile
     
    context ={
        'brand_name':brand,
        'User':User,
        'Category':Category,
        'email':email,
        'phone':phone,
    }
    subject = f"New Connection from ZAR"

    # Use a raw string (r"""...""") to avoid formatting issues with curly braces
    body = render_to_string('email_templates/connect-brand.html',context)

    recipients = [x.brand.email]
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