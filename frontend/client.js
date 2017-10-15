var server = "http://localhost:5000";
var ticketFields = Array("id", "subject", "description", "updated_at");

function viewTicket() {
    /* Call the API to look up ticket information for a single ticket and display it */
    var ticketID = document.getElementById("ticketID").value;
    var url = `${server}/ticket/${ticketID}`;

    $.get(url, function(data){
        // TODO: handle failure
        buildTicketView(JSON.parse(data));
    })
}

function buildTicketView(ticket) {
    /* Build up the view of the ticket */
    var container = document.getElementById("ticketContainer");
    container.innerHTML = "";
    var table = document.createElement("table");
    ticketFields.map(field => {
        row = document.createElement("tr");
        row.appendChild(createHeaderCell(field));
        row.appendChild(createBodyCell(ticket[field]));
        table.appendChild(row);
    })

    container.appendChild(table);
}

function listTickets() {
    /* Call the API to get the list of tickets and display it in a table */
    $.get(server + "/tickets", function(data){
        // TODO: handle failure
        buildTable(JSON.parse(data));
    })
}

function buildTable(tickets) {
    /* Given the array of ticket objects, build the ticket info table in the DOM */
    var container = document.getElementById("ticketContainer");
    container.innerHTML = "";
    var table = document.createElement("table");
    var header = document.createElement("tr");

    ticketFields.map(field => {
        header.appendChild(createHeaderCell(field.replace("_", " ")));
    })

    table.appendChild(header);

    tickets.map(ticket => {
        var row = createRow(ticket);
        table.appendChild(row);
    })

    container.appendChild(table);
}

function createRow(ticket) {
    var row = document.createElement("tr");

    ticketFields.map(field => {
        cell = createBodyCell(ticket[field])
        row.appendChild(cell);
    })

    return row;
}

function createHeaderCell(content) {
    return createCell(content, "th")
}

function createBodyCell(content) {
    return createCell(content, "td")
}

function createCell(content, cellType) {
    var cell = document.createElement(cellType);
    cell.innerHTML = content;
    return cell;
}
