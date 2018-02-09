$(document).ready(function() {

$('[data-toggle=tab]').click(function () {
  return true;}
);


// form submit
$( "#eventEdit" ).submit(function( event ) {
  console.log("Handler for .submit() called..");
  console.log( $( this ).serialize() );
});

$('.form_datepicker').datetimepicker({
    defaultDate: null,
    focusOnShow: false,
    format: 'DD.MM.YYYY' /*remove this line if you want to use time as well */
});

//$('#last_seen_picker').datetimepicker({
//    defaultDate: null ,
//    focusOnShow: false,
//    format: 'DD.MM.YYYY' /*remove this line if you want to use time as well */
//});
//
//$('#expiration_date_picker').datetimepicker({
//    defaultDate: null ,
//    focusOnShow: false,
//    format: 'DD.MM.YYYY' /*remove this line if you want to use time as well */
//});
//


});
