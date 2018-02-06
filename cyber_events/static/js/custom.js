$(document).ready(function() {

$('[data-toggle=tab]').click(function () {
  return true;}
);


// form submit
$( "#eventEdit" ).submit(function( event ) {
  console.log("Handler for .submit() called..");
  console.log( $( this ).serialize() );
//  event.preventDefault();
});

$('#datetimepicker6').datetimepicker({
    focusOnShow: false,
    format: 'DD.MM.YYYY' /*remove this line if you want to use time as well */
});

//$.extend( $.fn.dataTable.defaults, {
//    searching: false,
//} );
//
//$('#BSdataTable').DataTable();

});
