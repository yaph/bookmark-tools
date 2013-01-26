#!/usr/bin/env python
# coding: utf-8
# Convert browser bookmarks file to json for further processing.
import sys, json, requests, requests_cache, extraction
from bs4 import BeautifulSoup

def get_extract(html, url):
    e = extraction.Extractor().extract(html, source_url=url)
    return {
        'title': e.title,
        'description': e.description,
        'image': e.image,
        'url': e.url if e.url else url
    }

requests_cache.configure('urls')
alltags = []
bmfile = sys.argv[1]
html = None
with open(bmfile, 'r') as f:
    html = f.read()

not_ok = {}
links = {}
exceptions = {'request':[], 'extract':[]}
soup = BeautifulSoup(html)
for a in soup.find_all('a'):
    url = a.get('href')
    print('Processing url %s' % url)

    try:
        response = requests.get(url, verify=False, timeout=30)
    except Exception, err:
        exceptions['request'].append(url)
        print('Requesting url %s caused an exception %r' % (url, err))
        continue

    if 200 != response.status_code:
        not_ok[response.status_code] = not_ok.get(response.status_code, []) + [url]
        continue
    if response.text is None:
        print('No content for url %s' % url)
        continue

    try:
        extract = get_extract(response.text, url)
    except Exception, err:
        exceptions['extract'].append(url)
        print('Extracting content from url %s caused an exception %r' % (url, err))
        continue

    tags = a.get('tags')
    if tags:
        tags = tags.split(',')
    else:
        tags = ['__no_tag__']
    for t in tags:
        links[t] = links.get(t, []) + [extract]
    alltags += tags

with open('bookmarks.json', 'w') as f:
    json.dump({'links': links, 'not_ok': not_ok, 'tags':tags}, f)
