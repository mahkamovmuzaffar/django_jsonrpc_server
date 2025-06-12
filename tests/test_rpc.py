from django.test import TestCase, Client
import json


class JsonRPCTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def call_rpc(self, method, params=None, id=1):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": id
        }
        response = self.client.post(
            "/rpc/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        return json.loads(response.content)

    def test_ping_method(self):
        response = self.call_rpc("ping")
        self.assertIn("result", response)
        self.assertEqual(response["result"], "pong")

    def test_method_not_found(self):
        response = self.call_rpc("non_existing_method")
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32601)  # Method not found

    def test_invalid_params(self):
        response = self.call_rpc("some_method", {"wrong": "param"})
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)  # Invalid params
