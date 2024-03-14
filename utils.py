import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'  # SMTP server (e.g., smtp.gmail.com for Gmail)
EMAIL_PORT = 587  # SMTP port (e.g., 587 for TLS)
EMAIL_ADDRESS = 'amoh81benjamin@gmail.com'  # Your email address
EMAIL_PASSWORD = 'pkxeususxdungoeg'  # Your email password or app-specific password

def send_notification(subject, message):
    """
    Sends an email notification.
    
    :param subject: The subject of the email.
    :param message: The body of the email.
    """
    try:
        # Set up the email server and start TLS encryption
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS  # Sending to yourself; change as needed
        msg['Subject'] = subject

        # Attach the text message
        msg.attach(MIMEText(message, 'This email is to notify you that you have applied for the Dartmouth real estate housing successfully'))

        # Send the email and close the server connection
        server.send_message(msg)
        server.quit()

        print("Notification sent successfully.")
    except Exception as e:
        print(f"Failed to send notification: {e}")

# At the end of utils.py, add:
if __name__ == "__main__":
    send_notification("Test Subject", "This is a test message from your bot.")

# This will send a test email when utils.py is run directly.