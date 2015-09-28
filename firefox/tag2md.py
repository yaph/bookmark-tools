#!/usr/bin/env python
# coding: utf-8
import argparse
import json
import sys
from collections import defaultdict


parser = argparse.ArgumentParser(description='Create HTML link list for given tag.')
parser.add_argument('bmfile', help='Bookmarks file in JSON list format.')
parser.add_argument('tag', help='The tag to generate a link list for.')
args = parser.parse_args()

bookmarks = []
markdown = ''
tag_groups = defaultdict(list)
tpl_item = '* [{}]({})'

with open(args.bmfile, 'r') as f:
    data = json.load(f)

for b in data['bookmarks']:
    if not b['url'].startswith(('http', 'https')) or args.tag not in b['parents']:
        continue
    tag_groups[' • '.join(b['parents'])].append(tpl_item.format(b['title'], b['url']))

if not tag_groups:
    print('Tag not found: %s' % args.tag)
    sys.exit()

for group, links in tag_groups.items():
    markdown += '## {}\n\n{}\n\n'.format(group, '\n'.join(sorted(links)))

with open('../md/' + args.tag + '_list.md', 'w') as f:
    f.write(markdown)