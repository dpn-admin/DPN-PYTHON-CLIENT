# Fill out the following settings and save as dpn_rest_settings.py.
# Don't check dpn_rest_settings.py into source control, since this
# is a public repo and the settings file will have your API keys.
#
# Enter the URL (with port) and API key for *your own* DPN node.
# The API key should be the key for a user on your own node who
# has admin access.
#

# Set MY_NODE to the namespace of your node ('tdr', 'sdr', 'aptrust', etc.)
MY_NODE    = 'aptrust'

# This should be the IP address or fully-qualified domain name of your
# DPN node. This is used in constructing links to bags you want partners
# to replicate.
MY_SERVER  = 'devops.aptrust.org'

# Where do we keep DPN bags?
# OUTBOUND_DIR - full path to dir containing DPN bags for other nodes to copy.
# INBOUND_DIR  - full path to dir where we will store bags that we are
#                replicating from other nodes. We need to run checksums on
#                these and then send them off to long-term storage.
OUTBOUND_DIR = '/path/to/outbound'
INBOUND_DIR  = '/path/to/inbound'

# PARTNER_OUTBOUND_DIR is the name of the directory under the partner's
# home directory where they should look for files we want them to copy.
# For example, partner xyz will have an account on MY_SERVER under
# /home/dpn.xyz. We'll put files in /home/dpn.xyz/outbound for them to
# copy.
PARTNER_OUTBOUND_DIR = "outbound"


# Configurations for OUR OWN node.
# url is the url for your own node
# token is the API key/token for admin user at your own node.
# rsync_host is the hostname from which other nodes will transfer your content
# max_xfer_size is the max size of files you are willing to transfer in
TEST       = { 'url': '', 'token': '', 'rsync_host': '', 'max_xfer_size': 0 }
DEV        = { 'url': '', 'token': '', 'rsync_host': '', 'max_xfer_size': 0 }
PRODUCTION = { 'url': '', 'token': '', 'rsync_host': '', 'max_xfer_size': 0 }

available = [TEST, DEV, PRODUCTION]

# API keys for OTHER nodes that we want to query.
# Key is node namespace. Value is API key to connect to that node.
KEYS = {
    'aptrust': 'api key goes here',
    'hathi':   'api key goes here',
    'chron':   'api key goes here',
    'sdr':     'api key goes here',
    'tdr':     'api key goes here',
    }

def show_available():
    for config in available:
        if config['url'] != '' and config['key'] != '':
            max_xfer_size = config['max_xfer_size']
            if max_xfer_size == 0:
                max_xfer_size = "no size limit"
            print("{0} ... {1}".format(config['url'], max_xfer_size))
