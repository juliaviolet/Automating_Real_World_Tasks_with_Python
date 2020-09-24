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
    resp = requests.post('http://35.184.164.140/fruits/', json=item)
    if resp.status_code != 201:
        raise Exception('POST error status={}'.format(resp.status_code))
    print('Feedback ID: {}'.format(resp.json()["id"]))
