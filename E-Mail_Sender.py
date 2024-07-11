from Key import AppPassword
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Absender- und Empfänger-E-Mail-Adressen definieren
email_sender = 'dmitrirein545@gmail.com'
email_password = AppPassword
email_receiver = ["dmitri.rein@edu.tbz.ch", "dmitrirein545@gmail.com", "Daniel.Imbach@edu.tbz.ch"]

# HTML-Dateiinhalt lesen
with open('Temperatur.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Betreff der E-Mail erstellen
subject = 'Wetter der nächsten 5 Tagen'

# Multipart-Nachricht erstellen und Header setzen
message = MIMEMultipart()
message['From'] = email_sender
message['To'] = ", ".join(email_receiver)
message['Subject'] = subject

# HTML-Nachrichtentext anhängen
message.attach(MIMEText(html_content, 'html'))

# PDF-Datei im Binärmodus öffnen
with open("Wetter.pdf", "rb") as file:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(file.read())

# Datei in ASCII-Zeichen kodieren, um sie per E-Mail zu senden
encoders.encode_base64(part)

# Header als Schlüssel/Wert-Paar zum Anhangsteil hinzufügen
part.add_header('Content-Disposition', 'attachment; filename="Wetter.pdf"')

# Datei zur Nachricht hinzufügen
message.attach(part)

# Verbindung zum Gmail-SMTP-Server herstellen
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()  # Verbindung sichern
    server.login(email_sender, email_password)  # Beim E-Mail-Konto anmelden
    server.sendmail(email_sender, email_receiver, message.as_string())  # E-Mail senden

print("E-Mail wurde erfolgreich gesendet!")
