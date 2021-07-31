$(document).ready(function() {
    $('#getPriceSubmitBtn').click(function() {
        $(this).prop("disabled", true);
        $(this).prop("value", "Getting data ...");
        $("#url_form").submit()
    });




    $('#batchConvertSubmitBtn').click(function() {
        $(this).prop("disabled", true);
        $(this).prop("value", "Converting ...");
        $("#url_form").submit()
    });






    $('#emailsTable').DataTable( {
        "drawCallback": function( settings ) {
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

    $('.delete-email-btn').each(function(){
        $(this).on('click', function(){
            $('#delete_email_address_form input[id="id"]').val($(this).data("id"));
            console.log($(this).data("id"));
        });
    });
        }
    });


    $('#closeEmailFormModal').on('click', function(){
        $("#email_address_form").trigger("reset");
    });






    $('#copyEmailAddresses').on('click', function(){
        $("#copyAlert").show();

        var textAreaForEmails = $('.emailAdds');
        var emailAddresses = ""

        $('#emailsTable td:first-child').each(function(){
            emailAddresses += $(this).text() + ";";
        });

        textAreaForEmails.val(emailAddresses);

        textAreaForEmails.select();
        document.execCommand('copy');

    });

    $('#closeCopyAlert').on('click',function(e){
        e.preventDefault();
        $("#copyAlert").hide();
    });


    $('#calculateIBMForm').on('submit', function(e) {

        $('#BMIResult').children().remove();

        e.preventDefault();
        const formArray = $(this).serializeArray();
        const w = parseInt(formArray[0].value);
        const h = parseInt(formArray[1].value);


        const hToMeters = h / 100;
        const hToMeters2 = hToMeters * hToMeters


        const bmi =  w / hToMeters2;
        const idealWeight = hToMeters2 * 25;
        const excessWeight = w - idealWeight;
        const estimatedWeightLoss = excessWeight * 0.70

        console.log(bmi);

        $('#BMIResult').append(`
        <div class="col-7">
            <span class="mt-5 font-weight-bold">BMI Result:</span>
        </div>
        <div class="col-5">
            <span>${bmi.toFixed(2)}</span>
        </div>
        <div class="col-7">
            <span class="mt-5 font-weight-bold">Ideal Weight:</span>
        </div>
        <div class="col-5">
            ${idealWeight.toFixed(2)} kg
        </div>
        <div class="col-7">
            <span class="mt-5 font-weight-bold">Excess Weight: </span>
        </div>
        <div class="col-5">
            ${excessWeight.toFixed(2)} kg
        </div>
        <div class="col-7">
             <span class="mt-5 font-weight-bold">Estimated Weight Loss: </span>
        </div>
        <div class="col-5">
            ${estimatedWeightLoss.toFixed(2)} kg
        </div>
        `);

        $('#BMIResult .col-5').css({
            "font-weight": "bold",
            "font-size": "16px"
        });
    });
});

