$(document).ready(function() {
    var table = $('.datatable').DataTable( {
        dom: 'Bfrtip',
        lengthChange: false,
        buttons: [ 'copy', 'excel', 'pdf',
                {
                text: 'Add',
                action: function ( e, dt, node, config ) {
                    window.location = '/observables/add';
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

        $('#addObserv').submit(function() { // catch the form's submit event
            $.ajax({ // create an AJAX call...
                data: $(this).serialize(), // get the form data
                type: $(this).attr('method'), // GET or POST
                url: $(this).attr('action'), // the file to call
                success: function(response) { // on success..
                    $('#tab3').html(response); // update the DIV
                }
            });
            return false;
        });

    function postSearch(url, csrf, query) {
       // Send the data using post
       var posting = $.post( url, { search: query, csrfmiddlewaretoken: csrf } );
      
       // Put the results in a div
       posting.done(function( data ) {
         $("#search-result-container").empty().append(data);
       });
     }          

     $(function() {

       $("#observable_add").submit(function(event) {
         // Stop form from submitting normally
         event.preventDefault();

         var $form = $( this ),
           term = $form.find( "input[name='search']" ).val(),
           url = $form.attr( "action" );

         var csrf = $('input[name="csrfmiddlewaretoken"]').val();

         postSearch(url, csrf, term);
       });
     });

});
