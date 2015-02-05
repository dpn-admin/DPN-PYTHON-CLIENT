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
        url = "{0}/node/".format(self.url)
        return requests.get(url, headers=self.headers(), data=kwargs)

    def node_get(self, namespace):
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

    def registry_create(self, registry_obj):
        """
        Creates a registry entry. Only the repository admin can make this call,
        which means you can issue this call only against your own node.

        :param registry_obj: The object to create.

        :returns: requests.Response
        """
        url = "{0}/registry/".format(self.url)
        return requests.post(url, headers=self.headers(), data=json.dumps(registry_obj))

    def registry_update(self, registry_obj):
        """
        Updates a registry entry. Only the repository admin can make this call,
        which means you can issue this call only against your own node.

        :param registry_obj: The object to create.

        :returns: requests.Response
        """
        url = "{0}/registry/{1}/".format(self.url, registry_obj['dpn_object_id'])
        return requests.put(url, headers=self.headers(), data=json.dumps(registry_obj))



# ------------------------------------------------------------------
# Restoration methods
# ------------------------------------------------------------------
    def restore_list(self, **kwargs):
        url = "{0}/restore/".format(self.url)
        return requests.get(url, headers=self.headers(), data=kwargs)

    def restore_get(self, event_id):
        url = "{0}/restore/{1}/".format(self.url, event_id)
        return requests.get(url, headers=self.headers())

    def restore_create(self, object_id):
        pass

    def restore_update(self, restore_obj):
        pass


# ------------------------------------------------------------------
# Transfer methods
# ------------------------------------------------------------------
    def transfer_list(self, **kwargs):
        url = "{0}/transfer/".format(self.url)
        return requests.get(url, headers=self.headers(), data=kwargs)

    def transfer_get(self, event_id):
        url = "{0}/transfer/{1}/".format(self.url, event_id)
        return requests.get(url, headers=self.headers())

    def transfer_create(self, transfer_obj):
        pass

    def transfer_update(self, transfer_obj):
        pass
