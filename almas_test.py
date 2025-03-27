import unittest
from unittest.mock import patch, MagicMock
from email_sender import get_email_template, send_email

class TestEmailSender(unittest.TestCase):
    
    @patch("email_sender.psycopg2.connect")
    def test_get_email_template_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = ("Test Subject", "Test Body")
        mock_connect.return_value = mock_conn
        
        subject, body = get_email_template(1)
        self.assertEqual(subject, "Test Subject")
        self.assertEqual(body, "Test Body")
        
    @patch("email_sender.psycopg2.connect")
    def test_get_email_template_not_found(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value = mock_conn
        
        subject, body = get_email_template(1)
        self.assertIsNone(subject)
        self.assertIsNone(body)
        
    @patch("email_sender.psycopg2.connect")
    @patch("email_sender.smtplib.SMTP")
    @patch("email_sender.get_email_template")
    @patch("email_sender.os.getenv")
    def test_send_email_success(self, mock_getenv, mock_get_email_template, mock_smtp, mock_connect):
        mock_getenv.side_effect = lambda key, default=None: "test_sender@gmail.com" if key == "EMAIL_SENDER" else "test_password"
        mock_get_email_template.return_value = ("Test Subject", "Hello, {{name}}!")
        
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = ("recipient@example.com", "John")
        mock_connect.return_value = mock_conn
        
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
        
        result = send_email(1, 1, is_html=False)
        
        self.assertTrue(result)
        mock_smtp_instance.sendmail.assert_called_once()
        
    @patch("email_sender.psycopg2.connect")
    @patch("email_sender.get_email_template")
    @patch("email_sender.os.getenv")
    def test_send_email_recipient_not_found(self, mock_getenv, mock_get_email_template, mock_connect):
        mock_getenv.side_effect = lambda key, default=None: "test_sender@gmail.com" if key == "EMAIL_SENDER" else "test_password"
        mock_get_email_template.return_value = ("Test Subject", "Test Body")
        
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value = mock_conn
        
        result = send_email(1, 1, is_html=False)
        self.assertFalse(result)
        
    @patch("email_sender.psycopg2.connect")
    @patch("email_sender.get_email_template")
    @patch("email_sender.os.getenv")
    def test_send_email_template_not_found(self, mock_getenv, mock_get_email_template, mock_connect):
        mock_getenv.side_effect = lambda key, default=None: "test_sender@gmail.com" if key == "EMAIL_SENDER" else "test_password"
        mock_get_email_template.return_value = (None, None)
        
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = ("recipient@example.com", "John")
        mock_connect.return_value = mock_conn
        
        result = send_email(1, 1, is_html=False)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
