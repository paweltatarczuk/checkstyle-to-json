#!/usr/bin/env python

import codecs
import sys
from argparse import ArgumentParser, FileType
from itertools import repeat
from xml.etree import ElementTree

# Parse arguments
parser = ArgumentParser(description='Add source-code context to every \
    violation to XML report.')
parser.add_argument('report', help='XML report file path')
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
args = parser.parse_args()

##
# Get n-th line context from file
##
def get_context(filepath, n, before=3, after=3):
    lines = {}

    skip = max(0, n - before)
    before = n - skip
    
    with codecs.open(filepath, 'r', 'utf-8') as handle:
        # Skip `n - before` lines
        for _ in repeat(None, skip):
            handle.readline()

        # Read the context
        for i in range(1, before + after + 2):
            lines[skip + i] = (handle.readline())

    return (skip, skip + before + after, lines)

with codecs.open(args.report, 'r', 'utf-8') as handle:
    tree = ElementTree.parse(handle)

# Iterate over all violations
for element in tree.getroot():
    if element.find('./context') is not None:
        continue

    line = int(element.attrib['line'])
    filepath = element.attrib['file']
    
    (begin, end, lines) = get_context(filepath, line, 
        before=args.before, after=args.after)
    
    contextElement = ElementTree.SubElement(element, 'context', { 
        "begin": unicode(begin),
        "end" : unicode(end) 
    })
    contextElement.text = u"\n" + unicode(''.join(lines.values()))
    
    element.append(contextElement)

tree.write(args.report, encoding='utf-8', xml_declaration=True)
