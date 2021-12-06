#!/usr/bin/env python

import json
import hashlib
import sys
import os
from argparse import ArgumentParser, FileType
from itertools import repeat
from xml.etree import ElementTree

# Parse arguments
parser = ArgumentParser(description='Convert and print checkstyle from stdin to \
    json file with context.')
parser.add_argument('source', type=FileType('r'), help='Source checkstyle XML file path')
parser.add_argument('dest', type=FileType('w'), help='Destination JSON file path')
parser.add_argument(
    '-B, --before',
    dest='before',
    type=int,
    default=3,
    help='Amount of lines before used for file context fetch'
)
parser.add_argument(
    '-A, --after',
    dest='after',
    type=int,
    default=3,
    help='Amount of lines after used for file context fetch'
)
parser.add_argument(
    '-G', '--gitlab',
    dest='gitlab',
    action='store_true',
    help='produce gitlab-ci compatible codeclimate-like JSON file'
)
args = parser.parse_args()

##
# Get n-th line context from file
##
def get_context(filepath, n, before=3, after=3):
    lines = {}

    skip = max(0, n - before)
    before = n - skip

    with open(filepath, "r") as handle:
        # Skip `n - before` lines
        for _ in repeat(None, skip):
            handle.readline()

        # Read the context
        for i in range(1, before + after + 2):
            lines[skip + i] = (handle.readline())

    return lines

# Gathered files data
files = {}
all_items = []

# Iterate over all files
for fileElement in ElementTree.parse(args.source).getroot():
    filepath = fileElement.attrib['name']

    # Gathered items data
    items = []

    # Iterate over all errors
    for errorElement in fileElement:
        if "line" in errorElement.attrib:
          line = int(errorElement.attrib['line'])
        else:
          line = 0
        if "column" in errorElement.attrib:
          column = int(errorElement.attrib['column'])
        else:
          column = 0
        if "source" in errorElement.attrib:
          source = errorElement.attrib['source']
        else:
          source = ""
        
        # https://github.com/codeclimate/platform/blob/master/spec/analyzers/SPEC.md
        if args.gitlab:
            fp_rel = os.path.relpath(filepath)
            item = {
                'severity': 'info',
                'categories': 'Style',
                'content': {
                    'body': '```java\n' + '\n'.join(get_context(filepath, line, # should be sorted already
                      before=args.before, after=args.after).values()) + '\n```\n'
                },
                'location': {
                    'path': fp_rel,
                    'lines': {
                        'begin': line,
                    },
                },
                'description': errorElement.attrib['message'],
                'check_name':
                  source.split('.')[-1],
            }
            fingerprint = hashlib.md5(
                json.dumps(item, sort_keys=True).encode('utf-8')).hexdigest()
            item['fingerprint'] = fingerprint
            items.append(item)
        else:
            items.append({
                'severity': errorElement.attrib['severity'],
                'source': source,
                'line': line,
                'column': column,
                'message': errorElement.attrib['message'],
                'context': get_context(filepath, line,
                    before=args.before, after=args.after),
            })
    files[filepath] = items
    all_items = all_items + items

if args.gitlab:
  # Print gathered files in json format
  args.dest.write(
      json.dumps(all_items, indent=4, sort_keys=False)
  )
else:
  # Print gathered files in json format
  args.dest.write(
      json.dumps(files, indent=4, sort_keys=False)
  )
