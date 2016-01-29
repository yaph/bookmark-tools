bookmark-tools
==============

Command line tools to work with bookmark data from browsers and services.

## Pandoc Steps

* Export bookmarks as HTML in bookmarks manger
* run html2md.sh

## FireFox Steps

* Export bookmarks as JSON in bookmarks manger
* change into firefox directory
    ./json2jsonlist.py ~/Dropbox/bookmarks/bookmarks-2016-01-28.json bookmarks-list.json
    ./clean.py bookmarks-list.json
    ./tag2ms.py bookmarks-list.json TAGNAME

## Linkcheck

* Install and test LinkChecker with local HTML file https://pypi.python.org/pypi/LinkChecker
