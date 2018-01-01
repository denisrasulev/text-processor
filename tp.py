#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Project to create text cleaning script to clean text from user selected things.

- Called without any parameters it will show help
- Called with file input name only, it will show file stats, i.e. file size, number of words,
  and clean from everything and save lowercase words list in csv format.
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
import helper
import argparse
import chardet


# class to define colors for outputs, defines colors as escape sequences
class Color:
    def __init__(self):
        self.HEAD = '\033[95m'
        self.OKBL = '\033[94m'
        self.OKGR = '\033[92m'
        self.FAIL = '\033[93m'
        self.WARN = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDR = '\033[4m'


# create instance
clr = Color()


# function to check if file exists
def check_if_exists(file_name):
    """Check if output file already exists and propose to append to it or overwrite it."""
    # global variable to know if we shall append or overwrite output file
    global output_file_overwrite

    # check if file already exists and if yes, ask what user wants to do with it - append or overwrite
    if os.path.exists(file_name):
        answer = input("File '" + file_name + "' already exists. (A)ppend (default) to it or (O)verwrite it? ")

        # if user wants to overwrite file, give notice and set global variable to True
        if answer in ['o', 'O', '0']:
            print(clr.WARN + "ATTENTION: File will be overwritten!" + clr.ENDC)
            output_file_overwrite = True

        # if user wants to append file, give notice and set global variable to False
        elif answer in ['a', 'A', '']:
            print("Output file will be appended.")
            output_file_overwrite = False

        # if user entered anything else, give notice and exit
        else:
            print(clr.FAIL + "Please, enter 'A' to append information to the output file or 'O' to overwrite it."
                  + clr.ENDC)
            sys.exit(0)

    # if file does not exist then set global variable to True since new file will be created
    else:
        output_file_overwrite = True

    # return file name for further processing
    return file_name


# create args parser and add possible arguments
# TODO: print help if no args were supplied
# TODO: check if we can format help: -i IFILE --ifile IFILE -> -i, --ifile IFILE
parser = argparse.ArgumentParser(
    prog='tp',
    description="Script to clean source text from all and/or user selected elements.",
    epilog="tp (text processor) ver 0.1. © 2017 Denis Rasulev. All Rights Reserved.")
parser.add_argument('-i', '--ifile', type=argparse.FileType('r'), help="source text file")
parser.add_argument('-o', '--ofile', type=check_if_exists, help="output text file")
parser.add_argument('-f', '--format', help="output file format: csv or txt")
# TODO: parse format setting and validate it


# parse arguments
args = parser.parse_args()


# detect input file encoding
input_file = open(args.ifile.name, 'rb').read()
f_encoding = chardet.detect(input_file)['encoding']


# print args
print('\n')
print("Input file path     : {}".format(os.path.abspath(args.ifile.name)))
print("Input file size     : {}".format(helper.sizeof_fmt(os.path.getsize(args.ifile.name))))
print("Input file encoding : {}".format(f_encoding))
print("Output file path    : {}".format(os.path.abspath(args.ofile)))
print("Output file format  : {}".format(args.format))
print("Overwrite flag      : {}".format(output_file_overwrite))
print('\n')

# main part goes here - output list of words only
source_text = args.ifile.read()
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
