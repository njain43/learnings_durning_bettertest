import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


def send_email_with_report():
    # Email details
    sender = "mailtoniteshjain@gmail.com"
    recipient = "nitesh.jain@credit-suisse.com"
    subject = "test email"
    smtp_server = "127.0.0.1"
    smtp_port = 8001
    # smtp_username = "your_username"
    # smtp_password = "your_password"

    # Read the contents of the report.html file
    report_path = "C:\\Users\\nites\\IdeaProjects\\hackerrankquestions\\report.html"
    print(report_path)
    with open("C:\\Users\\areport.html", "r",encoding='utf-8') as file:
        report_content = file.read()

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    # Attach the report content as an HTML body
    msg.attach(MIMEText(report_content, "html"))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        # server.login(smtp_username, smtp_password)
        server.send_message(msg)

# Call the function to send the email with the Robot Framework report
send_email_with_report()