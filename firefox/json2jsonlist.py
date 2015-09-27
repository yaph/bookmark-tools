#!/usr/bin/env python
# coding: utf-8
import json
import click

class Bookmark():
    bookmarks = []
    tags = set()

    def parse(self, node, parents):
        ntype = node.get('type')
        if 'text/x-moz-place' == ntype:
            bm = {
                'url': node.get('uri'),
                'title': node.get('title'),
                'parents': parents
            }

            annos = node.get('annos')
            if annos:
                bm['description'] = annos[0].get('value')

            self.bookmarks.append(bm)

        elif 'text/x-moz-place-container' == ntype:
            title = node.get('title')
            if title:
                parents.append(title)

            self.tags = self.tags | set(parents)

            for child in node.get('children', []):
                self.parse(child, parents[:])

            if parents:
                parents.pop()


@click.command(help='Convert bookmarks json exported from FireFox to list of tagged urls.')
@click.argument('input', type=click.File('r'))
@click.argument('output', type=click.File('w'))
def cli(input, output):
    bm = Bookmark()
    bookmarks = json.load(input)
    bm.parse(bookmarks, [])

    # urls.append({'url': url, 'tags': tags})
    json.dump({'bookmarks': bm.bookmarks, 'tags': list(bm.tags)}, output)


if __name__ == '__main__':
    cli()