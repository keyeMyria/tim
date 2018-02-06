$(document).ready(function() {

$.extend( $.fn.dataTable.defaults, {
    searching: false,
    paging: false,
} );

$('#BSdataTable').DataTable();

});
