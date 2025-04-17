import unittest
import psycopg2
import project2 as project2

class TestEmailTemplateSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up database connection and test data"""
        cls.conn = psycopg2.connect(
            dbname="db_email_sender",
            user="postgres",
            password="38345ow2",
            host="localhost",
            port="5432"
        )
        cls.cursor = cls.conn.cursor()
        
        # Create test template
        cls.cursor.execute(
            "INSERT INTO email_templates (subject, body) VALUES (%s, %s) RETURNING id",
            ("Test Subject", "Test Body")
        )
        cls.test_template_id = cls.cursor.fetchone()[0]
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up test data and close connection"""
        cls.cursor.execute("DELETE FROM email_templates WHERE id = %s", (cls.test_template_id,))
        cls.conn.commit()
        cls.cursor.close()
        cls.conn.close()

    def test_get_existing_template(self):
        """Test retrieving an existing template"""
        result = project2.get_email_template(self.test_template_id)
        self.assertEqual(result, ("Test Subject", "Test Body"))

    def test_get_nonexistent_template(self):
        """Test retrieving a non-existent template"""
        result = project2.get_email_template(999999)
        self.assertIsNone(result)

    def test_create_valid_template(self):
        """Test creating a valid new template"""
        new_id = project2.create_email_template("New Subject", "New Body")
        self.assertIsInstance(new_id, int)
        
        # Verify creation
        self.cursor.execute("SELECT subject, body FROM email_templates WHERE id = %s", (new_id,))
        result = self.cursor.fetchone()
        self.assertEqual(result, ("New Subject", "New Body"))
        
        # Clean up
        self.cursor.execute("DELETE FROM email_templates WHERE id = %s", (new_id,))
        self.conn.commit()

    def test_create_invalid_template(self):
        """Test template creation with invalid input"""
        # Test empty subject
        new_id = project2.create_email_template("", "Valid Body")
        self.assertIsNotNone(new_id)
        self.cursor.execute("DELETE FROM email_templates WHERE id = %s", (new_id,))
        
        # Test empty body
        new_id = project2.create_email_template("Valid Subject", "")
        self.assertIsNotNone(new_id)
        self.cursor.execute("DELETE FROM email_templates WHERE id = %s", (new_id,))

    def test_create_duplicate_template(self):
        """Test creating template with duplicate content (should be allowed)"""
        new_id = project2.create_email_template("Test Subject", "Test Body")
        self.assertIsInstance(new_id, int)
        self.cursor.execute("DELETE FROM email_templates WHERE id = %s", (new_id,))

if __name__ == "__main__":
    unittest.main()