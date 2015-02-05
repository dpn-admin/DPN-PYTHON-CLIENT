import const
import json
import requests

class Client:

    def __init__(self, url, token):
        while url.endswith('/'):
            url = url[:-1]
        self.url = url
        self.token = token

    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'token {0}'.format(self.token),
        }

# ------------------------------------------------------------------
# Node methods
# ------------------------------------------------------------------
    def node_list(self, **kwargs):
        """
        Returns a list of DPN nodes.

        :param replicate_to: Boolean value.
        :param replicate_from: Boolean value.
        :param page_size: Number of max results per page.

        :returns: requests.Response
        """
        url = "{0}/node/".format(self.url)
        return requests.get(url, headers=self.headers(), data=kwargs)

    def node_get(self, namespace):
        """
        Returns the DPN node with the specified namespace.

        :param namespace: The namespace of the node. ('tdr', 'sdr', etc.)

        :returns: requests.Response
        """
        url = "{0}/node/{1}/".format(self.url, namespace)
        return requests.get(url, headers=self.headers())


# ------------------------------------------------------------------
# Registry methods
# ------------------------------------------------------------------
    def registry_list(self, **kwargs):
        """
        Returns a requests.Response object whose json contains a list of
        registry entries.

        :param before: DPN DateTime string to FILTER results by last_modified_date earlier than this.
        :param after: DPN DateTime String to FILTER result by last_modified_date later than this.
        :param first_node: String to FILTER by node namespace.
        :param object_type: String character to FILTER by object type.
        :param ordering: ORDER return by (accepted values: last_modified_date)
        :param page_size: Number of max results per page.

        :returns: requests.Response
        """
        url = "{0}/registry/".format(self.url)
        return requests.get(url, headers=self.headers(), data=kwargs)

    def registry_get(self, obj_id):
        """
        Returns a requests.Response object whose json contains the single
        registry entry that matches the specified obj_id.

        :param obj_id: A UUID string. The id of the registry entry to return.

        :returns: requests.Response
        """
        url = "{0}/registry/{1}/".format(self.url, obj_id)
        return requests.get(url, headers=self.headers())

    def registry_create(self, obj):
        """
        Creates a registry entry. Only the repository admin can make this call,
        which means you can issue this call only against your own node.

        :param obj: The object to create.

        :returns: requests.Response
        """
        url = "{0}/registry/".format(self.url)
        return requests.post(url, headers=self.headers(), data=json.dumps(obj))

    def registry_update(self, obj):
        """
        Updates a registry entry. Only the repository admin can make this call,
        which means you can issue this call only against your own node.

        :param obj: The object to create.

        :returns: requests.Response
        """
        url = "{0}/registry/{1}/".format(self.url, obj['dpn_object_id'])
        return requests.put(url, headers=self.headers(), data=json.dumps(obj))



# ------------------------------------------------------------------
# Restoration methods
# ------------------------------------------------------------------
    def restore_list(self, **kwargs):
        """
        Returns a paged list of Restore requests.

        *** RESTORE IS NOT YET IMPLEMENTED ***

        :param dpn_object_id: Filter by DPN Object ID
        :param status: Filter by status code.
        :param node: Filter by node namespace.
        :param ordered: Order by comma-separated list: 'created' and/or 'updated'

        :returns: requests.Response
        """
        url = "{0}/restore/".format(self.url)
        return requests.get(url, headers=self.headers(), data=kwargs)

    def restore_get(self, event_id):
        """
        Returns the restore request with the specified event id.

        *** RESTORE IS NOT YET IMPLEMENTED ***

        :param obj_id: The event_id of the restore request.

        :returns: requests.Response
        """
        url = "{0}/restore/{1}/".format(self.url, event_id)
        return requests.get(url, headers=self.headers())

    def restore_create(self, obj):
        """
        Creates a restore request. Only the repository admin can make this call,
        which means you can issue this call only against your own node.

        *** RESTORE IS NOT YET IMPLEMENTED ***

        :param obj: The request to create.

        :returns: requests.Response
        """
        url = "{0}/restore/".format(self.url)
        return requests.post(url, headers=self.headers(), data=json.dumps(obj))

    def restore_update(self, obj):
        """
        Updates a restore request.

        *** RESTORE IS NOT YET IMPLEMENTED ***

        :param obj_id: The ID of the restore request (NOT the ID of a DPN bag).

        :returns: requests.Response
        """
        url = "{0}/restore/{1}/".format(self.url, obj['event_id'])
        return requests.put(url, headers=self.headers(), data=json.dumps(obj))



# ------------------------------------------------------------------
# Transfer methods
# ------------------------------------------------------------------
    def transfer_list(self, **kwargs):
        """
        Returns a list of transfer requests, where the server wants you
        to transfer bags to your repository.

        :param dpn_object_id: Filter by exact DPN Object ID value.
        :param status: [P|A|R|C] to Filter by Pending, Accept, Reject or Confirmed status
        :param fixity: [true|false|none] to Filter by fixity status.
        :param valid: [true|false|none] to Filter by validation status.
        :param node: Filter by the namespace used for the node. ("aptrust"|"chron"|"sdr"...)
        :param created_on: Order result by record creation date. (prepend '-' to reverse order)
        :param updated_on: Order result by last update. (prepend '-' to reverse order)
        :param page_size: Max number of results per page.

        :returns: requests.Response
        """
        url = "{0}/transfer/".format(self.url)
        return requests.get(url, headers=self.headers(), data=kwargs)

    def transfer_get(self, event_id):
        """
        Returns the transfer requests with the specified id.

        :param event_id: The event_id of the transfer request you want to retrieve.

        :returns: requests.Response
        """
        url = "{0}/transfer/{1}/".format(self.url, event_id)
        return requests.get(url, headers=self.headers())

    def transfer_create(self, obj):
        """
        Creates a transfer request. Only the repository admin can make this call,
        which means you can issue this call only against your own node.

        :param obj: The request to create.

        :returns: requests.Response
        """
        url = "{0}/transfer/".format(self.url)
        return requests.post(url, headers=self.headers(), data=json.dumps(obj))

    def transfer_update(self, obj):
        """
        Updates a transfer request. The only fields in the transfer object
        relevant to this request are the event_id and status, which you
        must set to either 'A' (Accept) or 'R' (Reject).

        :param obj_id: The ID of the restore request (NOT the ID of a DPN bag).

        :returns: requests.Response
        """
        url = "{0}/transfer/{1}/".format(self.url, obj['event_id'])
        return requests.put(url, headers=self.headers(), data=json.dumps(obj))
