import requests
import os

url = "http://localhost/upload/"
#image_directory = os.path.expanduser('~') + '/supplier-data/images/'mage_list = os.listdir(image_directory)

image_path = 'supplier-data/images/'
jpeg_images  = [image for image in os.listdir(image_path) if '.jpeg' in image]

for image in jpeg_images:
        with open(image_path+image, 'rb') as opened:
                r = requests.post(url, files={'file': opened})
