#!/usr/bin/env python3

import os
import sys
import requests
import json
from urllib.parse import urlparse

if len(sys.argv) != 2:
    print("Usage: ./fetch_scivis.py <dataset name>")
    print("The dataset name should be all lowercase and without spaces to match the website")
    sys.exit(1)

r = requests.get("http://sci.utah.edu/~klacansky/cdn/open-scivis-datasets/{}/{}.json".format(sys.argv[1], sys.argv[1]))

script_path = os.path.dirname(os.path.realpath(__file__))
work_path = os.getcwd()

meta = r.json()
volume_path = urlparse(meta["url"])
meta["volume"] = os.path.normpath(work_path + "/" + os.path.basename(volume_path.path))

meta["camera"] = { "orbit": 5 }
meta["colormap"] = os.path.normpath(script_path + "/configs/paraview_cool_warm.png")
meta["image_size"] = [512, 512]

print("Data set Information")
print(json.dumps(meta, indent=4))
r = requests.get(meta["url"])
data = bytes(r.content)

with open(sys.argv[1] + ".json", "w") as f:
    f.write(json.dumps(meta, indent=4))

with open(os.path.basename(meta["url"]), "wb") as f:
    f.write(data)
