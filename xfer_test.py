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
from dpnclient import client, util
import dpn_rest_settings
import hashlib
import os
import subprocess

class XferTest:

    def __init__(self, config):
        self.client = client.Client(dpn_rest_settings, dpn_rest_settings.TEST)

    def replicate_files(self, namespace):
        """
        Replicate bags from the specified namespace.
        """
        requests = self.client.get_transfer_requests(namespace)
        for request in requests:
            link = request['link']
            replication_id = request['replication_id']
            # download the file via rsync
            print("Downloading {0}".format(link))
            local_path = self.copy_file(link)
            # calculate the checksum
            checksum = util.digest(local_path, "sha256")
            # send the checksum as receipt
            print("Returning checksum receipt {0}".format(checksum))
            self.client.set_transfer_fixity(namespace, replication_id, checksum)

    def copy_file(self, location):
        filename = os.path.basename(location.split(":")[1])
        dst = os.path.join(dpn_rest_settings.INBOUND_DIR, filename)
        command = ["rsync", "-Lav", "--compress",
                   "--compress-level=0", "--quiet", location, dst]
        #print(" ".join(command))
        try:
            with subprocess.Popen(command, stdout=subprocess.PIPE) as proc:
                print(str(proc.communicate()[0]))
            return dst

        except Exception as err:
            print("ERROR Transfer failed: {0}".format(err))
            raise err


if __name__ == "__main__":
    xfer = XferTest(dpn_rest_settings.TEST)
    xfer.replicate_files("test")
