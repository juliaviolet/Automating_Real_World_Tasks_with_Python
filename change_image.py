#!/usr/bin/env python3

import os
from PIL import Image

image_path = os.path.expanduser('~') + '/supplier-data/images/'

for image in os.listdir(image_path):
    if '.tiff' in image and '.' not in image[0]:
        img = Image.open(image_path + image)
        img.resize((600, 400)).convert("RGB").save(image_path + image.split('.')[0] + '.jpeg', 'jpeg')
        img.close()
