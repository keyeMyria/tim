$(document).ready(function() {

$('[data-toggle=tab]').click(function () {
  return true;}
);



$('#event_date_picker').datetimepicker({
    focusOnShow: false,
    format: 'DD.MM.YYYY' /*remove this line if you want to use time as well */
});

});
