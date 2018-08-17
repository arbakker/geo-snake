#!/usr/bin/env python
"""checkmk_check_wms_layers_geoserver.py: Check MK local check to test for all layers in GeoServer if the WMS service for that layer is functional"""
import check_featuretypes_geoserver
import csv
import configparser
import smtplib
import os
import glob
import datetime
import time
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename

def send_email(email_from, email_to, broken, working):
    me = email_from
    you = email_to

    host_name =  socket.gethostname()
    script_name = os.path.basename(__file__)
    date_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    subject = "Results {0} on {1} - {2}/{3}".format(script_name, host_name, broken, working)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Results {0} on {1} - {2}\n\nbroken featuretypes: {3}\nworking featuretypes: {4}".format(script_name, host_name, date_stamp, broken, working)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)

    path = check_featuretypes_geoserver.get_csv_path()
    extension = 'csv'
    os.chdir(path)
    result = [i for i in glob.glob("verify_fts*.{0}".format(extension))]


    for csv_file in result:
	with open(csv_file, "rb") as my_file:
	    part = MIMEApplication(my_file.read(), Name=basename(csv_file))
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(csv_file)
	    msg.attach(part)
	

    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')

    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit() 

def main():
    # required to make checkmk_verify_layers.ini in this folder to set url to check with credentials:
    # example checkmk_check_wms_layers_geoserver.ini:
    # [DEFAULT]
    # user = admin
    # password = geoserver
    # url = http://localhost:8000/geoserver/
    base_path = os.path.abspath(os.path.dirname(__file__))
    config = configparser.ConfigParser()
    config.read(os.path.join(base_path, u'checkmk_check.ini'))
    user = config['DEFAULT']['user']
    password = config['DEFAULT']['password']
    url = config['DEFAULT']['url']
    email_to = config['DEFAULT']['email_to']
    email_from = config['DEFAULT']['email_from']

    check_featuretypes_geoserver.main([user, password, url])
    csv_path = check_featuretypes_geoserver.get_csv_path()
    count_csv_file = check_featuretypes_geoserver.get_count_csv_file(csv_path)

    total_broken = -1
    total_working = -1

    with open(count_csv_file) as csvfile:
        reader = csv.DictReader(csvfile,delimiter='@')
        for row in reader:
            if row['workspace_name'] == "total":
                total_working = int(row['working_fts'])
                total_broken = int(row['broken_fts'])

    if total_broken ==0:
        status = 0 
    elif total_broken > 0:
        status = 3


    send_email(email_from, email_to, total_broken, total_working)
    status_string = "total fts: {0}, broken fts: {1}".format(total_working+total_broken, total_broken)
    print("{0} {1} invalid_fts={2} {3}".format(status, "Monitor-FeatureTypes-GeoServer", total_broken, status_string))

if __name__ == "__main__":
    main()
