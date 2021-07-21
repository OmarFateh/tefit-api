import re
import math

from django.utils.html import strip_tags
from django.utils.timesince import timesince


def count_words(html_string):
    """
    Take html string, strip html tags and count its words. 
    """
    word_string = strip_tags(html_string)
    matching_string = re.findall(r'\w+', word_string)
    return len(matching_string)


def get_read_time(html_string):
    """
    Take html string, get its words count, and return number of mins to read it, assuming 200 word per min.
    """
    count = count_words(html_string)
    return int(math.ceil(count/200.0))


def datetime_to_string(datetime):
    """
    Take a datetime object and return a nicely formatted string, eg: Aug 06, 2020 at 07:21 PM. 
    """
    return datetime.strftime("%b %d, %Y at %I:%M %p")


def rounded_timesince(datetime):
    """
    Take a datetime object and return the time between d and now rounded to lowest integer 
    as a nicely formatted string, eg: 7 hours, 16 minutes will be rounded to be 7 hours.
    """
    return timesince(datetime).split(",")[0]
