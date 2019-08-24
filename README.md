# qu
"This seemed dumb at first but now I use it all the time." - a colleague

Handle data quotation and spacing in the clipboard.

I constantly need to transform data in the clipboard between various formats:

- SQL (single quoted or unquoted comma-separated)
- newline (copied from shell stdout, email, etc.)
- Python printed objects (such as single-quoted lists of strings)
- Elasticsearch query strings (space separated unquoted, or double quoted JSON style lists)
- Splunk single-quoted query lists (for searches like `index=foo src_ip IN ('1.1.1.1','2.2.2.2')`
- Splunk `TERM` wraps like `index=foo TERM("1.1.1.1") OR TERM("2.2.2.2")`

I got tired of doing this with chains of shell utilities, so `qu` is a simple script that reads from STDIN, tries to infer the input format, and outputs the desired format according to the CLI switches.

## Installation
- Clone this repo.
- `cp qu.py qu`
- `chmod +x qu`
- `mv qu <wherever in your path you put your local hacks>`
  - I use `/usr/local/bin` for local hack-scripts but people have Opinions :tm: on this, so do what you like.

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
- Splunk "OR" formatting with each term wrapped in `TERM()`
- defanged URL (e.g. `https://foo[.]com`)
- refanged URL (e.g. `hxxps://foo[.]com` -> `https://foo.com`)

## Examples
```
usage: qu [-h] [-c] [-s] [-n] [-q1] [-q2] [-k] [-T] [-d] [-r]
          [-e EXTRA_STRIP_CHARS]

Handle quoting and spacing from STDIN for use with clipboard.

optional arguments:
  -h, --help            show this help message and exit
  -c, --comma           output comma delimited
  -s, --space           output space delimited
  -n, --newline         output newline delimited
  -q1, --single-quote   output single quoted
  -q2, --double-quote   output double quoted
  -k, --splunk-or       output Splunk OR style
  -T, --term            output Splunk OR wrapped in TERM()
  -d, --defang          naively defang URL tokens
  -r, --refang          naively refang URL tokens
  -e EXTRA_STRIP_CHARS, --extra-strip-chars EXTRA_STRIP_CHARS
                        extra chars to strip
```

Some examples:

```
Clipboard contains the string "1.1.1.1 2.2.2.2 3.3.3.3" (space delimited):

16:05 $ pbpaste
1.1.1.1 2.2.2.2 3.3.3.3

Output as newlines:

16:05 $ pbpaste | qu -n
1.1.1.1
2.2.2.2
3.3.3.3

Output CSV with no quoting:

16:05 $ pbpaste | qu -c
1.1.1.1,2.2.2.2,3.3.3.3

Output CSV with single quotes:

16:05 $ pbpaste | qu -c -q1
'1.1.1.1','2.2.2.2','3.3.3.3'

Output Splunk OR style with or without TERM() wrap:

16:05 $ pbpaste | qu -T
TERM("1.1.1.1") OR TERM("2.2.2.2") OR TERM("3.3.3.3")
16:06 $ pbpaste | qu -k
"1.1.1.1" OR "2.2.2.2" OR "3.3.3.3"
```
