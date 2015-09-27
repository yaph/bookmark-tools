# -*- coding: utf-8 -*-
import requests, requests_cache, json, re
from bs4 import BeautifulSoup

requests_cache.configure('delicious_links')
urllist = []
re_ws = re.compile(r'\s+')

def cleanws(s):
    return re.sub(re_ws, ' ', s)

with open('data.json') as f:
    bookmarks = json.load(f)

for p in bookmarks['posts']:
    url = p['post']['href']
    r = requests.get(url)
    if 200 != r.status_code:
        continue

    soup = BeautifulSoup(r.text)

    if not soup.title:
        continue
    title = soup.title.text

    try:
        description = str(soup.find_all('meta', attrs={'name':'description'})[0]['content'])
    except:
        if soup.p:
            description = soup.p.text
        else:
            description = ''

    urllist.append({'url': url, 'title': cleanws(title), 'description': cleanws(description)})

    # call phantomjs
    # http://packages.python.org/pypng/index.html

print urllist
