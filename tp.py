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
import re
import sys
import string
import argparse


# color class to use in outputs
class Color:
    HEAD = '\033[95m'
    OKBL = '\033[94m'
    OKGR = '\033[92m'
    FAIL = '\033[93m'
    WARN = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDR = '\033[4m'


# function to check file existence
def check_if_exists(file_name):
    """Check if output file already exists and propose to append to it or overwrite it."""
    # global variable to know if we shall append or overwrite output file
    global output_file_overwrite

    # check if file already exists and if yes, ask what user wants to do with it - append or overwrite
    if os.path.exists(file_name):
        answer = input("Output file already exists. (A)ppend (default) to it or (O)verwrite it? ")

        # if user wants to overwrite file, give notice and set global variable to True
        if answer in ['o', 'O', '0']:
            print(Color.WARN + "Output file will be overwritten!" + Color.ENDC)
            output_file_overwrite = True

        # if user wants to append file, give notice and set global variable to False
        elif answer in ['a', 'A', '']:
            print("Output file will be appended.")
            output_file_overwrite = False

        # if user entered anything else, give notice and exit
        else:
            print(Color.FAIL + "Please, enter 'A' to append information to the output file or 'O' to overwrite it."
                  + Color.ENDC)
            sys.exit(0)

    # if file does not exist then set global variable to True since new file will be created
    else:
        output_file_overwrite = True

    # return file name for further processing
    return file_name


# create args parser and add possible arguments
# TODO: print help if no args were supplied
# TODO: check if we can format help: -i INPUT --input INPUT -> -i, --input INPUT
parser = argparse.ArgumentParser(
    prog='tp',
    description="Script to clean source text from all and/or user selected elements.",
    epilog="tp (text processor) ver 0.1. © 2017 Denis Rasulev. All Rights Reserved.")
parser.add_argument('-i', '--input', type=argparse.FileType('r'), help="source text file")
parser.add_argument('-o', '--output', type=check_if_exists, help="output text file")
parser.add_argument('-f', '--format', help="output file format: csv or txt")
# TODO: parse format setting and validate it

# parse arguments
args = parser.parse_args()


# function to get human readable size of file
# https://stackoverflow.com/a/1094933/4440387
# TODO: replace old formatting with modern one
def sizeof_fmt(num, suffix='b'):
    for unit in [' ', ' K', ' M', ' G', ' T', ' P', ' E', ' Z']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, ' Y', suffix)


# print args
print('\n')
print("Input: {}".format(os.path.abspath(args.input.name)))
print("Input file size: {}".format(sizeof_fmt(os.path.getsize(args.input.name))))
print("Output: {}".format(args.output))
print("Format: {}".format(args.format))
print("Overwrite: {}".format(output_file_overwrite))
print('\n')

# main part goes here - output list of words only
source_text = args.input.read()

# detect and print out text encoding
# TODO: encoding


def clean(text):
    """Clean text from elements"""

    # remove all punctuation
    # TODO: How does it work?
    table = str.maketrans({key: ' ' for key in string.punctuation})
    text = text.translate(table)

    # remove punctuation in the beginning and end of words
    # code here

    # convert to lowercase
    text = text.lower()

    # split by words
    text = text.split()

    return text


cleaned_text = clean(source_text)
print(cleaned_text)

# save text to file

f = open(args.output, 'w')


def form_output(ext):
    """Convert processed word list to user selected file format - csv or txt.
       Default is csv."""
    return {
        'csv': ', '.join(cleaned_text),
        'txt': '\n'.join(cleaned_text)
    }.get(ext, ', '.join(cleaned_text))


out = form_output(args.format)

# save
f.write(out)
f.close()

# unused code snippets:
# text = re.sub('\s+', ' ', text)
# text = text.strip()















