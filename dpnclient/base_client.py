from . import const
import json
import requests
from requests.exceptions import RequestException

class BaseClient:
    """
    Base client for DPN REST service. This client returns requests.Response
    objects that include the status code of the response, and the raw text
    and json data. For all of this class's list/get/create/update methods,
    you'll be interested in the following attributes of the response object:

    response.status_code - Integer. HTTP status code returned by the server.
    response.text        - Raw response text. May be HTML on status code 500.
    response.json()      - The response JSON (for non-500 responses).

    For more information about the requests library and its Response objects,
    see the requests documentation at:

    http://docs.python-requests.org/en/latest/

    All methods that don't get the expected response from the server raise
    a RequestException, which the caller must handle. Check the response
    property of the RequestException for details (status_code, text, etc.).
    """
    def __init__(self, url, token):
        while url.endswith('/'):
            url = url[:-1]
        self.url = url
        self.token = token
        self.verify_ssl = True  # TDR cert is not legit - FIX THIS!

    def headers(self):
        """
        Returns a dictionary of default headers for the request.
        """
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

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/node/".format(self.url)
        response = requests.get(url, headers=self.headers(), params=kwargs,
                                verify=self.verify_ssl)
        if response.status_code != 200:
            raise RequestException(response.text, response=response)
        return response

    def node_get(self, namespace):
        """
        Returns the DPN node with the specified namespace.

        :param namespace: The namespace of the node. ('tdr', 'sdr', etc.)

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/node/{1}/".format(self.url, namespace)
        response = requests.get(url, headers=self.headers(), verify=self.verify_ssl)
        if response.status_code != 200:
            raise RequestException(response.text, response=response)
        return response


# ------------------------------------------------------------------
# Bag methods
# ------------------------------------------------------------------
    def bag_list(self, **kwargs):
        """
        Returns a requests.Response object whose json contains a list of
        bag entries.

        :param before: DPN DateTime string to FILTER results by last_modified_date earlier than this.
        :param after: DPN DateTime String to FILTER result by last_modified_date later than this.
        :param first_node: String to FILTER by node namespace.
        :param object_type: String character to FILTER by object type.
        :param ordering: ORDER return by (accepted values: last_modified_date)
        :param page_size: Number of max results per page.

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/bag/".format(self.url)
        response = requests.get(url, headers=self.headers(), params=kwargs,
                                verify=self.verify_ssl)
        if response.status_code != 200:
            raise RequestException(response.text, response=response)
        return response


    def bag_get(self, obj_id):
        """
        Returns a requests.Response object whose json contains the single
        bag entry that matches the specified obj_id.

        :param obj_id: A UUID string. The id of the bag entry to return.

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/bag/{1}/".format(self.url, obj_id)
        response = requests.get(url, headers=self.headers(), verify=self.verify_ssl)
        if response.status_code != 200:
            raise RequestException(response.text, response=response)
        return response


    def bag_create(self, obj):
        """
        Creates a bag entry. Only the repository admin can make this call,
        which means you can issue this call only against your own node.

        :param obj: The object to create.

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/bag/".format(self.url)
        response = requests.post(url, headers=self.headers(), data=json.dumps(obj),
                                 verify=self.verify_ssl)
        if response.status_code != 201:
            raise RequestException(response.text, response=response)
        return response


    def bag_update(self, obj):
        """
        Updates a bag entry. Only the repository admin can make this call,
        which means you can issue this call only against your own node.

        :param obj: The object to create.

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/bag/{1}/".format(self.url, obj['dpn_object_id'])
        response = requests.put(url, headers=self.headers(), data=json.dumps(obj),
                                verify=self.verify_ssl)
        if response.status_code != 200:
            raise RequestException(response.text, response=response)
        return response


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

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/restore/".format(self.url)
        response = requests.get(url, headers=self.headers(), params=kwargs,
                                verify=self.verify_ssl)
        if response.status_code != 200:
            raise RequestException(response.text, response=response)
        return response


    def restore_get(self, restore_id):
        """
        Returns the restore request with the specified event id.

        *** RESTORE IS NOT YET IMPLEMENTED ***

        :param obj_id: The restore_id of the restore request.

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/restore/{1}/".format(self.url, restore_id)
        response = requests.get(url, headers=self.headers(), verify=self.verify_ssl)
        if response.status_code != 200:
            raise RequestException(response.text, response=response)
        return response


    def restore_create(self, obj):
        """
        Creates a restore request. Only the repository admin can make this call,
        which means you can issue this call only against your own node.

        *** RESTORE IS NOT YET IMPLEMENTED ***

        :param obj: The request to create.

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/restore/".format(self.url)
        response = requests.post(url, headers=self.headers(), data=json.dumps(obj),
                                 verify=self.verify_ssl)
        if response.status_code != 201:
            raise RequestException(response.text, response=response)
        return response


    def restore_update(self, obj):
        """
        Updates a restore request.

        *** RESTORE IS NOT YET IMPLEMENTED ***

        :param obj_id: The ID of the restore request (NOT the ID of a DPN bag).

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/restore/{1}/".format(self.url, obj['restore_id'])
        response = requests.put(url, headers=self.headers(), data=json.dumps(obj),
                                verify=self.verify_ssl)
        if response.status_code != 200:
            raise RequestException(response.text, response=response)
        return response


# ------------------------------------------------------------------
# Replication Transfer methods
# ------------------------------------------------------------------
    def transfer_list(self, **kwargs):
        """
        Returns a list of transfer requests, where the server wants you
        to transfer bags to your repository.

        :param dpn_object_id: Filter by exact DPN Object ID value.
        :param status: Filter by request status ('Requested', 'Confirmed', etc)
        :param fixity: [true|false|none] to Filter by fixity status.
        :param valid: [true|false|none] to Filter by validation status.
        :param from_node: Filter by namespace that originated request. ("aptrust"|"chron"|"sdr"...)
        :param to_node: Filter by namespace that should fulfill request. ("aptrust"|"chron"|"sdr"...)
        :param created_on: Order result by record creation date. (prepend '-' to reverse order)
        :param updated_on: Order result by last update. (prepend '-' to reverse order)
        :param page_size: Max number of results per page.

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/replicate/".format(self.url)
        response = requests.get(url, headers=self.headers(), params=kwargs,
                                verify=self.verify_ssl)
        if response.status_code != 200:
            raise RequestException(response.text, response=response)
        return response


    def transfer_get(self, replication_id):
        """
        Returns the transfer requests with the specified id.

        :param replication_id: The replication_id of the transfer request you want to retrieve.

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/replicate/{1}/".format(self.url, replication_id)
        response = requests.get(url, headers=self.headers(), verify=self.verify_ssl)
        if response.status_code != 200:
            raise RequestException(response.text, response=response)
        return response


    def transfer_create(self, obj):
        """
        Creates a transfer request. Only the repository admin can make this call,
        which means you can issue this call only against your own node.

        :param obj: The request to create.

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/replicate/".format(self.url)
        response = requests.post(url, headers=self.headers(), data=json.dumps(obj),
                                 verify=self.verify_ssl)
        if response.status_code != 201:
            raise RequestException(response.text, response=response)
        return response


    def transfer_update(self, obj):
        """
        Updates a transfer request. The only fields in the transfer object
        relevant to this request are the replication_id, fixity_value,
        and status, which you must set to either 'A' (Accept) or 'R' (Reject).

        :param obj_id: The ID of the restore request (NOT the ID of a DPN bag).

        :returns: requests.Response

        :raises RequestException: Check the response property for details.
        """
        url = "{0}/api-v1/replicate/{1}/".format(self.url, obj['replication_id'])

        print("transfer_update " + json.dumps(obj))
        print("Headers: " + str(self.headers()))
        print("URL: " + url)

        response = requests.put(url, headers=self.headers(), data=json.dumps(obj),
                                verify=self.verify_ssl)
        if response.status_code != 200:
            raise RequestException(response.text, response=response)
        return response
