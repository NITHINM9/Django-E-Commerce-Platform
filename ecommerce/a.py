import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mnithin17042023@gmail.com'
EMAIL_HOST_PASSWORD = 'MNithin@2002'  # Be cautious about hardcoding your password

def send_email(to_email, subject, body):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the server
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)  # Log in to the server

        # Send the email
        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()  # Close the connection to the server

# Usage example
if __name__ == "__main__":
    recipient_email = "recipient@example.com"  # Replace with the recipient's email
    email_subject = "Test Email"
    email_body = "This is a test email sent from a Python script."

    send_email(recipient_email, email_subject, email_body)
