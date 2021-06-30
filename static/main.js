$(document).ready(function() {
    $('input[type="submit"]').click(function() {
        $(this).prop("disabled", true);
        $(this).prop("value", "Getting data ...");
        $("#url_form").submit()
    });

});