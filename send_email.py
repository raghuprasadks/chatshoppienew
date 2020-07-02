from email.mime.text import MIMEText
import smtplib


def send_email(email,name):

    from_email="anupg76@gmail.com"
    from_password="kalkiii76"
    to_email=email


    subject="Welcome to Chatshoppie"
    message="Congratulations... you have now registered for Chatshoppie.com, the one stop shop for all Shopping. It's as easy as Chating"

    msg=MIMEText(message,'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_password)
    gmail.send_message(msg)


