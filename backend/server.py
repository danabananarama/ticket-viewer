from flask import Flask, request, make_response
from functools import wraps
import json
from requests.exceptions import ConnectTimeout

from api_client import ZendeskApiClient 

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

def error_handler(f):
    @wraps(f)
    def wrapper(*args, **kw_args):
        try:
            return f(*args, **kw_args)
        except ConnectTimeout:
            return _create_response("Zendesk API appears to be unavailable...", 503)
        except Exception as e:
            app.logger.error(str(e))
            return _create_response("Internal server error", 500)
    return wrapper

@app.route("/ticket/<ticket_id>")
@error_handler
def lookup_ticket(ticket_id):
    """ Endpoint to look up ticket info 
    Args:
        ticket_id: Ticket id string
    
    Returns:
        Ticket info """
    ticket_json = app.client.get_ticket(ticket_id)
    ticket = _extract_fields(ticket_json)
    return _create_response(json.dumps(ticket), 200)

@app.route("/tickets")
@error_handler
def list_tickets():
    """ Endpoint to list all tickets """
    tickets_json = app.client.list_tickets()
    tickets = [_extract_fields(t) for t in tickets_json]
    return _create_response(json.dumps(tickets), 200)

if __name__ == "__main__":
    app.run()

