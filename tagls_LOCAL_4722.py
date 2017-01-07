import argparse
import os

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('locations', nargs='?', help='bar help')
parser.add_argument('-u', '--untagged', dest='untagged', default=False, 
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

if args.locations==None:
    locations='.'

def get_entries(userstring):
    return

def get_tagString(names):
    return

def parse_tags(string):
    return



