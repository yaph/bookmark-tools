#!/usr/bin/env python
# coding: utf-8
import argparse
import json
import sys


parser = argparse.ArgumentParser(description='tag2html - Create HTML link list for given tag.')
parser.add_argument('bmfile', help='Bookmarks file in JSON format.')
parser.add_argument('tag', help='The tag to generate a link list for.')
args = parser.parse_args()

bookmarks = []
tpl_item = '* [{}]({})'

with open(args.bmfile, 'r') as f:
    data = json.load(f)

for b in data['bookmarks']:
    if args.tag not in b['parents']:
        continue
    bookmarks.append(tpl_item.format(b['title'], b['url']))

if not bookmarks:
    print('Tag not found: %s' % args.tag)
    sys.exit()

with open('../md/' + args.tag + '_list.md', 'w') as f:
    f.write('\n'.join(bookmarks))