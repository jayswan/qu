#!/usr/bin/python
from __future__ import print_function
import argparse
import sys
try:
    from urllib.parse import urlparse,urlunparse
except ImportError:
    from urlparse import urlparse
    from urlparse import urlunparse

def strip_chars(s,strip_chars=["'",'"']):
    for c in strip_chars:
        s = s.replace(c,'')
    return s

def defang(url):
    # unclose URL domain components in []
    parsed = urlparse(url)
    defanged_netloc = parsed.netloc.replace('.','[.]')
    return urlunparse([parsed[0],defanged_netloc,parsed[2],parsed[3],parsed[4],parsed[5]])

def refang(url,strip_chars=['[',']']):
    # strip [] from a string, naively refanging defanged URLs
    for c in strip_chars:
        url = url.replace(c,'')
    return url

def get_tokens(input):
    # newline delimited
    if '\n' in input:
        # if it's newline delimited and has commas, strip commas
        # this accounts for printed Python list output
        input = input.replace(',','')
        tokens = [i.strip() for i in input.split('\n')]
    # comma delimited
    elif ',' in input:
        tokens = [i.strip() for i in input.split(',')]
    # space delimited
    else:
        tokens = [i.strip() for i in input.split(' ')]


    return tokens

def main():
    parser = argparse.ArgumentParser(description='Handle quoting and spacing from STDIN for use with clipboard.')
    parser.add_argument('-c','--comma',action='store_true',help='output comma delimited')
    parser.add_argument('-s','--space',action='store_true',help='output space delimited')
    parser.add_argument('-n','--newline',action='store_true',help='output newline delimited')
    parser.add_argument('-q1','--single-quote',action='store_true',help='output single quoted')
    parser.add_argument('-q2','--double-quote',action='store_true',help='output double quoted')
    parser.add_argument('-k','--splunk-or',action='store_true',help='output Splunk OR style')
    parser.add_argument('-d','--defang',action='store_true',help='naively defang URL tokens')
    parser.add_argument('-r','--refang',action='store_true',help='naively refang URL tokens')
    parser.add_argument('-e','--extra-strip-chars',help='extra chars to strip')
    args = parser.parse_args()

    input = sys.stdin.read().strip()
    input = strip_chars(input)

    tokens = get_tokens(input)

    if args.extra_strip_chars:
        tokens = [strip_chars(token,strip_chars=args.extra_strip_chars).strip() for token in tokens]

    if args.defang:
        tokens = [defang(token) for token in tokens if 'http' in token]

    if args.refang:
        tokens = [refang(token) for token in tokens if 'http' in token]

    if args.single_quote:
        tokens = ["'{}'".format(i) for i in tokens]

    if args.double_quote:
        tokens = ['"{}"'.format(i) for i in tokens]

    if args.comma:
        output = ','.join(tokens)
    elif args.newline:
        output = '\n'.join(tokens)
    # Splunk OR style
    elif args.splunk_or:
        tokens = ['"{}"'.format(i) for i in tokens]
        output = ' OR '.join(tokens)
    # default to space delimited
    else:
        output = ' '.join(tokens)

    print(output)
if __name__ == '__main__':
    main()
