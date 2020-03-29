################################################################################
#                                                                              #
#            Tool to clean text from all or user selected things               #
#                                                                              #
# - Without any parameters it will show usage instructions                     #
# - Called with file input name only, it will show file stats, i.e. file size, #
#  number of words, then clean from everything and save lower case words list  #
#  in csv format.                                                              #
# - Rest is according to the parameters                                        #
#                                                                              #
# 1. Open file                                                                 #
# 2. Get / show / save file stats                                              #
# 3. User selected options for cleaning: either by args / options or via GUI   #
# 4. Process text                                                              #
# 5. Save output in user selected format: plain text, csv, ?                   #
#                                                                              #
################################################################################

# Import required modules
import os
import sys
import requests
import argparse
import additions as addons
import processors as procs

# Create message colors instance
color = addons.Color()

version = "Text Processor. Ver 0.1 (c) 2017-2020 Denis Rasulev. All Rights " \
          "Reserved."

# Description of what the tool does
description = """
Script cleans SOURCE from all (default) or only user selected elements.

USAGE:

> python tp.py
Shows short usage info.

> python tp.py -h, --help
Shows this help message.

> python tp.py SOURCE
Script attempts to read SOURCE for further processing. 

Those elements are removed from the SOURCE by default:
- punctuation
- single letters
- extra spaces
- stop words
- digits

Some extra work done by script:
- spelling correction, including common abbreviations
- non-unicode characters are converted to unicode analogs

If output file name was not specified, the result is saved to .csv file
named as SOURCE with appended '_cleaned' word. For instance, if you called
'tp.py text.txt' then the result will be saved to 'text_cleaned.csv' file.

You can specify output file name with the following option:

> python tp.py SOURCE -o OUTPUT, --ofile OUTPUT
Script saves processed information to OUTPUT

By default it saves result as comma-separated list of words in lower case.

You can specify OUTPUT file format with the following option:

> python tp.py SOURCE -f CSV|TXT, --format CSV|TXT
Script will save output file in specified format.
"""

epilog = version

# Create arguments parser
parser = argparse.ArgumentParser(
    prog='tp.py',
    add_help=False,
    usage='%(prog)s source [-o output] [-f format]',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description,
    epilog=epilog)

# Add command line arguments
parser.add_argument('ifile',
                    metavar='SOURCE',
                    help="source to be processed")
parser.add_argument('-o', '--ofile',
                    metavar='OUTPUT',
                    help="specifies output file name")
parser.add_argument('-f', '--format',
                    metavar='FORMAT',
                    default='csv',
                    help="specifies output file format: csv or txt")

# If script is called without any arguments, print short usage note and exit
if len(sys.argv) == 1:
    print(version)
    print("")
    print("usage: tp.py source [-o output] [-f format]")
    print(" source   required, file name")
    print(" output   optional, file name")
    print(" format   optional, csv or txt")
    print("")
    print("help:     tp.py -h, --help")
    sys.exit(0)

# If script called with any argument requesting help, print help and exit
if sys.argv[1] in ['?', '/?', '-h', '--help']:
    parser.print_help()
    sys.exit(0)

if sys.argv[1] in ['-v', '--version']:
    print(version)
    sys.exit(0)

# If any other arguments were provided, parse them
args = parser.parse_args()

# Default output file extension is .csv. If user specified .txt, then use it
extension = ".csv"
if args.format == 'txt':
    extension = ".txt"

# By default we say that output file exists, so we append to it rather than
# overwrite, which is safer option
file_exists = True

# If user provided URL as a SOURCE
if args.ifile.startswith('http') or args.ifile.startswith('https'):

    # Connect to the requested URL
    try:
        # Wait for the response from server 5 sec and do not allow redirects
        r = requests.get(args.ifile, timeout=5, allow_redirects=False)

    # If r.status_code != requests.codes.ok
    except requests.ConnectionError or requests.Timeout as e:
        print("This error happened while processing the requested URL:")
        print(str(e))
        sys.exit(1)

    # We shall process only these types of contents
    allowed_content_types = ['text/plain',
                             'text/html',
                             'text/xml',
                             'text/csv',
                             'text/css',
                             'application/xml',
                             'application/json']

    if r.headers['content-type'].split(';')[0] in allowed_content_types:
        # Override encoding by real educated guess as provided by chardet
        r.encoding = r.apparent_encoding

        # Get content
        source_text = r.text

        # Set args and parameters if we process URL
        # TODO: get domain to save as output file name
        args.ofile = 'url_content_cleaned' + extension
        file_exists = addons.check_if_file_exists(args.ofile)
        size = 0
        lines = 0
        words = 0

    # If URL contains anything else, except what we can process, notify and exit
    else:
        print("Requested URL has different content than text, xml or json)")
        print("Content type:", r.headers['content-type'])
        sys.exit(1)

# If input is not URL, then we suppose it's file
else:
    f = open(args.ifile, 'r')
    source_text = open(args.ifile, 'r').read()

    # Set args and parameters if we process file
    size = addons.sizeof_fmt(os.path.getsize(args.ifile))
    lines = addons.count_lines(args.ifile)
    words = addons.count_words(args.ifile)

# If output file format is ommited then construct new output file name
if args.ofile is None:
    args.ofile = os.path.splitext(args.ifile)[0] + "_cleaned" + extension
    file_exists = addons.check_if_file_exists(args.ofile)

# Print received arguments and basic info
print("Input")
print("- file   : {}".format(args.ifile))
print("- size   : {}".format(size))
print("- lines  : {}".format(lines))
print("- words  : {}".format(words))
print("Output")
print("- file   : {}".format(args.ofile))
print("- format : {}".format(args.format))
print("- status : {}".format('append' if file_exists else 'overwrite'))

# Confirm if user wants to continue
answer = input(color.WARN + "\nProceed? (y/n): " + color.DFLT)

# If user cancels, notify and abort
if answer not in ['y', 'Y']:
    print(color.FAIL + "Operation aborted." + color.DFLT)
    sys.exit(0)

# Text processing
cleaned_text = procs.remove_punctuation(source_text)
cleaned_text = procs.remove_extra_spaces(cleaned_text)
cleaned_text = procs.remove_single_chars(cleaned_text)
cleaned_text = procs.remove_digits(cleaned_text)
cleaned_text = cleaned_text.split(' ')
cleaned_text = [x.lower() for x in cleaned_text]
cleaned_text = set(cleaned_text)
cleaned_text = sorted(cleaned_text)

# Select output file write mode - append or overwrite
write_mode = 'a' if file_exists else 'w'

# Open file in selected mode
f = open(args.ofile, write_mode)

# Convert words list to the default or user selected format
# csv (default) or txt (with one word per line)
out = addons.form_output(args.format, cleaned_text)

# Write to file and close it
f.write(out)
f.close()

# TODO: add try - except to all file opening commands
# TODO: calculate size of all processed files and add it to total number
# TODO: all text to set and for each unique word count number of occurencies
# TODO: count number of words and show top 30? 50? 100? most frequent ones
