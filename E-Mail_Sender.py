from Key import AppPassword
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Define email sender and receiver
email_sender = 'dmitrirein545@gmail.com'
email_password = AppPassword
email_receiver = ["dmitri.rein@edu.tbz.ch", "dmitrirein545@gmail.com", "Daniel.Imbach@edu.tbz.ch"]

# Read the HTML file content
with open('Temperatur.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Create the email subject
subject = 'Wetter der nächsten 5 Tagen'

# Create a multipart message and set headers
message = MIMEMultipart()
message['From'] = email_sender
message['To'] = ", ".join(email_receiver)
message['Subject'] = subject

# Attach the HTML message body
message.attach(MIMEText(html_content, 'html'))

# Open the PDF file in binary mode
with open("Wetter.pdf", "rb") as file:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(file.read())

# Encode the file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header('Content-Disposition', 'attachment; filename="Wetter.pdf"')

# Attach the file to the message
message.attach(part)

# Connect to the Gmail SMTP server
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()  # Secure the connection
    server.login(email_sender, email_password)  # Log in to the email account
    server.sendmail(email_sender, email_receiver, message.as_string())  # Send the email

print("Email sent successfully!")
