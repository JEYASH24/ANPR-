import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to

    user = "licenseplatetst@gmail.com"
    msg['From'] = user
    password = "wpgftszskfheyanp"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

if __name__ == '__main__':
    email_alert("HEY, IT'S AN ALERT FOR YOUR VEHICLE", "This is a test alert.", "mailtojeyash@gmail.com")
