from flask import Flask, request, make_response
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

def _lookup_ticket(ticket_id):
    ticket_json = app.client.get_ticket(ticket_id)
    ticket = _extract_fields(ticket_json["ticket"])
    return _create_response(json.dumps(ticket), 200)

@app.route("/ticket/<ticket_id>")
def lookup_ticket(ticket_id):
    """ Endpoint to look up ticket info 
    Args:
        ticket_id: Ticket id string
    
    Returns:
        Ticket info """
    try:
        return _lookup_ticket(ticket_id)
    except ConnectTimeout:
        return _create_response("Zendesk API appears to be unavailable...", 503)
    except Exception as e:
        app.logger.error(str(e))
        return _create_response("Internal server error", 500)

def _list_tickets():
    tickets_json = app.client.list_tickets()
    tickets = [_extract_fields(t) for t in tickets_json["tickets"]]
    return _create_response(json.dumps(tickets), 200)

@app.route("/tickets")
def list_tickets():
    """ Endpoint to list all tickets """
    try:
        return _list_tickets()
    except ConnectTimeout:
        return _create_response("Zendesk API appears to be unavailable...", 503)
    except Exception as e:
        app.logger.error(str(e))
        return _create_response("Internal server error", 500)

if __name__ == "__main__":
    app.run()
