#!/usr/bin/env python
# coding: utf-8
import argparse
import json
import requests
import sys


parser = argparse.ArgumentParser(description='Create HTML link list for given tag.')
parser.add_argument('bmfile', help='Bookmarks file in JSON list format.')
args = parser.parse_args()

not_ok = []

with open(args.bmfile, 'r') as f:
    data = json.load(f)

for i, b in enumerate(data['bookmarks']):
    url = b['url']
    if not url.startswith(('http', 'https')):
        continue
    print('#{}: {}'.format(i, url))
    try:
        b['status'] = requests.get(url).status_code
    except Exception as err:
        print('Request failed: {}'.format(err))
        continue
    if b['status'] != 200:
        not_ok.append(b)
        del b

with open(args.bmfile, 'w') as f:
    json.dump(data, f)

with open('not_ok.json', 'w') as f:
    json.dump(not_ok, f)