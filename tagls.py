#!/usr/bin/python
from __future__ import print_function
import argparse
import os
import re

parser = argparse.ArgumentParser(description='List files with tags')

parser.add_argument('locations', nargs='*', help='locations to look')
parser.add_argument('-e', '--ext', dest='ext', default='pdf', type=str,
                    help='Extension of files to look for tags. If empty string, looks for all files and dirs')
parser.add_argument('-t', '--tags', dest='tags', default=None, type=str,
                    help='Tags to look for in files')
parser.add_argument('-u', '--untagged', dest='untagged', default=False, action='store_true', 
                    help='If given, will print out unflagged')
parser.add_argument('-s', '--separator', dest='sep', default=',', type=str, help='Separator for tags')

args = parser.parse_args()


if not args.locations:
    args.locations = ['.']

if args.ext:
    rexp = r"\[([A-Za-z0-9,;_\-|"+args.sep+"]+)\]\."+args.ext
else:
    rexp = r"\[([A-Za-z0-9,;_\-|"+args.sep+"]+)\]"


def get_entries(places):
    entries = []
    for place in places:
        item = list(os.walk(place))
        for dirname, dirnames, filenames in item:
            #--------
            # Getting rid of hidden files
            filenames = [f for f in filenames if not f[0] == '.']
            dirnames[:] = [d for d in dirnames if not d[0] == '.']
            #--------
            entries.append(dirname)
            for filename in filenames:
                if filename.startswith('.'):
                    continue
                entries.append(os.path.join(dirname, filename))
    return entries

def get_tagString(names):
    tagstrs = {}
    for name in names:
        tagstr = re.search(rexp, name)
        if tagstr == None:
            tagstrs[name] = ''
        else:
            tagstrs[name] = tagstr.group(1)
    return tagstrs

def parse_tags(string, sep=args.sep):
    tags = string.split(',')
    tags = [ el for el in tags if el != '' ]
    return tags

def get_tagDict(entries):
    finalDict = {}
    for entry, tagstr in entries.items():
        finalDict[ entry ] = parse_tags(tagstr)
    return finalDict


entries = get_entries(args.locations)
tagstrings = get_tagString(entries)
tagsdic = get_tagDict(tagstrings)

if args.tags:
    mytags = parse_tags(args.tags)
    for entry, tags in tagsdic.items():
        if (all(x in tags for x in mytags)):
            print(entry)

else:
    tagged = []
    untagged = []
    for entry, tags in tagsdic.items():
        if tags:
            tagged.append(entry)
        else:
            untagged.append(entry)
    if args.untagged:
        print('\n'.join(untagged))
    else:
        print('\n'.join(tagged))
