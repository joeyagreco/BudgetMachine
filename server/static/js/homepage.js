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