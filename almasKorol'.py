import smtplib
import os
import logging
import psycopg2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_email_template(template_id):
    """Fetch email template from the database by ID."""
    try:
        conn = psycopg2.connect(
            dbname="db_email_sender",
            user="postgres",
            password="38345ow2",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT subject, body FROM email_templates WHERE id = %s", (template_id,))
        template = cursor.fetchone()
        cursor.close()
        conn.close()
        return template if template else (None, None)
    except Exception as e:
        logging.error(f"Database error: {e}")
        return None, None

def send_email(recipient_id, template_id, is_html=False):
    """Send an email using a template and recipient from the database."""
    try:
        # Load email credentials
        sender_email = os.getenv("EMAIL_SENDER", "otkelbaev2005@gmail.com")
        sender_password = os.getenv("EMAIL_PASSWORD", "nkcd wdhv bolh gmhy")
        
        if not sender_email or not sender_password:
            logging.error("Missing email credentials. Set EMAIL_SENDER and EMAIL_PASSWORD.")
            return False

        # Get recipient email
        conn = psycopg2.connect(
            dbname="db_email_sender",
            user="postgres",
            password="38345ow2",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT email, name FROM email_lists WHERE id = %s", (recipient_id,))
        recipient = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not recipient:
            logging.error("Recipient not found.")
            return False
        recipient_email, recipient_name = recipient
        
        # Get email template
        subject, body = get_email_template(template_id)
        if not subject or not body:
            logging.error("Email template not found.")
            return False
        
        # Personalize email (optional)
        body = body.replace("{{name}}", recipient_name if recipient_name else "Subscriber")
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
        
        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        logging.info(f"Email sent successfully to {recipient_email}")
        return True
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return False

# Example usage:
send_email(recipient_id=4, template_id=2, is_html=False)