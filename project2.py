# This code is designed to retrieve an email template (its subject and body) from a PostgreSQL database.
# The template is extracted from the email_templates table located in the db_email_sender database.
# The user enters the template ID from the keyboard, after which the program executes an SQL query and displays the result.

import psycopg2 #a library for interacting with PostgreSQL.
import os       #a standard Python module for working with environment variables

def get_email_template(template_id):
    """
    Retrieves the subject and body of an email template from the database db_email_sender from table email_templates .

    :param template_id: ID of the email template to fetch.
    :return: Tuple (subject, body) if found, otherwise None.
    """
    try:
        # Database connection details
        db_name = "db_email_sender"
        db_user = "postgres"
        db_password = "38345ow2"
        db_host = "localhost"  # Use "localhost" since it's on your computer
        db_port = "5432"  # Default PostgreSQL port

        # Establish database connection
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cur = conn.cursor()

        # Execute query to fetch the email template
        cur.execute("SELECT subject, body FROM email_templates WHERE id = %s", (template_id,))
        template = cur.fetchone()

    except Exception as e:
        print(f"Database query failed: {e}")
        template = None  # Return None if an error occurs

    finally:
        # Ensure resources are closed properly
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

    return template

# Example usage:
try:
    template_id = int(input("Enter ID of email template: "))
    template = get_email_template(template_id)

    if template:
        print(f"\nSubject: {template[0]}\nBody: {template[1]}")
    else:
        print("Template is not found.")

except ValueError:
    print("Error: ID should be a number.")