import json
from dpnclient import const
from dpnclient import util
from dpnclient.base_client import BaseClient
from requests.exceptions import RequestException
from datetime import datetime

class Client(BaseClient):
    """
    This is the higher-level DPN REST client that performs meaningful
    repository operations. It's based on the lower-level BaseClient, which
    just does raw REST operations, and it does expose the BaseClient's
    methods.

    :param settings: An instance of dpn_rest_settings, which is just a
    python config file. See settings_template.py for info about what should
    be in the settings file.

    :param active_config: A dictionary from dpn_rest_settings.py containing
    information about how to connect to a DPN rest server. The
    dpn_rest_settings.py file may have dictionaries called TEST, DEV, and
    PRODUCTION, each with keys 'url', 'token', 'rsync_host' and 'max_xfer_size'.
    """
    def __init__(self, settings, active_config):
        super(Client, self).__init__(active_config['url'], active_config['token'])
        self.rsync_host = active_config['rsync_host']
        self.max_xfer_size = active_config['max_xfer_size']
        self.settings = settings
        self.my_node = None
        self.all_nodes = []
        self.replicate_to = []
        self.replicate_from = []
        self.restore_to = []
        self.restore_from = []
        self.nodes_by_namespace = {}
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
            if node['namespace'] == self.settings.MY_NODE:
                self.my_node = node
            if node['replicate_from']:
                self.replicate_from.append(node)
            if node['replicate_to']:
                self.replicate_to.append(node)
            if node['restore_from']:
                self.restore_from.append(node)
            if node['restore_to']:
                self.restore_to.append(node)
            self.nodes_by_namespace[node['namespace']] = node
        return True

    def create_registry_entry(self, obj_id, bag_size, bag_type):
        """
        Creates a new registry entry on your own node. You must be admin
        to do this, and you cannot create registry entries on other nodes.

        :param obj_id: The ID of the DPN bag you want the other node to copy.
        :param bag_size: The size, in bytes, of the bag.
        :param bag_type: The type of bag/registry entry. See const.BAG_TYPES.

        :returns: The newly created registry entry as a dict.

        :raises RequestException: Check the response property for details.
        """
        if not util.looks_like_uuid(obj_id):
            raise ValueError("obj_id '{0}' should be a uuid".format(obj_id))
        if not isinstance(bag_size, int):
            raise TypeError("bag_size must be an integer")
        if not util.bag_type_valid(bag_type):
            raise ValueError("bag_type '{0}' is not valid".format(bag_type))
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
        response = self.registry_create(entry)
        if response is not None:
            return response.json()
        return None

    def create_transfer_request(self, obj_id, bag_size, username, fixity):
        """
        Creates a transfer request on your own node asking some other node
        to copy your file. You must be admin on your node to create a transfer
        request, and you cannot create transfer requests on other nodes.

        :param obj_id: The ID of the DPN bag you want the other node to copy.
        :param bag_size: The size, in bytes, of the bag.
        :param username: The SSH username the replicating node uses to connect to your node.
        :param fixity: The SHA-256 digest of the bag to be copied.

        :returns: The newly created transfer request as a dict.

        :raises RequestException: Check the response property for details.
        """
        if not util.looks_like_uuid(obj_id):
            raise ValueError("obj_id '{0}' should be a uuid".format(obj_id))
        if not isinstance(bag_size, int):
            raise TypeError("bag_size must be an integer")
        if not isinstance(username, str) or username.strip() == "":
            raise ValueError("username must be a non-empty string")
        if not isinstance(fixity, str) or fixity.strip() == "":
            raise ValueError("fixity must be a non-empty string")
        link = "{0}@{1}:{2}".format(username, self.rsync_host, obj_id)
        xfer_req = {
            "dpn_object_id": obj_id,
            "link": link,
            "node": self.my_node['namespace'],
            "size": bag_size,
            "exp_fixity": fixity,
        }
        response = self.transfer_create(xfer_req)
        if response is not None:
            return response.json()
        return None

    def get_transfer_requests(self, remote_node_namespace):
        """
        Retrieves transfer requests from another node (specified by namespace)
        that your node is supposed to fulfill.

        :param remote_node_namespace: The namespace of the node to connect to.

        :returns: A list of transfer requests, each of which is a dict.

        :raises RequestException: Check the response property for details.
        """
        other_node = self.nodes_by_namespace[remote_node_namespace]
        url = other_node['api_root']
        api_key = self.settings.KEYS[remote_node_namespace]
        client = BaseClient(url, api_key)
        page_num = 0
        xfer_requests = []

        # Get transfer requests in batches
        while True:
            page_num += 1
            response = client.transfer_list(status='P',
                                            page_size=20,
                                            node=self.settings.MY_NODE,
                                            page=page_num)
            data = response.json()
            xfer_requests.extend(data['results'])
            if len(xfer_requests) >= data['count']:
                break

        return xfer_requests

    def accept_transfer_request(self, remote_node_namespace, event_id):
        """
        Tells a remote node that you are accepting its transfer request.

        :param remote_node_namespace: The namespace of the node to connect to.
        :param event_id: The ID of the transfer request you are accepting.

        :returns: An updated transfer request.

        :raises RequestException: Check the response property for details.
        """
        return self._update_transfer_request(
            remote_node_namespace, event_id, const.STATUS_ACCEPT, None)

    def reject_transfer_request(self, remote_node_namespace, event_id):
        """
        Tells a remote node that you are rejectting its transfer request.

        :param remote_node_namespace: The namespace of the node to connect to.
        :param event_id: The ID of the transfer request you are rejecting.

        :returns: An updated transfer request.

        :raises RequestException: Check the response property for details.
        """
        return self._update_transfer_request(
            remote_node_namespace, event_id, const.STATUS_REJECT, None)

    def set_transfer_fixity(self, remote_node_namespace, event_id, fixity):
        """
        Tells a remote node that you have copied the file in its transfer
        request and that you calculated the specified SHA-256 checksum on
        that file.

        :param remote_node_namespace: The namespace of the node to connect to.
        :param event_id: The ID of the transfer request you completed.
        :param fixity: The SHA-256 checksum of the file you copied.

        :returns: An updated transfer request.

        :raises RequestException: Check the response property for details.
        """
        return self._update_transfer_request(
            remote_node_namespace, event_id, None, fixity)

    def _update_transfer_request(self, remote_node_namespace, event_id, status, fixity):
        other_node = self.nodes_by_namespace[remote_node_namespace]
        url = other_node['api_root']
        api_key = self.settings.KEYS[remote_node_namespace]
        client = BaseClient(url, api_key)
        data = { "event_id": event_id }
        if status is not None:
            data['status'] = status
        if fixity is not None:
            data['receipt'] = fixity
        print(data)
        response = client.transfer_update(data)
        if response is not None:
            return response.json()
        return None
