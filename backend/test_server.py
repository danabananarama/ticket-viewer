import server
import json
import unittest

test_ticket = {
    "id":           1,
    "subject":      "Subject",
    "description":  "Description",
    "updated_at":   "2017-01-01T00:00:00Z"
}

class MockApiClient(object):
    """ Class for mocking the API Client """
    def get_ticket(self, ticket_id):
        return {"ticket": test_ticket}

    def list_tickets(self):
        return {"tickets": [test_ticket]}

class TicketViewerTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        server.app.client = MockApiClient()
        self.app = server.app.test_client()

    def test_lookup_ticket(self):
        response = self.app.get("/ticket/1")
        self.assertEqual(json.loads(response.data), test_ticket)

    def test_list_tickets(self):
        response = self.app.get("/tickets")
        self.assertEqual(json.loads(response.data), [test_ticket])

if __name__ == "__main__":
    unittest.main()

