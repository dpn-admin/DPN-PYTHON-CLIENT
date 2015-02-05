import requests

class Client:

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'token {0}'.format(self.token),
        }

    def node_list(self):
        url = "{0}/node/".format(self.url)
        return requests.get(url, headers=self.headers())

    def node_get(self, namespace):
        url = "{0}/node/{1}/".format(self.url, namespace)
        return requests.get(url, headers=self.headers())

    def registry_list(self):
        pass

    def registry_get(self, obj_id):
        pass

    def registry_create(self, registry_obj):
        pass

    def registry_update(self, registry_obj):
        pass

    def restore_list(self):
        pass

    def restore_get(self, event_id):
        pass

    def restore_create(self, object_id):
        pass

    def restore_update(self, restore_obj):
        pass

    def transfer_list(self):
        pass

    def transfer_get(self, event_id):
        pass

    def transfer_create(self, transfer_obj):
        pass

    def transfer_update(self, transfer_obj):
        pass
