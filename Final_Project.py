#!/usr/bin/env python3

import os
from PIL import Image

image_path = os.path.expanduser('~') + '/supplier-data/images/'

for image in os.listdir(image_path):
    if '.tiff' in image and '.' not in image[0]:
        img = Image.open(image_path + image)
        img.resize((600, 400)).convert("RGB").save(image_path + image.split('.')[0] + '.jpeg', 'jpeg')
        img.close()


#!/usr/bin/env python3

import requests
import os

url = "http://localhost/upload/"
#image_directory = os.path.expanduser('~') + '/supplier-data/images/'mage_list = os.listdir(image_directory)

image_path = 'supplier-data/images/'
jpeg_images  = [image for image in os.listdir(image_path) if '.jpeg' in image]

for image in jpeg_images:
        with open(image_path+image, 'rb') as opened:
                r = requests.post(url, files={'file': opened})

#! /usr/bin/env python3

import os
import requests
import re

text_path = 'supplier-data/descriptions/'
image_path = 'supplier-data/images/'

#text_path = os.path.expanduser('~') + '/supplier-data/descriptions/'
text_files_list = sorted(os.listdir(text_path))

#image_path = os.path.expanduser('~') + '/supplier-data/images/'
image_files_list = sorted([image_name for image_name in os.listdir(image_path) if '.jpeg' in image_name])

list = []
image_count = 0

for text_file in text_files_list:

    format = ['name', 'weight', 'description']

    with open(text_path + text_file, 'r') as f:
        data = {}
        contents = f.read().split("\n")[0:3]
        contents[1] = int((re.search(r'\d+', contents[1])).group())

        counter = 0
        for content in contents:
            data[format[counter]] = content
            counter += 1

        data['image_name'] = image_files_list[image_count]

        list.append(data)
        image_count += 1

for item in list:
    resp = requests.post('http://34.123.127.8/fruits/', json=item)
    if resp.status_code != 201:
        raise Exception('POST error status={}'.format(resp.status_code))
    print('Feedback ID: {}'.format(resp.json()["id"]))

#!/usr/bin/env python3

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_report(filename, title, additional_info):
    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(filename)
    report_title = Paragraph(title, styles["h1"])
    report_info = Paragraph(additional_info, styles["Normal"])
    empty_line = Spacer(1,20)
    report.build([report_title, empty_line, report_info])

#!/usr/bin/env python3

import reports
import emails
import os

from datetime import date

text_path = os.path.expanduser('~') + '/supplier-data/descriptions/'
report = []

def import_data(data):
    for item in data:
        report.append("name: {}<br/>weight: {}\n".format(item[0], item[1]))
    return report

data_text = []

for text_file in os.listdir(text_path):
    with open(text_path + text_file, 'r') as f:
        data_text.append([line.strip() for line in f.readlines()])
        f.close()

if __name__ == "__main__":

    summary = import_data(data_text)

    summary_paragraph = "<br/><br/>".join(summary)

    title = "Supplier Update on {}\n".format(date.today().strftime("%B %d, %Y"))
    attachment = "/tmp/processed.pdf"

    reports.generate_report(attachment, title, summary_paragraph)

    subject = "Online Fruit Store Import Done"
    sender = "automation@example.com"
    receiver = "{}@example.com".format(os.environ.get('USER'))
    body = "The information in your catalog has been successfully updated with the information provided by your suppliers. For details, see the attached list."
    message = emails.generate_email(sender, receiver, subject, body, attachment)
    emails.send_email(message)

import email.message
import mimetypes
import os.path
import smtplib

def generate_email(sender, recipient, subject, body, attachment_path):
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    attachment_filename = os.path.basename(attachment_path)
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type, mime_subtype = mime_type.split('/', 1)

    with open(attachment_path, 'rb')as ap:
        message.add_attachment(ap.read(),
                               maintype = mime_type,
                               subtype = mime_subtype,
                               filename = attachment_filename)
    return message

def send_email(message):
        mail_server = smtplib.SMTP('localhost')
        mail_server.send_message(message)
        mail_server.quit()

def generate_error_report(sender, recipient, subject, body):
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    return message

#!/usr/bin/env python3

import os
import shutil
import psutil
import socket
from emails import generate_error_report, send_email
import time

def check_CPU_usage():
    usage = psutil.cpu_percent(1)
    return usage > 80

def check_disk_usage(disk):
    disk_usage = shutil.disk_usage(disk)
    free_space = disk_usage.free / disk_usage.total * 100
    return free_space > 20

def check_free_memory():
    free_memory = psutil.virtual_memory().available/(1024*1024)
    return free_memory > 500

def check_localhost():
    localhost = socket.gethostbyname('localhost')
    return localhost == '127.0.0.1'

if check_CPU_usage():
    error_message = "CPU usage is over 80%"
elif not check_disk_usage('/'):
    error_message = "Available disk space is less than 20%"
elif not check_free_memory():
    error_message = "Available memory is less than 500MB"
elif not check_localhost():
    error_message = 'localhost cannot be resolved to 127.0.0.1'
else:
    pass

if __name__ == "__main__":
    try:
        sender = "automation@example.com"
        receiver = "{}@example.com".format(os.environ.get('USER'))
        subject = "Error - {}".format(error_message)
        body = "Please check your system and resolve the issue as soon as possible."
        message = generate_error_report(sender, receiver, subject, body)
        send_email(message)
    except NameError:
        pass
