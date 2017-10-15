from flask import Flask, request, make_response
import json

from api_client import ZendeskApiClient 

app = Flask(__name__)
app.client = ZendeskApiClient()

def _extract_fields(ticket):
    """ Given ticket info dictionary, extract the fields that are of interest """
    fields = ["id", "subject", "description", "updated_at"]
    return {field: ticket[field] for field in fields}

@app.route("/lookup/<ticket_id>")
def lookup_ticket(ticket_id):
    """ Look up ticket info 
    Args:
        ticket_id: Ticket id string
    
    Returns:
        Ticket info """
    ticket_json = app.client.get_ticket(ticket_id)
    ticket = _extract_fields(ticket_json["ticket"])
    return json.dumps(ticket)

@app.route("/tickets")
def list_tickets():
    """ List all tickets """
    tickets_json = app.client.list_tickets()
    tickets = [_extract_fields(t) for t in tickets_json["tickets"]]
    return json.dumps(tickets)

if __name__ == "__main__":
    app.run()
