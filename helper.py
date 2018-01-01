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

    # split by words
    text = text.split()

    return text


def remove_punctuation_side(text, side='both'):
    """Remove punctuation from selected side of a word or both"""

    # split text by words
    text = text.split()

    if side == 'beg':
        # remove punctuation in the beginning of words
        text = [word.lstrip(string.punctuation) for word in text]

    if side == 'end':
        # remove punctuation in the end of words
        text = [word.rstrip(string.punctuation) for word in text]

    if side == 'both':
        # remove punctuation in the beginning and end of words
        text = [word.strip(string.punctuation) for word in text]

    text = ''.join(text)

    return text


def remove_numbers_all(text):
    """Remove all punctuation from anywhere in the text"""

    table = str.maketrans('', '', string.digits)
    text = text.translate(table)

    return text


def clean(text):
    """Clean text from elements"""

    # split by words
    text = text.split()

    # remove single letters
    text = re.sub(r'\b[a-z]\b', '', text)

    # convert to lowercase
    text = text.lower()

    # split by words
    text = text.split()

    return text
