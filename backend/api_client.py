import requests

auth = ("dana.ma537@gmail.com", "ticket")
API_ROOT = "https://ticketviewerdana.zendesk.com"


class ZendeskApiException(Exception):
    pass


class ZendeskApiClient(object):
    """ Client which calls the Zendesk Rest API """
    def error_handler(f):
        def wrapper(*args, **kw_args):
            try:
                return f(*args, **kw_args)
            except requests.exceptions.ConnectTimeout:
                raise
            except Exception as e:
                raise ZendeskApiException(e.message)
        return wrapper

    def _get(self, url, append_root=True):
        """ Make a GET request to the API, timing out if there is no response within 30 seconds """
        return requests.get(url, auth=auth, timeout=30)

    @error_handler
    def get_ticket(self, ticket_id):
        """ Given a ticket id, return the ticket info in a JSON dictionary"""
        response = self._get(API_ROOT + "/api/v2/tickets/{}.json".format(ticket_id))
        return response.json()["ticket"]

    @error_handler
    def list_tickets(self):
        """ List all tickets from the API.
        When more than a hundred tickets are returned, flattens the results paginated by the API.

        Returns:
            List of all tickets """
        url = API_ROOT + "/api/v2/tickets.json"
        tickets = []
        while url:
            response = self._get(url)
            data = response.json()
            tickets.extend(data['tickets'])
            url = data['next_page']
        return tickets
