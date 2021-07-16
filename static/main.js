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

$(document).ready(function () {
    $('#closeEmailFormModal').on('click', function(){
        $("#email_address_form").trigger("reset");
    });

    $('.edit-email-btn').each(function(){
        $(this).on('click', function(){
            $('input[id="id"').val($(this).data("id"));
            $('input[id="email_address"').val($(this).parent().siblings()[0].textContent);
            $('input[id="employee_name"').val($(this).parent().siblings()[1].textContent);
            $('input[id="designation"').val($(this).parent().siblings()[2].textContent);
            $('select[id="department"').val($(this).parent().siblings()[3].textContent).change();;
            $('select[id="status"').val($(this).parent().siblings()[4].textContent).change();;
        });
    });
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

