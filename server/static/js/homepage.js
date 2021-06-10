function initializeTable() {
    $(document).ready( function () {
        $('#transactionsTable').DataTable(
            {
                "order": [[ 5, "desc" ]],
                "searching": false,
                "iDisplayLength": 25,
                "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]
            }
        );
    } );
}

window.onload = initializeTable();

function onEnvironmentSwitchClick() {
    // check if checkbox is checked or not then send to route
    let checked = document.getElementById("environment-switch").checked;
    window.location = "/update-data-environment?checked=" + checked;
}