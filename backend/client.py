import requests

auth = ("dana.ma537@gmail.com", "ticket")
API_ROOT = "https://ticketviewerdana.zendesk.com"

class ZendeskApiClient(object):
    """ Client which calls the Zendesk Rest API """
    def _get(self, uri):
        return requests.get(API_ROOT + uri, auth=auth)

    def list_tickets(self):
        """ List all tickets as a JSON dictionary """
        tickets = self._get("/api/v2/tickets.json")
        return tickets.json()


if __name__ == "__main__":
    print(ZendeskApiClient().list_tickets())
