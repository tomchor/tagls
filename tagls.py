from __future__ import print_function
import argparse
import os
import re

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('locations', nargs='*', help='locations to look')
parser.add_argument('-e', '--ext', dest='ext', default='pdf', type=str,
                    help='Extension of files to look for tags. If empty string, looks for all files and dirs')
parser.add_argument('-t', '--tags', dest='tags', default=None, type=str,
                    help='Tags to look for in files')
parser.add_argument('-u', '--untagged', dest='untagged', default=False, 
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

if not args.locations:
    args.locations = ['.']

if args.ext:
    rexp = r"\[([A-Za-z0-9_]+)\]\."+args.ext
else:
    rexp = r"\[([A-Za-z0-9_]+)\]"


def get_entries(places):
    entries = []
    for place in places:
        item = list(os.walk(place))
        for dirname, dirnames, filenames in item:
            if any(map(lambda x: '/.' in x, [dirname, dirnames])):
                continue
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

def parse_tags(string):
    return


entries = get_entries(args.locations)
tagstrings = get_tagString(entries)
print(tagstrings)


