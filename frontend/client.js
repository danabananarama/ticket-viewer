var server = "http://localhost:5000";
var ticketFields = Array("id", "subject", "description", "updated_at");
var ticketsPerPage = 100;
var tickets = Array();

function viewTicket() {
    /* Call the API to look up ticket information for a single ticket and display it */
    var ticketID = document.getElementById("ticketID").value;
    var url = `${server}/ticket/${ticketID}`;

    $.get(url, function(data) {
        buildTicketView(JSON.parse(data));
    }).fail(function(response) {
        displayError(response);
    })
}

function buildTicketView(ticket) {
    /* Build up the view of the ticket */
    clearTickets();
    var container = document.getElementById("ticketContainer");
    var table = document.createElement("table");
    ticketFields.map(field => {
        row = document.createElement("tr");
        row.appendChild(createHeaderCell(field));
        row.appendChild(createBodyCell(ticket[field]));
        table.appendChild(row);
    })

    container.appendChild(table);
}

function displayError(response) {
    clearTickets();
    var container = document.getElementById("ticketContainer");
    var errorDisplayed = "";

    if (response.status == 504) {
        errorDisplayed = "Zendesk API unresponsive";
    } else if (response.status == 503) {
        errorDisplayed = "Zendesk API returned an unexpected response";
    } else if (response.status == 500) {
        errorDisplayed = "Server error; please contact technical support";
    }

    var errorContainer = document.createElement("div")
    errorContainer.setAttribute("class", "error")
    errorContainer.innerHTML = errorDisplayed;
    container.appendChild(errorContainer)
}

function listTickets() {
    /* Call the API to get the list of tickets and display it in a table */
    displayWaitingMessage();

    $.get(server + "/tickets", function(data){
        tickets = JSON.parse(data);
        var numPages = Math.ceil(tickets.length / ticketsPerPage);
        setNumberPages(numPages);
        displayTickets(tickets, 1);
    }).fail(function(response) {
        displayError(response);
    })
}

function displayWaitingMessage() {
    clearTickets();
    var container = document.getElementById("ticketContainer");
    container.innerHTML = "Querying Zendesk API...";
}

function setNumberPages(numPages) {
    var container = document.getElementById("pages");
    for (page = 1; page <= numPages; page++) {
        var button = document.createElement("button");
        button.innerHTML = page;
        // Using closures to solve the issue of javascript scoping
        button.onclick = function(page){return function(){showPage(page)};}(page);
        container.appendChild(button);
    }
}

function showPage(pageNo) {
    displayTickets(tickets, pageNo)
}

function displayTickets(tickets, pageNo) {
    var start = ticketsPerPage * (pageNo - 1);
    var end = ticketsPerPage * pageNo - 1
    buildTable(tickets.slice(start, end))
}

function clearTickets() {
    /* Clear the last tickets viewed */
    var container = document.getElementById("ticketContainer");
    container.innerHTML = "";
    var pages = document.getElementById("pages");
    pages.innerHTML = "";
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
