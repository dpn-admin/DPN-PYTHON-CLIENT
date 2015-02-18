from dpnclient.base_client import BaseClient

# TODO: Integration tests!

def test_headers():
    baseclient = BaseClient("http://www.example.com", "API_TOKEN_1234")
    headers = baseclient.headers()
    assert headers['Content-Type'] == 'application/json'
    assert headers['Accept'] == 'application/json'
    assert headers['Authorization'] == 'token API_TOKEN_1234'
