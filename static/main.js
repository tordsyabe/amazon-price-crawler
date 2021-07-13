$(document).ready(function() {
    $('#getPriceSubmitBtn').click(function() {
        $(this).prop("disabled", true);
        $(this).prop("value", "Getting data ...");
        $("#url_form").submit()
    });

});

$(document).ready(function() {
    $('#batchConvertSubmitBtn').click(function() {
        $(this).prop("disabled", true);
        $(this).prop("value", "Converting ...");
        $("#url_form").submit()
    });



    });

$(document).ready(function () {
      $('#emailsTable').DataTable();
      });