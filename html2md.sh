#!/bin/bash
set -euo pipefail

file=${1:-}
if [[ -z "$file" ]]; then
    echo "usage: $0 bookmarks.html"
    exit 1
fi

pandoc -t markdown -o md/bookmarks.md ${1}
