

import os
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

    # Use a raw string (r"""...""") to avoid formatting issues with curly braces
    body = r"""
        <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to ZAR Luxury</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Gloock&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Red+Rose:wght@300&display=swap" rel="stylesheet">
</head>
 <style>
    @font-face{{
      font-family: 'Gloock';
      src: url('https://fonts.googleapis.com/css2?family=Gloock&display=swap') ,
           
      font-weight: 400;
      font-style: normal;
    }}
    @font-face{{
      font-family: 'Red Rose';
      src: url('https://fonts.googleapis.com/css2?family=Red+Rose:wght@300&display=swap') ,
           
      font-weight: 300;
      font-style: normal;
    }}
  </style>
<body style="font-family: 'Red Rose', sans-serif; font-weight: 300; background-color: black; color: white; margin: 0; padding: 0;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" align="center">
    <tr>
      <td align="center" style="padding: 1rem;">
        <table role="presentation" width="90%" cellspacing="0" cellpadding="0" border="0" align="center" style="background-color: black; color: white;">
          <tr>
            <td>
              <div style="position: relative; background-image: linear-gradient(to bottom, #000, #2563eb); color: white; overflow: hidden;">
                <div style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; height: 560px;">
                  <img src="https://images.pexels.com/photos/3701455/pexels-photo-3701455.jpeg?cs=srgb&dl=pexels-bruceclarkinoc-3701455.jpg&fm=jpg" alt="Background Image" style="object-fit: cover; object-position: center; width: 100%; height: 100%;" />
                  <div style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; background-image: linear-gradient(to bottom, #000, rgba(0, 0, 0, 0.8), transparent); opacity: 1;"></div>
                </div>
                <!-- Logo Image at Top Right Corner -->
                <div style="position: absolute; top: 1rem; left: 1rem;">
                  <img src="https://www.zarluxury.com/static/images/zar-logos-2.webp" alt="Logo" style="width: auto; height: 4rem;" />
                </div>
                <div style="height: 560px; position: relative; z-index: 10; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; text-align: left; padding-left: 2rem; padding-right: 2rem;">
                  <h1 style="font-size: 3rem; margin-bottom: 1rem; font-family: 'Gloock', serif; font-weight: 400; font-style: normal;">Connecting Excellence</h1>
                  <p style="font-size: 1.125rem; color: #d1d5db; margin-bottom: 1rem;">in Luxury Living and Design</p>
                </div>
              </div>
              <div style="padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);">
                <h1 style="font-size: 1.875rem; font-weight: bold; margin-bottom: 1rem; font-family: 'Gloock', serif; font-weight: 400; font-style: normal;">Welcome to ZAR Luxury</h1>
                <p style="font-size: 1.125rem; margin-bottom: 1rem;">Dear <span style="font-weight: 600;">({email})</span>,</p>
                <p style="font-size: 1.125rem; margin-bottom: 1rem;">Thank you for choosing ZAR Luxury and taking the time to complete your sign-up.</p>
                <p style="font-size: 1.125rem; margin-bottom: 1rem;">We have successfully received your request, and your profile is currently under review. Our team is carefully assessing the details, and we will notify you once the review process is complete.</p>
                <p style="font-size: 1.125rem; margin-bottom: 1rem;">If you have any questions in the meantime, please don’t hesitate to contact us.</p>
                <p style="font-size: 1.125rem;">Regards,</p>
                <p style="font-size: 1.125rem; font-weight: 600; font-family: 'Gloock', serif; font-weight: 400; font-style: normal;">ZAR Luxury Team</p>
              </div>
              <h2 style="font-size: 1.5rem; text-align: center; font-family: 'Gloock', serif; font-weight: 400; font-style: normal;">Our Partners</h2>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" align="center" style="display: grid; grid-template-columns: repeat(1, minmax(0, 1fr)); gap: 1rem; max-width: 80rem; margin-left: auto; margin-right: auto; margin-top: 6rem;">
                <!-- Architect Card -->
                <tr>
                  <td>
                    <article style="position: relative; isolation: isolate; display: flex; flex-direction: column; justify-content: flex-end; overflow: hidden; border-radius: 1rem; padding: 2rem; padding-top: 10rem;">
                      <img src="https://images.pexels.com/photos/157811/pexels-photo-157811.jpeg?cs=srgb&dl=pexels-yentl-jacobs-43020-157811.jpg&fm=jpg" alt="Architects" style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; height: 100%; width: 100%; object-fit: cover;">
                      <div style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; background-image: linear-gradient(to top, #1a202c, rgba(26, 32, 44, 0.4));"></div>
                      <h3 style="z-index: 10; margin-top: 0.75rem; font-size: 1.875rem; font-weight: bold; color: white; font-family: 'Gloock', serif; font-weight: 400; font-style: normal;">Architects</h3>
                      <div style="z-index: 10; gap-y-1 overflow-hidden text-sm leading-6 text-gray-300;">Crafting spaces</div>
                    </article>
                  </td>
                </tr>
                <!-- Designers Card -->
                <tr>
                  <td>
                    <article style="position: relative; isolation: isolate; display: flex; flex-direction: column; justify-content: flex-end; overflow: hidden; border-radius: 1rem; padding: 2rem; padding-top: 10rem;">
                      <img src="https://images.pexels.com/photos/3797991/pexels-photo-3797991.jpeg?cs=srgb&dl=pexels-houzlook-3797991.jpg&fm=jpg" alt="Designers" style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; height: 100%; width: 100%; object-fit: cover;">
                      <div style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; background-image: linear-gradient(to top, #1a202c, rgba(26, 32, 44, 0.4));"></div>
                      <h3 style="z-index: 10; margin-top: 0.75rem; font-size: 1.875rem; font-weight: bold; color: white; font-family: 'Gloock', serif; font-weight: 400; font-style: normal;">Designers</h3>
                      <div style="z-index: 10; gap-y-1 overflow-hidden text-sm leading-6 text-gray-300;">Shaping aesthetics</div>
                    </article>
                  </td>
                </tr>
                <!-- Consultants Card -->
                <tr>
                  <td>
                    <article style="position: relative; isolation: isolate; display: flex; flex-direction: column; justify-content: flex-end; overflow: hidden; border-radius: 1rem; padding: 2rem; padding-top: 10rem;">
                      <img src="https://images.pexels.com/photos/667838/pexels-photo-667838.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500" alt="Consultants" style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; height: 100%; width: 100%; object-fit: cover;">
                      <div style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; background-image: linear-gradient(to top, #1a202c, rgba(26, 32, 44, 0.4));"></div>
                      <h3 style="z-index: 10; margin-top: 0.75rem; font-size: 1.875rem; font-weight: bold; color: white; font-family: 'Gloock', serif; font-weight: 400; font-style: normal;">Consultants</h3>
                      <div style="z-index: 10; gap-y-1 overflow-hidden text-sm leading-6 text-gray-300;">Providing insights</div>
                    </article>
                  </td>
                </tr>
              </table>
              <!-- Bottom Heading and Contact Information -->
              <div style="margin-top: 3rem; text-align: center;">
                <h2 style="font-size: 1.875rem; font-weight: bold; margin-bottom: 1rem;">Curating Finest Design</h2>
                <p style="font-size: 0.875rem; color: #d1d5db;">
                  <a href="http://www.zarluxury.com" style="text-decoration: none; color: white;">www.zarluxury.com</a> | <a href="mailto:info@zarluxury.com" style="text-decoration: none; color: white;">info@zarluxury.com</a>
                </p>
              </div>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
    """.format(
        email=user,
    )

    recipients = [user]

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=EMAIL_HOST_USER,
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