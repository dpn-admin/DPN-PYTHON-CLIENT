import re
import const
from datetime import datetime

# Regex for something that looks like a UUID.
RE_UUID = re.compile("^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-?[a-f0-9]{12}\Z", re.IGNORECASE)

def now_str():
    """
    Returns datetime.now in the form of a string. Useful for creating
    JSON dates.
    """
    return str(datetime.now())

def looks_like_uuid(string):
    """
    Returns True if string looks like a UUID.
    """
    return RE_UUID.match(string) != None

def status_valid(status):
    """
    Returns True if status is a valid DPN status option.
    """
    return status in const.STATUSES

def protocol_valid(protocol):
    """
    Returns True if protocol is a valid DPN protocol option.
    """
    return protocol in const.PROTOCOLS

def bag_type_valid(bag_type):
    """
    Returns True if bag_type is a valid DPN bag type.
    """
    return bag_type in const.BAG_TYPES

def fixity_type_valid(fixity_type):
    """
    Returns True if fixity_type is a valid DPN fixity type.
    """
    return fixity_type in const.FIXITY_TYPES
