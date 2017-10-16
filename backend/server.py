from flask import Flask, request, make_response
from functools import wraps
import json
from requests.exceptions import ConnectTimeout

from api_client import ZendeskApiClient, ZendeskApiException

app = Flask(__name__)
app.client = ZendeskApiClient()

def _extract_fields(ticket):
    """ Given ticket info dictionary, extract the fields that are of interest """
    fields = ["id", "subject", "description", "updated_at"]
    return {field: ticket[field] for field in fields}

def _create_response(payload, status_code):
    response = make_response(payload, status_code)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

def endpoint(f):
    """ Endpoint decorator which wraps the result in a HTTP response and handles errors """
    @wraps(f)
    def wrapper(*args, **kw_args):
        try:
            result = f(*args, **kw_args) 
            return _create_response(result, 200)
        except ConnectTimeout:
            app.logger.error("Connection timeout while waiting for the API")
            return _create_response("Zendesk API appears to be unavailable...", 504)
        except ZendeskApiException as e:
            app.logger.error("Unexpected response from Zendesk API: {}" + e.message)
            return _create_response("Unexpected response from the Zendesk API.", 503)
        except Exception as e:
            app.logger.error(str(e))
            return _create_response("Internal server error", 500)
    return wrapper

@app.route("/ticket/<ticket_id>")
@endpoint
def lookup_ticket(ticket_id):
    """ Endpoint to look up ticket info 
    Args:
        ticket_id: Ticket id string
    
    Returns:
        Ticket info """
    ticket_json = app.client.get_ticket(ticket_id)
    ticket = _extract_fields(ticket_json)
    return json.dumps(ticket)

@app.route("/tickets")
@endpoint
def list_tickets():
    """ Endpoint to list all tickets """
    tickets_json = app.client.list_tickets()
    tickets = [_extract_fields(t) for t in tickets_json]
    return json.dumps(tickets)

if __name__ == "__main__":
    app.run()

