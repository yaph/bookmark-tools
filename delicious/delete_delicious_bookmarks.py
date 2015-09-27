#!/usr/bin/env python
# coding: utf-8
# remove all your bookmarks from delicious
import sys, json, requests

if 3 != len(sys.argv):
    print "Usage\n%s user password" %sys.argv[0]

user = sys.argv[1]
pw = sys.argv[2]

r = requests.get('https://api.delicious.com/v1/json/posts/all', auth=(user, pw))
posts = json.loads(r.content)['posts']
for p in posts:
    requests.get('https://api.delicious.com/v1/posts/delete', params={'md5': p['post']['hash']}, auth=(user, pw))
