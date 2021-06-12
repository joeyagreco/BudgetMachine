function initializeTable() {
    $(document).ready( function () {
        $('#transactionsTable').DataTable(
            {
                "order": [[ 5, "desc" ]],
                "iDisplayLength": 25,
                "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]
            }
        );
    } );
}

function setEnvironmentSwitch() {
    let envSwitch = document.getElementById("environment-switch");
    envSwitch.checked = envSwitch.dataset.checked == "True";
}

function onEnvironmentSwitchClick() {
    // check if checkbox is checked or not then send to route
    let checked = document.getElementById("environment-switch").checked;
    window.location = "/update-data-environment?checked=" + checked;
}

function openTransaction(tId) {
    onTransactionClick();
    // populate transaction form with appropriate values
    document.getElementById("amount-input").value = document.getElementById("transaction-amount-" + tId).innerHTML;
    let category = document.getElementById("transaction-category-" + tId).innerHTML
    document.getElementById("category-button").innerHTML = category;
    // set dropdown to be selected
    document.getElementById(category).classList.add("active");
    if(document.getElementById("transaction-isIncome-" + tId).innerHTML == "True") {
        document.getElementById("flexSwitchCheckDefault").checked = "True";
    }
    document.getElementById("note").value = document.getElementById("transaction-note-" + tId).innerHTML;
    document.getElementById("date-input").value = document.getElementById("transaction-date-" + tId).innerHTML;
}

function init() {
    // runs all methods that need to be ran on page load
    initializeTable();
    setEnvironmentSwitch();
}