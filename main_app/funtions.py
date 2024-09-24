

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
    body = render_to_string('email_templates/welcome_email.html', context)
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

    # Use an f-string for body formatting
    body = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to ZAR Luxury – You're the ONE</title>
</head>
<body style="background-color: #000000; color: #ffffff; margin: 0; padding: 0; font-family: 'Arial', sans-serif;">
  <table role="presentation" style="width: 100%; background-color: #000000;" cellpadding="0" cellspacing="0" border="0">
    <tr>
      <td align="center">
        <table role="presentation" style="max-width: 600px; width: 100%; background-color: #1a1a1a; color: #ffffff; padding: 20px; border-collapse: collapse;" cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td align="center" style="padding: 20px;">
              <img src="https://www.zarluxury.com/static/images/zar-logos-2.webp" alt="ZAR Luxury Logo" style="width: 150px; height: auto;">
            </td>
          </tr>
          <tr>
            <td align="center" style="font-family: 'Gloock', serif; font-size: 24px; font-weight: bold; padding-bottom: 10px; color: #ffffff;">
              Welcome to ZAR Luxury
            </td>
          </tr>
          <tr>
            <td align="center" style="font-size: 16px; font-family: 'Arial', sans-serif; color: #ffffff;">
              <p style="margin: 0;">You're the ONE</p>
            </td>
          </tr>
          <tr>
            <td style="padding: 20px; text-align: left; line-height: 1.6; font-size: 16px; color: #ffffff;">
              <p>Dear Member,</p>
              <p>Welcome to the distinguished circle of ZAR Luxury, where luxury meets exclusivity.</p>
              <p>Your membership has been successfully activated, and we are pleased to provide you with your unique passcode key.</p>
              <div style="font-size: 24px; font-weight: bold; background-color: #333333; padding: 10px; text-align: center; margin: 20px 0; border: 1px solid #555555; color: #ffffff;">
                {code}
              </div>
              <p>With this key, you can unlock a world designed for the discerning few—offering you access to carefully curated materials, personalized services, and a network of the finest brands and designers.</p>
              <p>We invite you to step into the world of ZAR, where every detail is crafted to meet your highest expectations.</p>
              <p>If you have any inquiries or require assistance, our dedicated concierge team is here to serve you. For us, you are not just a member—you are the ONE.</p>
              <p>Regards,</p>
              <p>ZAR Luxury Team</p>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding: 20px; font-size: 12px; color: #bbbbbb;">
              <p>ZAR Luxury - Where Luxury Meets Exclusivity</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
    """

    recipients = [email]

    email_message = EmailMessage(
        subject=subject,
        body=body,
        from_email=EMAIL_HOST_USER,
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



    subject = f"Payment Link from Zar Luxury"

    # Use a raw string (r"""...""") to avoid formatting issues with curly braces
    body = f"""
        <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Profile Has Been Approved</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Red+Rose:wght@300&display=swap');
    body {{
      font-family: 'Red Rose', sans-serif;
      background-color: #1a1a1a;
      margin: 0;
      padding: 0;
      color: #fff;
    }}
    .container {{
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #2a2a2a;
      border: 1px solid #444;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    }}
    .header {{
      background-color: #333;
      color: #fff;
      padding: 10px 0;
      text-align: center;
    }}
    .content {{
      padding: 20px;
      line-height: 1.6;
    }}
    .payment-link {{
      font-size: 18px;
      font-weight: bold;
      color: #fff;
      background-color: #333;
      padding: 10px;
      border: 1px solid #555;
      text-align: center;
      margin: 20px 0;
      display: block;
      text-decoration: none;
    }}
    .footer {{
      text-align: center;
      padding: 10px;
      font-size: 12px;
      color: #bbb;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Your Profile Has Been Approved</h1>
    </div>
    <div class="content">
      <p>Dear <span class="name">{email}</span>,</p>
      <p>We are pleased to inform you that your profile has been successfully reviewed and approved by our team at ZAR Luxury.</p>
      <p>To complete your registration, please finalize your payment by clicking the link below:</p>
      <a href="{link}" target="_blank" class="payment-link">Complete Your Payment</a>
      <p>We look forward to having you as a valued member of our exclusive network. Should you have any questions or need assistance with the payment process, please feel free to contact us at <a href="mailto:info@zarluxury.com" style="color: #fff;">(Contact Information)</a>.</p>
      <p>Thank you for choosing ZAR Luxury.</p>
      <p>Regards,</p>
      <p>ZAR Luxury Team</p>
    </div>
    <div class="footer">
      <p>ZAR Luxury - Where Luxury Meets Exclusivity</p>
    </div>
  </div>
</body>
</html>
    """

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