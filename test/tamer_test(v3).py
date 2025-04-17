# test_email_system.py (исправленная версия)
import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from email_system import EmailSystem # type: ignore

class TestEmailSystemInit(unittest.TestCase):
    @patch("os.makedirs")
    def test_directory_creation(self, mock_makedirs):
        """Тест создания директорий"""
        EmailSystem()
        mock_makedirs.assert_any_call("delivery_reports", exist_ok=True)
        mock_makedirs.assert_any_call("received_mails", exist_ok=True)

    @patch("os.makedirs", side_effect=OSError("Permission denied"))
    def test_directory_creation_failure(self, mock_makedirs):
        """Тест ошибки создания директорий"""
        with self.assertRaises(OSError):
            EmailSystem()

class TestSendMessage(unittest.TestCase):
    def setUp(self):
        self.email_system = EmailSystem()
        self.email_system._record_delivery_status = MagicMock()

    @patch("random.random", return_value=0.7)
    def test_send_success(self, mock_random):
        """Тест успешной отправки"""
        result = self.email_system.send_message(1, "Test")
        self.assertTrue(result)
        self.email_system._record_delivery_status.assert_called_with(1, "DELIVERED", None)

    @patch("random.random", return_value=0.9)
    def test_send_failure(self, mock_random):
        """Тест ошибки отправки"""
        result = self.email_system.send_message(2, "Test")
        self.assertFalse(result)
        self.email_system._record_delivery_status.assert_called_with(2, "FAILED", "Имитация сетевой ошибки")

    @patch("random.random", side_effect=[0.7, 0.2])
    @patch.object(EmailSystem, "save_reply")
    def test_reply_saving(self, mock_save, mock_random):
        """Тест сохранения ответа"""
        self.email_system.send_message(3, "Test")
        mock_save.assert_called_once_with(3, "Спасибо за ваше сообщение!\nС уважением,\nПолучатель")

class TestSaveReply(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_replies"
        self.email_system = EmailSystem()
        self.email_system.replies_dir = self.test_dir
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("datetime.datetime")
    def test_reply_file_content(self, mock_dt):
        """Тест содержимого файла ответа"""
        mock_dt.now.return_value.strftime.return_value = "20240101_120000"
        mock_dt.now.return_value.isoformat.return_value = "2024-01-01T12:00:00"
        
        self.email_system.save_reply(1, "Test reply")
        file_path = os.path.join(self.test_dir, "reply_1_20240101_120000.txt")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("ID отправленного письма: 1", content)
            self.assertIn("Test reply", content)

class TestGenerateReport(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_reports"
        self.email_system = EmailSystem()
        self.email_system.report_dir = self.test_dir
        os.makedirs(self.test_dir, exist_ok=True)
        
        self.email_system.delivery_statuses = [
            {"email_id": 1, "status": "DELIVERED", "timestamp": "2024-01-01T00:00:00", "error": None},
            {"email_id": 2, "status": "FAILED", "timestamp": "2024-01-01T00:00:01", "error": "Ошибка"}
        ]

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("datetime.datetime")
    def test_report_generation(self, mock_dt):
        """Тест генерации отчета"""
        mock_dt.now.return_value.strftime.return_value = "20240101_120000"
        
        self.email_system.generate_delivery_report()
        report_path = os.path.join(self.test_dir, "delivery_report_20240101_120000.txt")
        
        expected_content = [
            "Отчет о доставке писем",
            "=" * 40,
            "Сгенерирован: 2024-01-01T00:00:00",
            "\nСтатистика:",
            "Всего писем: 2",
            "Успешно доставлено: 1",
            "Ошибок доставки: 1",
            "\nДетали:",
            "ID\tСтатус\tВремя\t\tОшибка",
            "1\tDELIVERED\t2024-01-01T00:00:00\tНет",
            "2\tFAILED\t2024-01-01T00:00:01\tОшибка"
        ]
        
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read().split("\n")
            for expected, actual in zip(expected_content, content):
                self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()