#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to clean text from all or user selected things.

- Called without any parameters it will show help
- Called with file input name only, it will show file stats, i.e. file size,
  number of words, and clean from everything and save lower case words list
  in csv format.
- Rest is according to the parameters

1. Open file
2. Get / show / save file stats
3. User selected options for cleaning: either by args / options or via GUI
4. Process text
5. Save output in user selected format: plain text, csv, ?
"""

# import required modules
import os
import sys
import argparse
import chardet
import helper


# class to define colors for messages, defines colors as escape sequences
class Color:
    """Class defines colors for messages"""

    def __init__(self):
        self.OKGR = '\033[92m'
        self.FAIL = '\033[93m'
        self.WARN = '\033[33m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'


# create message colors instance
color = Color()


# function to check if file exists
def check_if_exists(file_name):
    """Check if output file name already exists and then propose to append to it
    or overwrite it."""
    # global variable to know if we shall append or overwrite output file
    global output_file_overwrite

    # check if file already exists and if yes, ask what user wants to do with it
    # - append or overwrite
    if os.path.exists(file_name):
        answer = input(color.WARN + "\nWarning: " + color.ENDC +
                       "File '" + file_name + "' already exists."
                       "\n(" + color.BOLD + "A" + color.ENDC + ")ppend (default)"
                       " to it or (" + color.BOLD + "O" + color.ENDC + ")verwrite it? ")

        # if user wants to overwrite file, give notice and set global variable to True
        if answer in ['o', 'O', '0']:
            print("File will be overwritten!")
            output_file_overwrite = True

        # if user wants to append file, give notice and set global variable to False
        elif answer in ['a', 'A', '']:
            print("Output file will be appended.")
            output_file_overwrite = False

        # if user enters anything else, give help notice and exit
        else:
            print(color.FAIL + "Please, enter 'A' to append information to the output file or 'O' to overwrite it."
                  + color.ENDC)
            sys.exit(0)

    # if file does not exist then set global variable to True since new file will be created
    else:
        output_file_overwrite = True

    # return file name for further processing
    return file_name


# description of what the script does
description = """
Script shows this help message and exits if called without any arguments
or with optional '-h', '--help'. Given one parameter, the script assumes
it is a SOURCE and attempts to read it for further processing.

Script cleans SOURCE from all (default) or only user selected elements and
saves the result into a file. By default it saves result as comma-separated
list of words in lower case.

These are elements removed from a source by default:
- punctuation
- single letters
- extra spaces
- stop words
- numbers

Some extra work done by script:
- spelling correction, including common abbreviations
- non-unicode characters are converted to unicode analogs

If output file name was not specified, the result is saved to .csv file
named as SOURCE with appended '_cleaned' word. For instance, if you called
'tp.py text.txt' then the result will be saved to 'text_cleaned.csv' file.
"""

# create arguments parser
parser = argparse.ArgumentParser(
    prog='tp.py',
    add_help=False,
    usage='%(prog)s source [-o output] [-f format]',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description,
    epilog="Text Processor. Ver 0.1 ©2017 Denis Rasulev. All Rights Reserved.")

# add arguments
parser.add_argument('ifile',
                    metavar='SOURCE',  # type=argparse.FileType('r'),
                    help="source to be processed")
parser.add_argument('-o', '--ofile',
                    metavar='OUTPUT', type=check_if_exists,
                    help="specifies output file name")
parser.add_argument('-f', '--format',
                    metavar='FORMAT',
                    default='csv',
                    help="specifies output file format: csv or txt")


# if script called without any arguments, print short usage note and exit
if len(sys.argv) == 1:
    print("usage: tp.py source [-o output] [-f format]")
    print("help : tp.py -h, --help")
    sys.exit(0)

# if script called with any argument requesting help, print help and exit
if sys.argv[1] in ['?', '/?', '-h', '--help']:
    parser.print_help()
    sys.exit(0)


# if any other arguments were provided, parse them
args = parser.parse_args()

# TODO: processor for HTTP URLs
# check if user provided URL as a SOURCE
if args.ifile.startswith('http'):

    # import requests
    # r = requests.get(args.ifile)
    # print(r.status_code)
    # print(r.headers['content-type'])
    # print(r.encoding)
    # print(r.text)

    print("URLs will be accepted and processed in the future versions.")
    sys.exit(0)
else:
    input_file = open(args.ifile, 'rb').read()
    f_encoding = chardet.detect(input_file)['encoding']


if args.ofile is None:
    args.ofile = os.path.splitext(args.ifile)[0] + "_cleaned" + os.path.splitext(args.ifile)[1]
    check_if_exists(args.ofile)


# print args
print('\n')
print("Input file path     : {}".format(os.path.abspath(args.ifile)))
print("Input file size     : {}".format(helper.sizeof_fmt(os.path.getsize(args.ifile))))
print("Input file encoding : {}".format(f_encoding))
print("Output file path    : {}".format(os.path.abspath(args.ofile)))
print("Output file format  : {}".format(args.format))
print("Overwrite flag      : {}".format(output_file_overwrite))
print('\n')

# main part goes here - output list of words only
f = open(args.ifile, 'r')
source_text = f.read()

cleaned_text = helper.remove_punctuation_all(source_text)

# if we only need unique words
if False:
    cleaned_text = set(cleaned_text)


# save text to file
if output_file_overwrite:
    write_mode = 'w'  # append if already exists
else:
    write_mode = 'a'  # make a new file if not


# open file in required mode - append or oveerwrite
f = open(args.ofile, write_mode)


def form_output(ext):
    """Convert processed word list to user selected file format - csv (default) or txt (one word per line)."""
    return {
        'csv': ', '.join(cleaned_text),
        'txt': '\n'.join(cleaned_text)
    }.get(ext, ', '.join(cleaned_text))


# convert words list to user selected format - csv (default) or txt (one word per line)
out = form_output(args.format)


# write to file and close
f.write(out)
f.close()

# TODO: calculate size of all processed files - find file size and add it to saved number
