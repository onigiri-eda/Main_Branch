# Email Template Management System
# Handles retrieval and creation of email templates in PostgreSQL database

import psycopg2

def get_email_template(template_id):
    """
    Retrieves the subject and body of an email template from the database.
    
    :param template_id: ID of the email template to fetch
    :return: Tuple (subject, body) if found, None otherwise
    """
    try:
        conn = psycopg2.connect(
            dbname="db_email_sender",
            user="postgres",
            password="38345ow2",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT subject, body FROM email_templates WHERE id = %s", (template_id,))
        return cur.fetchone()
    
    except Exception as e:
        print(f"Database error: {e}")
        return None
    
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

def create_email_template(subject, body):
    """
    Creates a new email template in the database.
    
    :param subject: Email subject line
    :param body: Email body content
    :return: ID of the created template, None if failed
    """
    try:
        conn = psycopg2.connect(
            dbname="db_email_sender",
            user="postgres",
            password="38345ow2",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO email_templates (subject, body) VALUES (%s, %s) RETURNING id",
            (subject, body)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id
    
    except Exception as e:
        print(f"Template creation failed: {e}")
        return None
    
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("Email Template Manager\n" + "=" * 25)
    action = input("Choose action [get/create]: ").lower().strip()
    
    if action == "get":
        try:
            template_id = int(input("Enter template ID: "))
            result = get_email_template(template_id)
            
            if result:
                print(f"\nSubject: {result[0]}\nBody:\n{result[1]}")
            else:
                print("No template found with that ID")
                
        except ValueError:
            print("Error: Please enter a valid numeric ID")
    
    elif action == "create":
        print("\nCreate New Template")
        subject = input("Enter subject: ").strip()
        body = input("Enter body content:\n").strip()
        
        if not subject or not body:
            print("Error: Both subject and body are required")
        else:
            template_id = create_email_template(subject, body)
            if template_id:
                print(f"Template created successfully! ID: {template_id}")
            else:
                print("Failed to create template")
    
    else:
        print("Invalid action. Please choose 'get' or 'create'")