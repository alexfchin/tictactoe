import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def send(txt):
    msg = MIMEMultipart()
    msg['From'] = 'csecloud356@gmail.com'
    msg['To'] = txt
    msg['Subject'] = 'test email'
    message = ' click this to verify your account on /ttt :)'
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login('csecloud356@gmail.com', 'tictactoe')
    mailserver.sendmail('csecloud356@gmail.com','iiacherry@aim.com',msg.as_string())
    mailserver.quit()

