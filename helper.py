import re
import string


# function to get human readable size of file
# https://stackoverflow.com/a/1094933/4440387
def sizeof_fmt(size, suffix='b'):
    """Return size of file in human readable format"""

    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(size) < 1024.0:
            return '{:3.2f} {}{}'.format(size, unit, suffix)
        size /= 1024.0
    return '{:0.2f} {}{}'.format(size, 'Y', suffix)


def remove_punctuation_all(text):
    """Remove all punctuation from anywhere in the text"""

    table = str.maketrans('', '', string.punctuation)
    text = text.translate(table)

    return text


def remove_numbers_all(text):
    """Remove all punctuation from anywhere in the text"""

    table = str.maketrans('', '', string.digits)
    text = text.translate(table)

    return text
