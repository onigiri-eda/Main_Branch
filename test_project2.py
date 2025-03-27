import unittest
from unittest.mock import patch, MagicMock
import project2  

class TestGetEmailTemplate(unittest.TestCase):

    @patch('project2.psycopg2.connect')
    def test_template_found(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('Test Subject', 'Test Body')
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = project2.get_email_template(1)
        self.assertEqual(result, ('Test Subject', 'Test Body'))
        
        mock_cursor.execute.assert_called_once_with(
            "SELECT subject, body FROM email_templates WHERE id = %s", (1,)
        )
        
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('project2.psycopg2.connect')
    def test_template_not_found(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = project2.get_email_template(9999)
        self.assertIsNone(result)
        
        mock_cursor.execute.assert_called_once_with(
            "SELECT subject, body FROM email_templates WHERE id = %s", (9999,)
        )
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('project2.psycopg2.connect', side_effect=Exception("Connection error"))
    def test_exception_handling(self, mock_connect):
        result = project2.get_email_template(1)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
