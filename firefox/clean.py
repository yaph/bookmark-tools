#!/usr/bin/env python
# coding: utf-8
import argparse
import json

import requests
import requests_cache

from lassie import Lassie


parser = argparse.ArgumentParser(description='Separates URLs with 200 status code from those without.')
parser.add_argument('bmfile', help='Bookmarks file in JSON list format.')
args = parser.parse_args()

not_ok = []
bookmarks = []

requests_cache.configure('../cache/requests')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.130 Chrome/43.0.2357.130 Safari/537.36'
headers = {'User-Agent': user_agent}
l = Lassie()
l.request_opts = {'headers': headers}
webclient = requests.Session()
webclient.headers.update(headers)


with open(args.bmfile, 'r') as f:
    data = json.load(f)

for i, b in enumerate(data['bookmarks']):
    url = b['url']
    if not url or not url.startswith(('http', 'https')):
        continue

    print('#{}: {}'.format(i, url))
    try:
        resp = webclient.head(url, timeout=10, headers={'User-Agent': user_agent})
        b['status'] = resp.status_code
    except Exception as err:
        print('Request failed: {}'.format(err))
        continue
    if b['status'] != 200:
        not_ok.append(b)
        continue

    # Follow redirects one hop.
    if resp.is_redirect:
        url = resp.headers['Location']

    if resp.headers.get('content-type', '').startswith('text/html'):
        try:
            summary = l.fetch(url)
            b['title'] = summary['title'].strip()
            b['url'] = summary['url'].strip()
        except Exception as err:
            print('Fetching {} failed with error:\n{}'.format(url, err))

    bookmarks.append(b)

data['bookmarks'] = bookmarks

with open('cleaned_' + args.bmfile, 'w') as f:
    json.dump(data, f)

with open('not_ok.json', 'w') as f:
    json.dump(not_ok, f)