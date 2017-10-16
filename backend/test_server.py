import json
from requests.exceptions import ConnectTimeout
import unittest

from api_client import ZendeskApiException
import server

test_ticket = {
    "id":           1,
    "subject":      "Subject",
    "description":  "Description",
    "updated_at":   "2017-01-01T00:00:00Z"
}


class MockApiClient(object):
    """ Class for mocking the API Client """
    def get_ticket(self, ticket_id):
        if ticket_id == "1":
            return test_ticket
        elif ticket_id == "timeout":
            raise ConnectTimeout
        elif ticket_id == "api_error":
            raise ZendeskApiException("Test error")
        else:
            raise Exception("No such ticket")

    def list_tickets(self):
        return [test_ticket]


class TicketViewerTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        server.app.client = MockApiClient()
        self.app = server.app.test_client()

    def test_lookup_ticket(self):
        response = self.app.get("/ticket/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), test_ticket)

    def test_handles_failures(self):
        response = self.app.get("/ticket/2")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data, b"Internal server error")

    def test_handles_timeouts(self):
        response = self.app.get("/ticket/timeout")
        self.assertEqual(response.status_code, 504)
        self.assertEqual(response.data, b"Zendesk API appears to be unavailable...")

    def test_handles_api_error(self):
        response = self.app.get("/ticket/api_error")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.data, b"Unexpected response from the Zendesk API.")

    def test_list_tickets(self):
        response = self.app.get("/tickets")
        self.assertEqual(json.loads(response.data), [test_ticket])

if __name__ == "__main__":
    unittest.main()
