$(document).ready(function() {
    var table = $('#observable_dt').DataTable( {
        dom: 'Bfrtip',
        lengthChange: false,
        buttons: [ 'copy', 'excel', 'pdf', 
                {
                text: 'Add',
                action: function ( e, dt, node, config ) {
                    window.location = '/events/add';
                }
            }
        ],
        "searching": true,
        'pageLength': 10,
        "lengthMenu": [ 1, 10, 25, 50, 75, 100 ],
        "length" : 25,
        //"aaSorting": [[ 0, "desc" ]],
        "autoWidth": false,
        "columns": [
                        { "sortable": true, "searchable": true, "class": "center" },
                        { "sortable": true, "searchable": true, "class": "center" },
                        { "sortable": true, "searchable": true, "class": "center" },
                        { "sortable": true, "searchable": true, "class": "center" },
                        { "sortable": false, "searchable": false, "class": "center" },
                        ],
        "processing": true,
        "serverSide": true,
        "stateSave": true,
        "ajax": USERS_LIST_JSON_URL

    } );
 
    table.buttons().container()
        .appendTo( '.datatable .col-md-6:eq(0)' );

    var table = $('#event_dt').DataTable( {
        dom: 'Bfrtip',
        lengthChange: false,
        buttons: [ 'copy', 'excel', 'pdf', 
                {
                text: 'Add',
                action: function ( e, dt, node, config ) {
                    window.location = '/events/add';
                }
            }
        ],
        "searching": true,
        'pageLength': 10,
        "lengthMenu": [ 1, 10, 25, 50, 75, 100 ],
        "length" : 25,
        //"aaSorting": [[ 0, "desc" ]],
        "autoWidth": false,
        "columns": [
                        { "sortable": true, "searchable": true, "class": "center" },
                        { "sortable": true, "searchable": true, "class": "center" },
                        { "sortable": true, "searchable": true, "class": "center" },
                        { "sortable": true, "searchable": true, "class": "center" },
                        { "sortable": false, "searchable": false, "class": "center" },
                        ],
        "processing": true,
        "serverSide": true,
        "stateSave": true,
        "ajax": USERS_LIST_JSON_URL

    } );
 
    table.buttons().container()
        .appendTo( '.datatable .col-md-6:eq(0)' );

} );
