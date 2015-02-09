import re
import const
import dpn_rest_settings
import hashlib
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

def username(namespace):
    """
    Returns the local user name (ssh account) for the specified namespace.
    """
    return "dpn.{0}".format(namepsace)

def xfer_dir(namespace):
    """
    Returns the name of the "outbound" directory for the specified
    partner. E.g. "tdr" => /home/dpn.tdr/outbound
    """
    user = username(namespace)
    return "/home/{0}/outbound".format(user)

def rsync_link(namespace, filename):
    """
    Returns the rsync url for the specified namespace to copy the
    specified file.
    """
    return "{0}@{1}:{2}{3}".format(
        user(namespace), dpn_rest_settings.MY_SERVER,
        dpn_rest_settings.PARTNER_OUTBOUND_DIR, filename)

def digest(abs_path, algorithm):
    """
    Returns the sha256 or md5 hex hash of a file.

    :param abs_path: Absolute path to file.
    :param algorithm: Either 'md5' or 'sha256'

    :returns str: Hex digest of the file.
    """
    size = 65536
    if algorithm == 'md5':
        checksum = hashlib.md5()
    elif algorithm == 'sha256':
        checksum = hashlib.sha256()
    else:
        raise ValueError("algorithm must be either md5 or sha256")
    with open(abs_path, 'rb') as f:
        buf = f.read(size)
        while len(buf) > 0:
            checksum.update(buf)
            buf = f.read(size)
    return checksum.hexdigest()
