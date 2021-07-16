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

$(document).ready(function(){

    var textAreaForEmails = $('.emailAdds');
    var emailAddresses = ""

    $('#emailsTable td:first-child').each(function(){
        emailAddresses += $(this).text() + ";";
    });

    textAreaForEmails.val(emailAddresses);

    $('#copyEmailAddresses').on('click', function(){
        $("#copyAlert").show();

        textAreaForEmails.select();
        document.execCommand('copy');

    });

    $('#closeCopyAlert').on('click',function(e){
        e.preventDefault();
        $("#copyAlert").hide();
    });



});