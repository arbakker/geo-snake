#!/usr/bin/env python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import glob
import datetime
import time

me = "a.r.bakker1@gmail.com"
you = "a.r.bakker1@gmail.com"

script_name = os.path.basename(__file__)
date_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
subject = "Results {0}".format(script_name)

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text = "Results {0}\n\n".format(script_name)

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)

path = 'csv'
extension = 'csv'
os.chdir(path)
result = [i for i in glob.glob('verify_fts*.{}'.format(extension))]

for csv_file in result:
    file = open(csv_file, "r")
    content = file.read() 
    part_att = MIMEText(content, 'csv')
    msg.attach(part_att)

# Send the message via local SMTP server.
s = smtplib.SMTP('localhost', 1025)

# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(me, you, msg.as_string())
s.quit()