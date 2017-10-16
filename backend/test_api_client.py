import json
import unittest
from unittest.mock import patch

from api_client import ZendeskApiClient, API_ROOT

test_ticket = {
    "subject": "Subject",
    "description": "Description",
    "updated_at": "2017-01-01T00:00:00Z"
}


class MockRequests(object):
    """ Helper class to mock the Zendesk REST API for unit testing """
    class MockResponse(object):
        def __init__(self, json):
            self._json = json

        def json(self):
            return self._json

    api_dict = {
        API_ROOT + "/api/v2/tickets.json": MockResponse({"tickets": [test_ticket], "next_page": API_ROOT + "/api/v2/tickets.json?page=2"}),
        API_ROOT + "/api/v2/tickets.json?page=2": MockResponse({"tickets": [test_ticket], "next_page": None}),
        API_ROOT + "/api/v2/tickets/1.json": MockResponse({"ticket": test_ticket})
    }

    def get(self, uri, **kwArgs):
        return self.api_dict[uri]


class TestZendeskApiClient(unittest.TestCase):
    client = ZendeskApiClient()

    @patch("requests.get")
    def test_list_tickets(self, mock_get):
        mock_get.side_effect = MockRequests().get
        tickets = self.client.list_tickets()
        self.assertEqual(tickets, [test_ticket, test_ticket])

    @patch("requests.get")
    def test_get_ticket(self, mock_get):
        mock_get.side_effect = MockRequests().get
        tickets = self.client.get_ticket(1)
        self.assertEqual(tickets, test_ticket)

if __name__ == "__main__":
    unittest.main()
