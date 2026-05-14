import re

REGEX_STATSD_MESSAGE = re.compile(r"(?P<metric>.*)\:(?P<value>.*)\|(?P<mtype>\w+)")
