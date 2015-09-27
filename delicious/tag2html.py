#!/usr/bin/env python
# coding: utf-8
import sys, json, argparse
from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser(description='tag2html - Create HTML link list for given tag.')
parser.add_argument('-d', action='store_const', const=True, help='Delete given tag from bookmarks file.')
parser.add_argument('bmfile', help='Bookmarks file in JSON format.')
parser.add_argument('tag', help='The tag to generate a link list for.')
args = parser.parse_args()

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('thumbnails.html')

with open(args.bmfile, 'r') as f:
    data = json.load(f)

if args.tag not in data['links']:
    print('Tag not found: %s' % args.tag)
    sys.exit()

html = template.render(links=data['links'][args.tag])
with open('html/' + args.tag + '_list.html', 'w') as f:
    f.write(html.encode('utf-8'))

if args.d:
    del(data['links'][args.tag])
    with open(args.bmfile, 'w') as f:
        json.dump(data, f)