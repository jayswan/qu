#!/usr/bin/python
from __future__ import print_function
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Handle quoting and spacing from STDIN for use with clipboard.')
    parser.add_argument('-c','--comma',action='store_true',help='output comma delimited')
    parser.add_argument('-s','--space',action='store_true',help='output space delimited')
    parser.add_argument('-n','--newline',action='store_true',help='output newline delimited')
    parser.add_argument('-q1','--single-quote',action='store_true',help='output single quoted')
    parser.add_argument('-q2','--double-quote',action='store_true',help='output double quoted')
    parser.add_argument('-k','--splunk-or',action='store_true',help='output Splunk OR style')
    args = parser.parse_args()

    input = sys.stdin.read().strip()
    quote_chars =["'",'"']
    for c in quote_chars:
        input = input.replace(c,'')

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
