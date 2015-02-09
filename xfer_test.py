# xfer_test.py
#
# A quick and dirty script to implement DPN replicating node
# functions. This is not a production script. It merely
# implements the following basic transfer features for an initial
# test run:
#
# 1. Query a remote node for pending transfer requests.
# 2. Use rsync to copy files in the transfer requests.
# 3. Calculate the sha-265 checksums of the files.
# 4. Send the checksums back to the remote node.
#
# Pre-reqs:
#
# 1. This must run on a box that has access to the remote DPN servers,
#    such as devops.aptrust.org.
# 2. The dpn_rest_settings.py file must be configured correctly. The
#    template for that file is settings_template.py. The actual
#    settings file is not in GitHub.
#
# Usage:
#
# python xfer_test.py [remote_node]
#
# Param remote_node should be one of: tdr, sdr, chron or hathi
#
# ----------------------------------------------------------------------
import client
import dpn_rest_settings
import hashlib
import os
import util

class XferTest:

    def __init__(self, config):
        self.client = client.Client(
            config['url'], config['key'], config['rsync_host'],
            config['max_xfer_size'])
        self.client.verify_ssl = False  # TDR does not have a legit cert

    def replicate_files(self, namespace):
        """
        Replicate bags from the specified namespace.
        """
        requests = self.client.get_transfer_requests(namespace)
        for request in requests:
            print(request['link'])
            # mark the transfer as accepted
            # rsync the file
            # calculate the checksum
            # send the checksum as receipt


if __name__ == "__main__":
    xfer = XferTest(dpn_rest_settings.DEV)
    xfer.replicate_files("tdr")
