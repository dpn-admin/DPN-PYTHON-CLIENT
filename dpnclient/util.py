import re
from dpnclient import const
import hashlib
from datetime import datetime

# Regex for something that looks like a UUID.
RE_UUID = re.compile("^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-?[a-f0-9]{12}\Z", re.IGNORECASE)
RE_TIMESTAMP = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.*\d*Z\Z')

def now_str():
    """
    Returns datetime.now in the form of a string. Useful for creating
    JSON dates.
    """
    return datetime.utcnow().isoformat("T") + "Z"

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
    return "dpn.{0}".format(namespace)

def xfer_dir(namespace):
    """
    Returns the name of the "outbound" directory for the specified
    partner. E.g. "tdr" => /home/dpn.tdr/outbound

    *** TODO: USE SETTINGS INSTEAD! THIS SHOULD NOT BE HARD CODED! ***
    """
    user = username(namespace)
    return "/home/{0}/outbound".format(user)

def rsync_link(namespace, my_server, partner_outbound_dir, filename):
    """
    Returns the rsync url for the specified namespace to copy the
    specified file.

    :param namespace: is the namespace of the node you want to copy
    this file (tdr, srd, chron, etc).

    :param my_server: should be your server's fully-qualified domain
    name or IP address, as set in your dpn_rest_settings.py file.

    :param partner_outbound_dir: should be the name of the directory
    in which you hold files for the partner specified in namespace to
    copy outbound files.

    :param filename: is the name of the file to copy (usually a UUID
    with a .tar extension)

    :returns: A string that looks like this: user@myserver.kom:dir/filename.tar
    """
    if partner_outbound_dir.endswith('/') == False:
        partner_outbound_dir += '/'
    return "{0}@{1}:{2}{3}".format(
        username(namespace), my_server, partner_outbound_dir, filename)

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
