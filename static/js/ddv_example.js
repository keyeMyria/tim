$(document).ready(function() {
    var dt_table = $('.datatable').dataTable({
        "bFilter": true,
        "aLengthMenu": [[25, 50, 100, 200], [25, 50, 100, 200]],
        "iDisplayLength" : 25,
        "aaSorting": [[ 0, "desc" ]],
        "bAutoWidth": true,
        "aoColumns": [
                        { "bSortable": true, "bSearchable": true, "sClass": "center" },
                        { "bSortable": true, "bSearchable": true, "sClass": "center" },
                        ],
        "processing": true,
        "serverSide": true,
        "stateSave": true,
        "ajax": USERS_LIST_JSON_URL
    });
});
