import smtplib
from email.mime.text import MIMEText


def send_mail(Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = 'c01bff72d2db58'
    password = 'c8dbb58be36f46'
    message = f"<h3>New Response Submission</h3><ul><li>Name: {Name}</li><li>Q1: {Q1}</li><li>Q2: {Q2}</li><li>Q3: {Q3}</li><li>Q4: {Q4}</li><li>Q5: {Q5}</li><li>Q6: {Q6}</li><li>Q7: {Q7}</li></ul>"

    sender_email = 'ronak.chandgadhia@gmail.com'
    receiver_email = 'ronak.chang007@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
