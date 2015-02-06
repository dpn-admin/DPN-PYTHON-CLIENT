import json
import util
import dpn_rest_settings as settings
from base_client import BaseClient
from requests.exceptions import RequestException
from datetime import datetime

class Client(BaseClient):
    """
    This is the higher-level DPN REST client that performs meaningful
    repository operations. It's based on the lower-level BaseClient, which
    just does raw REST operations, and it does expose the BaseClient's
    methods.
    """
    def __init__(self, url, token):
        super(Client, self).__init__(url, token)
        self.my_node = None
        self.all_nodes = []
        self.replicate_to = []
        self.replicate_from = []
        self.restore_to = []
        self.restore_from = []
        self._init_nodes()


    def _init_nodes(self):
        """
        Initializes some information about all known nodes, including
        which node is ours, which nodes we can replicate to and from,
        and which nodes we can restore to and from.
        """
        response = self.node_list()
        data = response.json()
        self.all_nodes = data['results']
        for node in self.all_nodes:
            if node['namespace'] == settings.MY_NODE:
                self.my_node = node
            if node['replicate_from']:
                self.replicate_from.append(node)
            if node['replicate_to']:
                self.replicate_to.append(node)
            if node['restore_from']:
                self.restore_from.append(node)
            if node['restore_to']:
                self.restore_to.append(node)
        return True


    def create_registry_entry(self, obj_id, bag_type, bag_size):
        if not util.bag_type_valid(bag_type):
            raise ValueError("bag_type '{0}' is not valid".format(bag_type))
        if not isinstance(bag_size, int):
            raise TypeError("bag_size must be an integer")
        timestamp = util.now_str()
        entry = {
            "first_node": self.my_node['namespace'],
            "brightening_objects": [],
            "rights_objects": [],
            "replicating_nodes": [],
            "dpn_object_id": obj_id,
            "local_id": None,
            "version_number": 1,
            "creation_date": timestamp,
            "last_modified_date": timestamp,
            "bag_size": bag_size,
            "object_type": bag_type,
            "previous_version": None,
            "forward_version": None,
            "first_version": obj_id,
        }
        return self.registry_create(entry)


# ------------------------------------------------------------------
# First node operations
# ------------------------------------------------------------------
# 1. Create registry entry. Do this when you, as first node, have received a new item.

# 2. Create transfer request. After creating a registry entry, create requests for
#    two other nodes to copy the new item.




# ------------------------------------------------------------------
# Replicating node operations
# ------------------------------------------------------------------
# 1. Query other nodes for transfer requests.

# 2. Accept transfer requests. This tells the other node you will be storing the item.

# 3. Send transfer fixity. Once you have received the item into your storage area,
#    calculate the sha256 digest and send it back to the originating node to indicate
#    your copy is complete.
