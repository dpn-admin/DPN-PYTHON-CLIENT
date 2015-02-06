# Fill out the following settings and save as dpn_rest_settings.py.
# Don't check dpn_rest_settings.py into source control, since this
# is a public repo and the settings file will have your API keys.
#
# Enter the URL (with port) and API key for *your own* DPN node.
# The API key should be the key for a user on your own node who
# has admin access.
#

TEST       = { 'url': '', 'key': '', 'max_xfer_size': 0 }
DEV        = { 'url': '', 'key': '', 'max_xfer_size': 0 }
PRODUCTION = { 'url': '', 'key': '', 'max_xfer_size': 0 }

available = [TEST, DEV, PRODUCTION]

def show_available():
    for config in available:
        if config['url'] != '' and config['key'] != '':
            max_xfer_size = config['max_xfer_size']
            if max_xfer_size == 0:
                max_xfer_size = "no size limit"
            print("{0} ... {1}".format(config['url'], max_xfer_size))
