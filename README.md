# qu
Handle data quotation and spacing in the clipboard.

I constantly need to transform data in the clipboard between various formats:

- SQL (single quoted or unquoted comma-separated)
- newline (copied from shell stdout, email, etc.)
- Python printed objects (such as single-quoted lists of strings)
- Elasticsearch query strings (space separated unquoted, or double quoted JSON style lists)
- many others

I got tired of doing this with chains of shell utilities, so `qu` is a simple script that reads from STDIN, tries to infer the input format, and outputs the desired format according to the CLI switches.

## Installation
- Clone this repo.
- `cp qu.py qu`
- `chmod +x qu`
- `mv qu <wherever in your path you put your local hacks>`
  - I use `/usr/local/bin` for local hack-scripts but people have Opinions on this, so do what you like.

## Inputs
- newline delimted (commas stripped)
- comma delimted
- space delimted

## Outputs
- single quoted
- double quoted
- unquoted
- comma delimted
- space delimited
- newline delimted
- Splunk "OR" formatting

## Examples
```
$ qu -h
usage: qu [-h] [-c] [-s] [-n] [-q1] [-q2] [-k]

Handle quoting and spacing from STDIN for use with clipboard.

optional arguments:
  -h, --help           show this help message and exit
  -c, --comma          output comma delimited
  -s, --space          output space delimited
  -n, --newline        output newline delimited
  -q1, --single-quote  output single quoted
  -q2, --double-quote  output double quoted
  -k, --splunk-or      output Splunk OR style
```

```
12:54 $ pbpaste
foo bar baz
✔ /tmp
12:54 $ pbpaste | qu -n
foo
bar
baz
✔ /tmp
12:54 $ pbpaste | qu -k
"foo" OR "bar" OR "baz"
✔ /tmp
12:54 $ pbpaste | qu -q1 -c
'foo','bar','baz'
```
