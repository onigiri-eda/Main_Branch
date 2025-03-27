import os
import logging
import random
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("email_system.log"),
        logging.StreamHandler()
    ]
)

class EmailSystem:
    def __init__(self):
        self.delivery_statuses = []
        self.report_dir = "delivery_reports"
        self.replies_dir = "received_mails"
        self._setup_directories()

    def _setup_directories(self):
        """Create required directories if they don't exist"""
        try:
            os.makedirs(self.report_dir, exist_ok=True)
            os.makedirs(self.replies_dir, exist_ok=True)
        except OSError as e:
            logging.error(f"Directory creation failed: {e}")
            raise

    def send_message(self, sent_email_id, message_content):
        """Simulate message sending with random success/failure"""
        try:
            # Simulate sending process
            if random.random() < 0.8:  # 80% success rate
                logging.info(f"Message {sent_email_id} sent successfully")
                self._record_delivery_status(sent_email_id, "DELIVERED")
                
                # Simulate receiving a reply
                if random.random() < 0.3:  # 30% chance of reply
                    self.save_reply(
                        sent_email_id,
                        "Thank you for your message!\nBest regards,\nRecipient"
                    )
                return True
            else:
                raise Exception("Simulated network error")
                
        except Exception as e:
            logging.error(f"Failed to send message {sent_email_id}: {str(e)}")
            self._record_delivery_status(sent_email_id, "FAILED", str(e))
            return False

    def _record_delivery_status(self, email_id, status, error=None):
        """Record message delivery status"""
        self.delivery_statuses.append({
            "email_id": email_id,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "error": error
        })

    def save_reply(self, sent_email_id, reply_text):
        """Save reply to a file with proper error handling"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.replies_dir}/reply_{sent_email_id}_{timestamp}.txt"
            
            content = (
                f"Sent Email ID: {sent_email_id}\n"
                f"Received At: {datetime.now().isoformat()}\n\n"
                f"{reply_text}"
            )

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logging.info(f"Reply saved: {filename}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save reply for {sent_email_id}: {str(e)}")
            return False

    def generate_delivery_report(self):
        """Generate comprehensive delivery report"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"{self.report_dir}/delivery_report_{timestamp}.txt"
            
            report_content = [
                "Email Delivery Report",
                "=" * 40,
                f"Generated at: {datetime.now().isoformat()}",
                "\nStatus Summary:"
            ]

            # Count statistics
            total = len(self.delivery_statuses)
            success = sum(1 for s in self.delivery_statuses if s["status"] == "DELIVERED")
            failure = total - success

            report_content.extend([
                f"Total messages: {total}",
                f"Successfully delivered: {success}",
                f"Failed deliveries: {failure}",
                "\nDetailed Report:",
                "ID\tStatus\tTimestamp\t\tError"
            ])

            # Add individual records
            for record in self.delivery_statuses:
                report_content.append(
                    f"{record['email_id']}\t"

f"{record['status']}\t"
                    f"{record['timestamp']}\t"
                    f"{record['error'] or 'N/A'}"
                )

            with open(report_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_content))

            logging.info(f"Generated delivery report: {report_path}")
            return True

        except Exception as e:
            logging.error(f"Failed to generate report: {str(e)}")
            return False

if os.name == "__main__":
    email_system = EmailSystem()
    
    # Simulate sending 10 messages
    for message_id in range(1, 11):
        email_system.send_message(
            sent_email_id=message_id,
            message_content=f"Important message #{message_id}"
        )
    
    # Generate final report
    email_system.generate_delivery_report()