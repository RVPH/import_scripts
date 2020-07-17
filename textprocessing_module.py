# Text processing functions for
# Russkiy Vrach Publishing House article database

import re

# Individual functions to process text


def remove_linebreaks(value: str) -> str:
    """Remove linebreaks (\n) """
    regexp = re.compile(r'\n')
    return regexp.sub(' ', value)


def remove_wordwraps(value: str) -> str:
    """Remove wordwraps (-\n) """
    regexp = re.compile(r'-\n')
    return regexp.sub('', value)


def remove_extra_spaces(value: str) -> str:
    """Remove leading and trailing space characters and replace any 
       multiple whitespace characters to one space character"""
    regexp = re.compile(r'^\s+')
    value = regexp.sub('', value)
    regexp = re.compile(r'\s+$')
    value = regexp.sub('', value)
    regexp = re.compile(r'\s+')
    return regexp.sub(' ', value)


def remove_trailing_dots(value: str) -> str:
    """Remove trailing dot(s)"""
    regexp = re.compile(r'\.+$')
    return regexp.sub('', value)


def replace_semicolon_to_comma(value: str) -> str:
    """Remove semicolons to commas"""
    regexp = re.compile(r';')
    return regexp.sub(',', value)


def arrange_spaces_around_commas(value: str) -> str:
    """Remove unnecessary space before commas and add a single space after"""
    regexp = re.compile(r'\s+,')
    value = regexp.sub(',', value)
    regexp = re.compile(r',\s*')
    return regexp.sub(', ', value)


def remove_phrase_before_colon(value: str) -> str:
    """Remove a phrase before colon at the beginning of the given string"""
    regexp = re.compile(r'^.*:\s*')
    return regexp.sub('', value)


def remove_extra_spaces_in_list(value: str) -> str:
    """Remove spaces in the beginning of a string in a list"""
    regexp = re.compile(r'^[ \t]+', re.M)
    value = regexp.sub('', value, re.M)
    #regexp = re.compile(r'\n\s+', re.M)
    #value = regexp.sub('\n', value, re.M)
    regexp = re.compile(r'¬')
    value = regexp.sub('', value)
    regexp = re.compile(r'')
    value = regexp.sub('-', value)
    regexp = re.compile(r'[ \t][ \t]+', re.M)
    return regexp.sub(' ', value, re.M)

# Stack of functions to check critical values


def id_is_valid(cell: 'Excel cell') -> 'Boolean':
    """Check ID field"""
    if type(cell.value) is str:
        if re.compile(r'........-\d\d\d\d-\d\d-\d\d').fullmatch(cell.value):
            return True
    return False


def volume_is_valid(cell: 'Excel cell') -> 'Boolean':
    """Check Volume field"""
    regexp = re.compile(r'^\d{1,2}$')
    if regexp.fullmatch(str(cell.value)):
        return True
    return False


def month_is_valid(cell: 'Excel cell') -> 'Boolean':
    """Check Month field"""
    regexp = re.compile(r'^\d{1,2}$')
    if regexp.fullmatch(str(cell.value)):
        return True
    return False


# Stack of texprocessing functions by Excel columns

def process_title_field(cell: 'Excel cell') -> None:
    """Stack of texprocessing functions for 'Title' field"""
    # Check whether cell has the type of 'String'
    # to ignore emply cells
    if type(cell.value) is str:
        cell.value = remove_wordwraps(cell.value)
        cell.value = remove_linebreaks(cell.value)
        cell.value = remove_extra_spaces(cell.value)
        cell.value = remove_trailing_dots(cell.value)


def process_authors_list_field(cell: 'Excel cell') -> None:
    """Stack of texprocessing functions for 'Authors list' field"""
    if type(cell.value) is str:
        cell.value = remove_wordwraps(cell.value)
        cell.value = remove_linebreaks(cell.value)
        cell.value = remove_extra_spaces(cell.value)
        cell.value = replace_semicolon_to_comma(cell.value)
        cell.value = arrange_spaces_around_commas(cell.value)


def process_authors_field(cell: 'Excel cell') -> None:
    if type(cell.value) is str:
        cell.value = remove_wordwraps(cell.value)
        cell.value = remove_linebreaks(cell.value)
        cell.value = remove_extra_spaces(cell.value)


def process_abstract_field(cell: 'Excel cell') -> None:
    if type(cell.value) is str:
        cell.value = remove_wordwraps(cell.value)
        cell.value = remove_linebreaks(cell.value)
        cell.value = remove_extra_spaces(cell.value)


def process_keywords_field(cell: 'Excel cell') -> None:
    if type(cell.value) is str:
        cell.value = remove_wordwraps(cell.value)
        cell.value = remove_phrase_before_colon(cell.value)
        cell.value = remove_linebreaks(cell.value)
        cell.value = remove_extra_spaces(cell.value)
        cell.value = replace_semicolon_to_comma(cell.value)
        cell.value = arrange_spaces_around_commas(cell.value)
        cell.value = remove_trailing_dots(cell.value)


def process_rubric_field(cell: 'Excel cell') -> None:
    if type(cell.value) is str:
        cell.value = remove_wordwraps(cell.value)
        cell.value = remove_linebreaks(cell.value)
        cell.value = remove_extra_spaces(cell.value)
        cell.value = remove_trailing_dots(cell.value)
        cell.value = cell.value.upper()


def process_references_field(cell: 'Excel cell') -> None:
    if type(cell.value) is str:
        cell.value = remove_extra_spaces_in_list(cell.value)


def process_pages_field(cell: 'Excel cell') -> None:
    if type(cell.value) is str:
        cell.value = remove_extra_spaces(cell.value)
