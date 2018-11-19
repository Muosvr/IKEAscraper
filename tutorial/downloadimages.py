#! /usr/bin/python3.7

import json
import urllib.request as request
import sys

# print(sys.version)
image_limit = 500
with open("IKEAimages.json") as f:
    data = json.load(f)

for product in data[:image_limit]:
    request.urlretrieve(product["img_url"],"IKEAimages/"+product["image_name"])
