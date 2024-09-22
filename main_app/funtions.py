

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
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>ZAR Luxury Email</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Red+Rose&display=swap');
                body {
                    font-family: 'Red Rose', sans-serif;
                    margin: 0;
                    padding: 0;
                    color: #ffffff;
                    background-color: #000000;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                }
                .hero {
                    position: relative;
                    height: 400px;
                }
                .hero img {
                    width: 100%;
                    height: 400px;
                    object-fit: cover;
                    border-radius: 10px;
                }
                .logo img {
                    position: absolute;
                    top: 20px;
                    left: 20px;
                    width: 100px;
                    height: auto;
                }
                .hero-overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: linear-gradient(
                      to bottom,
                      rgba(0, 0, 0, 1) 0%,
                      rgba(0, 0, 0, 0) 100%
                    );
                }
                .hero-content {
                    position: absolute;
                    top: 100px;
                    left: 50px;
                }
                .hero-content h1 {
                    font-family: "Times New Roman", Times, serif;
                    font-size: 36px;
                    margin: 0 0 10px 0;
                }
                .hero-content p {
                    font-size: 18px;
                    margin: 0;
                }
                .content {
                    padding: 0 20px;
                }
                .content h2 {
                    text-align: center;
                }
                .content p {
                    text-align: center;
                    padding-inline: 2rem;
                }
                .partners {
                    display: flex;
                    gap: 10px;
                }
                .partner-card {
                    text-align: center;
                }
                .partner-img {
                    width: 100%;
                    height: 250px;
                    max-width: 180px;
                    margin-bottom: 10px;
                    border-radius: 10px;
                }
                section {
                    margin-bottom: 3rem;
                    margin-top: 3rem;
                }
                .partner-title {
                    font-size: 14px;
                    font-weight: bold;
                }
                h2 {
                    text-align: center;
                }
                footer {
                    text-align: center;
                    font-size: 14px;
                    padding: 20px 0;
                }
                .bg-image-header {
                    filter: saturate(0);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <header class="hero">
                    <img
                        class="bg-image-header"
                        src="https://images.unsplash.com/photo-1599696848652-f0ff23bc911f?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                        alt="Luxury Chair"
                    />
                    <div class="hero-overlay"></div>
                    <div class="logo">
                        <img
                            src="https://www.zarluxury.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fzar-logos-2.a14a82bb.png&w=128&q=75"
                            alt="ZAR Logo"
                        />
                    </div>
                    <div class="hero-content">
                        <h1>Connecting Excellence</h1>
                        <p>in Luxury Living and Design</p>
                    </div>
                </header>

                <main class="content">
                    <section>
                        <h2>Welcome to the world of ZAR Luxury Pvt. Ltd.</h2>
                        <p>At ZAR Luxury, we pride ourselves on delivering unparalleled
                        experiences to our discerning clientele.</p>
                        <p>Our mission is to bridge the gap between luxury brands, developers,
                        home buyers, architects, and interior designers by providing
                        unparalleled access to high-quality products and services.</p>
                    </section>

                    <section>
                        <h2>OUR PARTNERS</h2>
                        <div class="partners">
                            <div class="partner-card">
                                <img class="partner-img" src="https://via.placeholder.com/180" alt="Architects"/>
                                <p class="partner-title">Architects</p>
                            </div>
                            <div class="partner-card">
                                <img class="partner-img" src="https://via.placeholder.com/180" alt="Designers"/>
                                <p class="partner-title">Designers</p>
                            </div>
                            <div class="partner-card">
                                <img class="partner-img" src="https://via.placeholder.com/180" alt="Builders"/>
                                <p class="partner-title">Builders</p>
                            </div>
                        </div>
                    </section>

                    <section>
                        <h2 style="font-family: serif;">Curating the finest</h2>
                        <p style="text-align: center"><em>in design and living</em></p>
                    </section>
                </main>

                <footer>
                    <p>www.zarluxury.com | info@zarluxury.com</p>
                </footer>
            </div>
        </body>
        </html>
    """

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
        .passcode {{
          font-size: 24px;
          font-weight: bold;
          color: #fff;
          background-color: #333;
          padding: 10px;
          border: 1px solid #555;
          text-align: center;
          margin: 20px 0;
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
          <h1>Welcome to ZAR Luxury</h1>
          <p>You're the ONE</p>
        </div>
        <div class="content">
          <p>Dear {email},</p>
          <p>Welcome to the distinguished circle of ZAR Luxury, where luxury meets exclusivity.</p>
          <p>Your membership has been successfully activated, and we are pleased to provide you with your unique passcode key. This key is your gateway to a realm of unparalleled elegance and bespoke experiences.</p>
          <div class="passcode">
            {code}
          </div>
          <p>With this key, you can unlock a world designed for the discerning few—offering you access to carefully curated materials, personalized services, and a network of the finest brands and designers.</p>
          <p>We invite you to step into the world of ZAR, where every detail is crafted to meet your highest expectations. Your journey into a world beyond the ordinary begins now.</p>
          <p>If you have any inquiries or require assistance, our dedicated concierge team is here to serve you. For us, you are not just a member—you are the ONE.</p>
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
    email.content_subtype = "html"  # Sending HTML email
    email.send()

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