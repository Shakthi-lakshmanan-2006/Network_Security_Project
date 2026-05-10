import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import Config
from utils.logger import logger

class EmailService:
    @staticmethod
    def send_security_alert(alert_type, severity, description, source_ip):
        """Send email alert to administrator"""
        if not Config.EMAIL_USER or not Config.EMAIL_PASSWORD:
            logger.warning("Email settings not configured. Skipping email alert.")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.EMAIL_USER
            msg['To'] = Config.ALERT_EMAIL
            msg['Subject'] = f"🚨 [{severity.upper()}] Security Alert: {alert_type}"
            
            body = f"""
            <html>
            <body>
                <h2 style="color: #d32f2f;">Network Security Alert</h2>
                <hr/>
                <table style="border-collapse: collapse; width: 100%;">
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Alert Type:</td>
                        <td style="padding: 8px;">{alert_type}</td>
                    </tr>
                    <tr style="background-color: #f5f5f5;">
                        <td style="padding: 8px; font-weight: bold;">Severity:</td>
                        <td style="padding: 8px; color: #d32f2f;">{severity.upper()}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Source IP:</td>
                        <td style="padding: 8px;">{source_ip}</td>
                    </tr>
                    <tr style="background-color: #f5f5f5;">
                        <td style="padding: 8px; font-weight: bold;">Description:</td>
                        <td style="padding: 8px;">{description}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight: bold;">Timestamp:</td>
                        <td style="padding: 8px;">{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</td>
                    </tr>
                </table>
                <br/>
                <p style="color: #666;">Please login to the admin dashboard immediately to investigate and take action.</p>
                <p style="color: #666;"><strong>Network Security System</strong></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT)
            server.starttls()
            server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Alert email sent to {Config.ALERT_EMAIL}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {str(e)}")
            return False