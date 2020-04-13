# Additions and supporting functions

# Import required modules
import os
import sys
from subprocess import check_output

from config import Config


# Give human names to text coloring escape sequences for output messages
class Color:
    """Give human names to text coloring escape sequences"""

    def __init__(self):
        self.OKGR = '\033[92m'  # ok      (green)
        self.FAIL = '\033[31m'  # failure (red)
        self.WARN = '\033[33m'  # warning (yellow)
        self.DFLT = '\033[0m'  # default (normal)
        self.BOLD = '\033[1m'  # bold    (emphasize)


clr = Color()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def check_if_file_exists(file_name):
    """Check if output file name already exists and then propose to append to it
    or overwrite it."""

    # Check if file already exists and if yes, ask what to do with it -
    # append or overwrite
    if os.path.exists(file_name):
        decision = input(
            clr.WARN + "\nWarning: " + clr.DFLT +
            "File '" + file_name + "' already exists.\n" "(" + clr.BOLD +
            "A" + clr.DFLT + ")ppend (" "default)"" to it or (" + clr.BOLD +
            "O" + clr.DFLT + ")verwrite it? ")

        # If user wants to overwrite file, notify and return True
        if decision in ['a', 'A', '']:
            print(clr.WARN + "Output file will be appended." + clr.DFLT)
            return True

        # If user wants to append file, notify and return False
        elif decision in ['o', 'O', '0']:
            print(clr.FAIL + "File will be overwritten!" + clr.DFLT)
            return False

        # If user enters anything else, give notice and exit
        else:
            print("Incorrect input, try again.")
            sys.exit(0)

    # If file does not exist, return False
    else:
        return False


def form_output(extension, text):
    """Convert processed word list to user selected file format - csv (default)
    or txt (one word per line)."""
    return {
        'csv': ', '.join(text),
        'txt': '\n'.join(text)
    }.get(extension, ', '.join(text))


# Function to get human readable size of file
# https://stackoverflow.com/a/1094933/4440387
def sizeof_fmt(size, suffix='bytes'):
    """Return size of file in human readable format"""

    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(size) < 1024.0:
            return '{:3.2f} {}{}'.format(size, unit, suffix)
        size /= 1024.0
    return '{:0.2f} {}{}'.format(size, 'Y', suffix)


def count_char(text, char):
    """Count how many times char is in text"""
    count = 0
    for c in text:
        if c == char:
            count += 1
    return count


def count_lines(filename):
    return int(check_output(["wc", "-l", filename]).split()[0])


def count_words(filename):
    return int(check_output(["wc", "-w", filename]).split()[0])

# TODO: counting functions?
# for char in "abcdefghijklmnopqrstuvwxyz":
#   perc = 100 * count_char(text, char) / len(text)
#   print("{0} - {1}%".format(char, round(perc, 2)))
