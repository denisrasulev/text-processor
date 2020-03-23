################################################################################
#                                                                              #
#           Script to clean text from all or user selected things              #
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

# import required modules
import os
import sys
import argparse
import helpers
from subprocess import check_output


# give human names to text coloring escape sequences for output messages
class Color:
    """Give human names to text coloring escape sequences"""

    def __init__(self):
        self.OKGR = '\033[92m'  # ok (green)
        self.FAIL = '\033[31m'  # failure (red)
        self.WARN = '\033[33m'  # warning (yellow)
        self.ENDC = '\033[0m'   # end coloring (return to normal color)
        self.BOLD = '\033[1m'   # bold


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
        decision = input(color.WARN + "\nWarning: " + color.ENDC +
                         "File '" + file_name + "' already exists.\n"
                         "(" + color.BOLD + "A" + color.ENDC + ")ppend (default)"
                         " to it or (" + color.BOLD + "O" + color.ENDC + ")verwrite it? ")

        # if user wants to overwrite file, notify and set global variable to True
        if decision in ['o', 'O', '0']:
            print(color.FAIL + "File will be overwritten!" + color.ENDC)
            output_file_overwrite = True

        # if user wants to append file, notify and set global variable to False
        elif decision in ['a', 'A', '']:
            print(color.WARN + "Output file will be appended." + color.ENDC)
            output_file_overwrite = False

        # if user enters anything else, give help notice and exit
        else:
            print("Incorrect input, script stopped. Run again.")
            sys.exit(0)

    # if file does not exist then set global variable to True since new file will be created
    else:
        output_file_overwrite = True

    # return file name for further processing
    return file_name


version = "Text Processor. Ver 0.1 (c) 2017-2019 Denis Rasulev. All Rights " \
          "Reserved."

# description of what the script does
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

# create arguments parser
parser = argparse.ArgumentParser(
    prog='tp.py',
    add_help=False,
    usage='%(prog)s source [-o output] [-f format]',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description,
    epilog=epilog)

# add arguments
parser.add_argument('ifile',
                    metavar='SOURCE',
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
    print(version)
    print("")
    print("usage: tp.py source [-o output] [-f format]")
    print(" source   required, file name")
    print(" output   optional, file name")
    print(" format   optional, csv or txt")
    print("")
    print("help:     tp.py -h, --help")
    sys.exit(0)

# if script called with any argument requesting help, print help and exit
if sys.argv[1] in ['?', '/?', '-h', '--help']:
    parser.print_help()
    sys.exit(0)

if sys.argv[1] in ['-v', '--version']:
    print(version)
    sys.exit(0)

# if any other arguments were provided, parse them
args = parser.parse_args()

# check if user provided URL as a SOURCE
if args.ifile.startswith('http') or args.ifile.startswith('https'):

    # TODO: processor for HTTP URLs
    # import requests
    # r = requests.get(args.ifile)
    # print(r.status_code)
    # print(r.headers['content-type'])
    # print(r.encoding)
    # print(r.text)

    print("URLs will be accepted and processed in future versions.")
    sys.exit(0)
else:
    input_file = open(args.ifile, 'r').read()

# default output file extension is .csv. If user specified .txt, then use it
extension = ".csv"
if args.format == 'txt':
    extension = ".txt"

# if output file format is ommited then construct new output file name
if args.ofile is None:
    args.ofile = os.path.splitext(args.ifile)[0] + "_cleaned" + extension
    check_if_exists(args.ofile)


def wc_line(filename):
    return int(check_output(["wc", "-l", filename]).split()[0])


def wc_word(filename):
    return int(check_output(["wc", "-w", filename]).split()[0])


# print args and basic info
print("Input file")
print("- path   : {}".format(os.path.abspath(args.ifile)))
print("- size   : {}".format(helpers.sizeof_fmt(os.path.getsize(args.ifile))))
print("- lines  : {}".format(wc_line(args.ifile)))
print("- words  : {}".format(wc_word(args.ifile)))
print("Output file")
print("- path   : {}".format(os.path.abspath(args.ofile)))
print("- format : {}".format(args.format))
print("Overwrite")
print("- status : {}".format(output_file_overwrite))

# and confirm user action
answer = input(color.WARN + "\nProceed? (y/n): " + color.ENDC)

# if user wants to overwrite file, notify and set global variable to True
if answer not in ['y', 'Y']:
    print(color.FAIL + "Operation aborted." + color.ENDC)
    sys.exit(0)

# main part
f = open(args.ifile, 'r')
source_text = f.read()

# text processing functions
cleaned_text = helpers.remove_punctuation(source_text)
cleaned_text = helpers.remove_digits(cleaned_text)
cleaned_text = helpers.remove_chars(cleaned_text)
cleaned_text = cleaned_text.split()
cleaned_text = [x.lower() for x in cleaned_text]
cleaned_text = set(cleaned_text)
cleaned_text = sorted(cleaned_text)

# save text to file
if output_file_overwrite:
    write_mode = 'w'  # append if already exists
else:
    write_mode = 'a'  # make a new file if not

# open file in required mode - append or oveerwrite
f = open(args.ofile, write_mode)


def form_output(ext):
    """Convert processed word list to user selected file format - csv (default)
    or txt (one word per line)."""
    return {
        'csv': ', '.join(cleaned_text),
        'txt': '\n'.join(cleaned_text)
    }.get(ext, ', '.join(cleaned_text))


# convert words list to user selected format - csv (default) or txt (one word
# per line)
out = form_output(args.format)

# write to file and close
f.write(out)
f.close()

# TODO: calculate size of all processed files - find file size and add it to saved number
# TODO: all text to set and for each unique character count number of occurencies
# TODO: count number of words and top 30? 50? 100? most frequent ones

# for char in "abcdefghijklmnopqrstuvwxyz":
#   perc = 100 * count_char(text, char) / len(text)
#   print("{0} - {1}%".format(char, round(perc, 2)))
