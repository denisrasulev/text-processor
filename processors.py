# Text processing functions

# Import required modules
import re


def remove_html_tags(text):
    """Remove HTML tags from the text"""

    tags = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    text = re.sub(tags, ' ', text)

    return text


def remove_punctuation(text):
    """Remove all punctuation from anywhere in the text"""

    text = re.sub(r'[^\w\s]', ' ', text)

    return text


def remove_digits(text):
    """Remove all digits from anywhere in the text"""

    text = re.sub(r'\d+', ' ', text)

    return text


def remove_single_chars(text):
    """Remove all single chars from the text"""

    text = re.sub(r'\b\w\b', ' ', text)

    return text


def remove_extra_spaces(text):
    """Remove extra spaces from the text"""

    # Replace multiple spaces with single ones
    text = re.sub(r"\s+", ' ', text)
    # Remove leading and trailing spaces
    text = re.sub(r"^\s+|\s+$", "", text)

    return text
