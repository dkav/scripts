#!/usr/bin/python

import smtplib
import csv
import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def write_msg(fname, sender, receiver):
    """ Write a message"""
    # Message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "SUBJECT"
    msg['From'] = sender
    msg['To'] = receiver

    # Body of message
    text = "Text".format(fname)

    html = """\
<html>
<head></head>
<body>

</body>
</html>""".format(fname)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    return msg


def main():
    """Main"""
    # SMTP server connection settings
    server = 'smtp.server.com:587'
    smtp_user = 'USER'
    smtp_pwd = getpass.getpass("Enter your SMTP server password:")
    sender = 'SENDER'

    # Data file
    fn = ('xxx.csv')

    # Read in account information
    csvfile = open(fn, "rb")
    reader = csv.reader(csvfile)
    reader.next()
    data = [row for row in reader]
    csvfile.close()
    snd_email = raw_input("Send email/s y or n:")
    if snd_email == "y":
        try:
            smtpserver = smtplib.SMTP(server)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(smtp_user, smtp_pwd)
        except smtplib.SMTPException:
            print "Error: unable to connect to SMTP server"

        for fname, lname, email in data:
            receiver = ' '.join([fname, lname, ''.join(['<', email, '>'])])
            print "Message to {0}".format(receiver)
            msg = write_msg(fname, sender, receiver)
            try:
                smtpserver.sendmail(sender, receiver, msg.as_string())
                print "Successfully sent email"
            except smtplib.SMTPException:
                print "Error: unable to send email"

        smtpserver.close()


if __name__ == "__main__":
    main()
